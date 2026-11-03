import unittest
from urllib.parse import parse_qs, urlsplit

from search_url import build_search_url


class SearchUrlTests(unittest.TestCase):
    def setUp(self):
        self.url = build_search_url(3, ["saldırı", "şiddet"], "or", "01/01/2016", "31/12/2016", "gundem")
        fragment = urlsplit(self.url).fragment
        self.assertTrue(fragment.startswith("/?"))
        self.query = parse_qs(fragment[2:])

    def test_order_and_where_are_separate_parameters(self):
        self.assertEqual(self.query["order"], ["Yeniden Eskiye"])
        self.assertEqual(self.query["where"], ["hurriyet"])

    def test_search_parameters_are_preserved(self):
        expected = {
            "page": ["3"], "key": ["saldırı şiddet"], "how": ["Article"], "or": ["saldırı şiddet"],
            "startDate": ["01/01/2016"], "finishDate": ["31/12/2016"], "platform": ["hurriyet"],
            "mainCategory": ["/gundem/"], "isDetail": ["true"],
        }
        for key, value in expected.items():
            with self.subTest(key=key):
                self.assertEqual(self.query[key], value)
        self.assertEqual(set(self.query), set(expected) | {"order", "where"})


if __name__ == "__main__":
    unittest.main()
