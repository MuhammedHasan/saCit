import unittest
from paper import Paper


class TestPaperStaticMethods(unittest.TestCase):

    def setUp(self):
        self.id = '10.1.1.582.1'

    def test__file_id_to_location(self):
        location = Paper._id_to_path(self.id)
        self.assertEqual(location, '10/1/1/582/1/10.1.1.582.1')

if __name__ == '__main__':
    unittest.main()
