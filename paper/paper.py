import urllib2
import xmltodict
import settings
import extract
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
from helper import *


class Paper:

    def __init__(self, id):
        self.id = id
        self.text = Paper._get_text(id)
        self.xml = xmltodict.parse(Paper._get_xml(id))
        self.pars = xmltodict.parse(self._get_pars())

    @property
    def xml_citations(self):
        if self.xml['document'].get('citations'):
            if self.xml['document']['citations'].get('citation'):
                citations = self.xml['document']['citations']['citation']
                if type(citations) != list:
                    return [citations]
                return citations
        return list()

    @property
    def cid(self):
        try:
            return self.xml['document'].get('clusterid')
        except urllib2.HTTPError:
            return None

    @property
    def title(self):
        return self.xml['document']['title']

    @property
    def abstract(self):
        return self.xml['document']['abstract']

    @property
    def year(self):
        return self.xml['document']['year']

    @property
    def pars_citations(self):
        algs = self.pars['algorithms']['algorithm']
        for i in algs:
            if i.get('citationList'):
                return i['citationList']['citation']
        return list()

    @staticmethod
    def _id_to_path(id, type_doc):
        ''' type_doc get 'xml' or 'text' input '''
        return settings.DATA_HOST + type_doc + '/' + id.replace('.', '/') + '/'

    @staticmethod
    def _get_text(id):
        url = Paper._id_to_path(id, 'text') + id + '.txt'
        return urllib2.urlopen(url).read()

    @staticmethod
    def _get_xml_last_version(id):
        url = Paper._id_to_path(id, 'xml')
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        return soup.select('a')[-1]['href']

    @staticmethod
    def _get_xml(id):
        last_version = Paper._get_xml_last_version(id)
        url = Paper._id_to_path(id, 'xml') + last_version
        return urllib2.urlopen(url).read()

    def _get_pars(self):
        return extract.extract_all(self.text)

    @staticmethod
    def is_citation_same(pars_raw, xml_raw):
        ''' This function check extracted citation is same
        using citation raws'''
        pars_raw = ''.join(e for e in pars_raw if e.isalnum()).lower()
        xml_raw = ''.join(e for e in xml_raw if e.isalnum()).lower()
        if pars_raw in xml_raw or xml_raw in pars_raw:
            return 1
        return SequenceMatcher(None, pars_raw, xml_raw).ratio()

    def find_cid_of_pars_citation(self, pars_raw):
        max_match = 0.6
        cid = None
        for i in self.xml_citations:
            if i.get('paperid') and i.get('title') and i.get('clusterid'):
                sim = Paper.is_citation_same(i['raw'], pars_raw)
                if sim > max_match:
                    max_match, cid = sim, i['clusterid']
        return cid

    def find_all_cid_of_pars_citation(self):
        cid_context = list()
        for i in if_not_list_make_list(self.pars_citations):
            if i.get('contexts') and i.get('rawString') and i.get('@valid'):
                cid = self.find_cid_of_pars_citation(i['rawString'])
                if cid:
                    for j in if_not_list_make_list(i['contexts']):
                        if j.get('context'):
                            ctx = list()
                            for z in if_not_list_make_list(j['context']):
                                if z.get('#text'):
                                    ctx.append(z['#text'])
                            cid_context.append((cid, ctx))
        return cid_context
