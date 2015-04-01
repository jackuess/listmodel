import io
import unittest

from listmodel import JSONDoc, QueryAttr, YAMLDoc


class TestJSONDoc(unittest.TestCase):
    def setUp(self):
        class Bookshelf(JSONDoc):
            class Iterable(YAMLDoc):
                __query__ = "$.books"

                isbn = QueryAttr("$.isbn")
                title = QueryAttr("$.title")
                author = QueryAttr("$.author")

                @QueryAttr("$.author")
                def author_first_name(self, value):
                    return value.split(", ")[1]

                @QueryAttr("$.author")
                def author_last_name(self, value):
                    return value.split(", ")[0]

            name = QueryAttr("$.name")
            undefined = QueryAttr("$.undefined")
        self.Bookshelf = Bookshelf

        self.json = u"""{
            "name": "My Bookshelf",
            "books": [{
                "title": "1984",
                "author": "Orwell, George",
                "isbn": "978-0-452-28423-4"
            }, {
                "title": "The man in the high castle",
                "author": "Dick, Philip K.",
                "isbn": "0679740678"
            }]
        }
        """

    def assert_shelf_is_correct(self, shelf):
        self.assertEqual(shelf.name, "My Bookshelf")
        self.assertIs(shelf.undefined, None)

        books = list(shelf)
        self.assertEqual(books[0].isbn, "978-0-452-28423-4")
        self.assertEqual(books[0].title, "1984")
        self.assertEqual(books[0].author, "Orwell, George")
        self.assertEqual(books[0].author_first_name, "George")
        self.assertEqual(books[0].author_last_name, "Orwell")
        self.assertEqual(books[1].isbn, "0679740678")
        self.assertEqual(books[1].title, "The man in the high castle")
        self.assertEqual(books[1].author, "Dick, Philip K.")
        self.assertEqual(books[1].author_first_name, "Philip K.")
        self.assertEqual(books[1].author_last_name, "Dick")

    def test_fromfile(self):
        shelf = self.Bookshelf.fromfile(io.StringIO(self.json))
        self.assert_shelf_is_correct(shelf)

    def test_fromstring(self):
        shelf = self.Bookshelf.fromstring(self.json)
        self.assert_shelf_is_correct(shelf)


class TestYAMLDoc(unittest.TestCase):
    def setUp(self):
        class Bookshelf(YAMLDoc):
            class Iterable(YAMLDoc):
                __query__ = "$.books"

                isbn = QueryAttr("$.isbn")
                title = QueryAttr("$.title")
                author = QueryAttr("$.author")

                @QueryAttr("$.author")
                def author_first_name(self, value):
                    return value.split(", ")[1]

                @QueryAttr("$.author")
                def author_last_name(self, value):
                    return value.split(", ")[0]

            name = QueryAttr("$.name")
            undefined = QueryAttr("$.undefined")
        self.Bookshelf = Bookshelf

        self.yaml = u"""
            name: My Bookshelf
            books:
                - title: "1984"
                  author: "Orwell, George"
                  isbn: 978-0-452-28423-4
                - title: The man in the high castle
                  author: "Dick, Philip K."
                  isbn: 0679740678
        """

    def assert_shelf_is_correct(self, shelf):
        self.assertEqual(shelf.name, "My Bookshelf")
        self.assertIs(shelf.undefined, None)

        books = list(shelf)
        self.assertEqual(books[0].isbn, "978-0-452-28423-4")
        self.assertEqual(books[0].title, "1984")
        self.assertEqual(books[0].author, "Orwell, George")
        self.assertEqual(books[0].author_first_name, "George")
        self.assertEqual(books[0].author_last_name, "Orwell")
        self.assertEqual(books[1].isbn, "0679740678")
        self.assertEqual(books[1].title, "The man in the high castle")
        self.assertEqual(books[1].author, "Dick, Philip K.")
        self.assertEqual(books[1].author_first_name, "Philip K.")
        self.assertEqual(books[1].author_last_name, "Dick")

    def test_fromfile(self):
        shelf = self.Bookshelf.fromfile(io.StringIO(self.yaml))
        self.assert_shelf_is_correct(shelf)

    def test_fromstring(self):
        shelf = self.Bookshelf.fromstring(self.yaml)
        self.assert_shelf_is_correct(shelf)
