import urllib2
import xmltodict


class Paper:

    def __init__(self, id):
        self.text = Paper.get_text()
        self.xml = Paper.get_xml()
        self.pars = Paper.get_pars()

    @staticmethod
    def _id_to_path(id):
        return id.replace('.', '/') + '/' + id

    @staticmethod
    def _get_text(id):
        pass

    @staticmethod
    def _get_xml(id):
        pass

    @staticmethod
    def _get_pars(id):
        pass
