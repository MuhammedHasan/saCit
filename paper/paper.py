import urllib2
import settings
import extract
from difflib import SequenceMatcher
from helper import *
from pymongo import MongoClient
import xmltodict
from textblob import TextBlob


class Paper:

    def __init__(self, id):
        collection = Paper._create_connection()
        self.mongo = collection.find_one({'@id': id})
        self.pars = xmltodict.parse(self._get_pars())

    @property
    def pars_citations(self):
        algs = self.pars['algorithms']['algorithm']
        for i in algs:
            if i.get('citationList'):
                return i['citationList']['citation']
        return list()

    @property
    def mongo_citations(self):
        if self.mongo.get('citations'):
            if self.mongo['citations'].get('citation'):
                citations = self.mongo['citations']['citation']
                return if_not_list_make_list(citations)
        return list()

    def _get_pars(self):
        return extract.extract_all(self.mongo['text'])

    @staticmethod
    def _create_connection():
        client = MongoClient(settings.MONGO_HOST_IP)
        db = client[settings.MONGO_DATABASE_NAME]
        return db[settings.MONGO_COLLECTION_NAME]

    @staticmethod
    def _cid_to_paper_id(cid):
        collection = Paper._create_connection()
        paper = collection.find_one({'clusterid': cid})
        return paper.get('@id') if paper else None

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
        for i in self.mongo_citations:
            if i.get('raw') and i.get('clusterid'):
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

    def find_all_id_of_pars_citation(self):
        id_of_pars_citation = [
            (Paper._cid_to_paper_id(k), v)
            for k, v in self.find_all_cid_of_pars_citation()
            if k or v
        ]
        return filter(lambda x: x[0] and x[1], id_of_pars_citation)

    def get_centiment_with_paperid(self):
        return [(k, Paper._calc_sent_each_context(v))
                for k, v in self.find_all_id_of_pars_citation()]

    @staticmethod
    def _calc_sent_each_context(contexts):
        return sum(
            [TextBlob(c).sentiment.polarity for c in contexts]
        ) / float(len(contexts))
