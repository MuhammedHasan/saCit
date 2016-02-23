import unittest
from paper import Paper


class TestPaperStaticMethods(unittest.TestCase):

    def setUp(self):
        self.id = '10.1.1.1.1483'

    def test__file_id_to_location(self):
        location = Paper._id_to_path(self.id)
        self.assertEqual(location, '10/1/1/1/1483/10.1.1.1.1483')

    def test__get_text(self):
        self.assertIsNotNone(Paper._get_text(self.id))

    def test__get_xml(self):
        self.assertIsNotNone(Paper._get_xml(self.id))

    def test__is_title_same(self):
        self.assertTrue(Paper.is_title_same('asd asd asd', 'asd asd asd'))
        self.assertTrue(Paper.is_title_same('a!!.,,.s!!!..d', 'asd'))


class TestPaper(unittest.TestCase):

    def setUp(self):
        self.paper = Paper('10.1.1.1.1483')

    def test__get_pars(self):
        # TODO : Most logical test ever seen
        self.assertIsNotNone(self.paper._get_pars())

if __name__ == '__main__':
    unittest.main()
