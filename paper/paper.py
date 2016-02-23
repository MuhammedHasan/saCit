import urllib2
import xmltodict
import settings
import extract
from difflib import SequenceMatcher


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
    def _id_to_path(id):
        return id.replace('.', '/') + '/' + id

    @staticmethod
    def _get_text(id):
        url = settings.DATA_HOST + 'text/' + Paper._id_to_path(id) + '.txt'
        return urllib2.urlopen(url).read()

    @staticmethod
    def _get_xml(id):
        url = settings.DATA_HOST + 'xml/' + Paper._id_to_path(id) + '.xml'
        return urllib2.urlopen(url).read()

    def _get_pars(self):
        return extract.extract_all(self.text)

    @staticmethod
    def is_title_same(pars_title, xml_title):
        ''' This function check extracted title is same.
        Those title are from citeseerx and from parscit.'''
        pars_title = ''.join(e for e in pars_title if e.isalnum()).lower()
        xml_title = ''.join(e for e in xml_title if e.isalnum()).lower()
        if xml_title in pars_title or pars_title in xml_title:
            return True
        elif SequenceMatcher(None, pars_title, xml_title).ratio() > 0.6:
            return True
        return False
