import unittest
from paper import Paper
import settings
from pymongo import MongoClient


class TestPaperStaticMethods(unittest.TestCase):

    def test__create_connetion(self):
        collection = Paper._create_connection()
        self.assertIsNotNone(collection)

    def test__is_citation_same(self):
        self.assertEqual(Paper.is_citation_same(
            'asd asd asd', 'asd asd asd'), 1)
        self.assertEqual(Paper.is_citation_same('a!!.,,.s!!!..d', 'asd'), 1)

    def test__cid_to_paper_id(self):
        self.assertEqual(Paper._cid_to_paper_id('95209'), '10.1.1.1.8671')


class TestPaper(unittest.TestCase):

    def setUp(self):
        self.paper = Paper('10.1.1.1.1577')

    def test__get_pars(self):
        # TODO : Most logical test ever seen
        self.assertIsNotNone(self.paper._get_pars())

if __name__ == '__main__':
    unittest.main()
