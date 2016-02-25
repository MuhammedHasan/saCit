import urllib2
import xmltodict
import settings
import extract
from difflib import SequenceMatcher
from bs4 import BeautifulSoup


class Paper:

    def __init__(self, id):
        self.id = id
        self.text = Paper._get_text(id)
        self.xml = xmltodict.parse(Paper._get_xml(id))
        self.pars = xmltodict.parse(self._get_pars())

    @property
    def xml_citations(self):
        return self.xml['document']['citations']['citation']

    @property
    def pars_citations(self):
        algs = self.pars['algorithms']['algorithm']
        for i in algs:
            if 'citationList' in i.keys():
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

    def find_title_of_pars_citation(self, pars_raw):
        max_match = 0.6
        matching_title = None
        for i in self.xml_citations:
            if i.get('paperid') and i.get('title'):
                sim = Paper.is_citation_same(i['raw'], pars_raw)
                if sim > max_match:
                    max_match, matching_title = sim, i['title']
        return matching_title

    def get_ids_and_contexts_of_citation(self, doi_title):
        ids = list()
        for i in self.pars_citations:
            title = self.find_title_of_pars_citation(i)
            paper_id = filter(lambda x: x['title'] == title, doi_title)
            if paper_id:
                ids.append(paper_id[0]['doi'])
        return ids
