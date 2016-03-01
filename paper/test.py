import unittest
from paper import Paper
import settings
from crawler import *


class TestPaperStaticMethods(unittest.TestCase):

    def setUp(self):
        self.id = '10.1.1.1.1483'

    def test__file_id_to_location(self):
        settings.DATA_HOST = 'http://10.100.8.89/'
        location = Paper._id_to_path(self.id, 'text')
        self.assertEqual(location, 'http://10.100.8.89/text/10/1/1/1/1483/')
        location = Paper._id_to_path(self.id, 'xml')
        self.assertEqual(location, 'http://10.100.8.89/xml/10/1/1/1/1483/')

    def test__get_text(self):
        self.assertIsNotNone(Paper._get_text(self.id))

    def test__get_xml(self):
        self.assertIsNotNone(Paper._get_xml(self.id))

    def test__is_citation_same(self):
        self.assertEqual(Paper.is_citation_same(
            'asd asd asd', 'asd asd asd'), 1)
        self.assertEqual(Paper.is_citation_same('a!!.,,.s!!!..d', 'asd'), 1)


class TestPaper(unittest.TestCase):

    def setUp(self):
        self.paper = Paper('10.1.1.128.9172')

    def test__get_pars(self):
        # TODO : Most logical test ever seen
        self.assertIsNotNone(self.paper._get_pars())


class TestCrawler(unittest.TestCase):

    def test_cid_to_paperid(self):
        self.assertEqual(cid_to_paperid(595), '10.1.1.13.9939')
        self.assertEqual(cid_to_paperid(578), '10.1.1.137.3147')
        self.assertIsNone(cid_to_paperid(579), None)
        self.assertIsNone(cid_to_paperid(0), None)
        self.assertIsNone(cid_to_paperid(600), None)

    def test_cids_to_paperids(self):
        self.assertEqual(
            cids_to_paperids([595, 578, 579]),
            ['10.1.1.13.9939', '10.1.1.137.3147', None]
        )

if __name__ == '__main__':
    unittest.main()
