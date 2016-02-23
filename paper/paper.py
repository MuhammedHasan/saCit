import urllib2
import xmltodict
import settings
import extract


class Paper:

    def __init__(self, id):
        self.id = id
        self.text = Paper._get_text(id)
        self.xml = xmltodict.parse(Paper._get_xml(id))
        self.pars = xmltodict.parse(self._get_pars())

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
