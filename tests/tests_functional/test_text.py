import io
import unittest

from listmodel import TextDoc, QueryAttr

from ..utils import TestCaseMixin


class TestTextDoc(TestCaseMixin, unittest.TestCase):
    class Bookshelf(TextDoc):
        class Iterable(TextDoc):
            __query__ = "<book>(.*?)</book>"

            class Iterable(TextDoc):
                __query__ = "<chapter[^>]*>.*?</chapter>"

                id = QueryAttr('<chapter[^>]+id="([^\"]*)"')
                text = QueryAttr(">(.*)</chapter>")

            isbn = QueryAttr("<isbn>(.*?)</isbn>")
            title = QueryAttr("<title>(.*?)</title>")
            author = QueryAttr("<author>(.*?)</author>")
            revisions = QueryAttr("<rev>(\d+)</rev>")
            name_tuple = QueryAttr("<author>([^,]+),\s*(.+?)</author>")
            name_dict = QueryAttr("<author>(?P<lastname>[^,]+),\s*(?P<firstname>.+?)</author>")

            @QueryAttr("<author>(.*?)</author>")
            def author_first_name(self, value):
                return value.split(", ")[1]

            @QueryAttr("<author>(.*?)</author>")
            def author_last_name(self, value):
                return value.split(", ")[0]

        name = QueryAttr("<name>(.*?)</name>")
        undefined = QueryAttr("<undefined>(.*?)</undefined>")

    xml = u"""<bookshelf>
        <name>My Bookshelf</name>
        <book>
            <title>1984</title>
            <author>Orwell, George</author>
            <isbn>978-0-452-28423-4</isbn>
            <revisions>
                <rev>1</rev>
                <rev>2</rev>
                <rev>3</rev>
            </revisions>
            <chapter id="1">...</chapter>
            <chapter id="2">...</chapter>
            <chapter id="3">...</chapter>
        </book>
        <book>
            <title>The man in the high castle</title>
            <author>Dick, Philip K.</author>
            <isbn>0679740678</isbn>
            <chapter id="4">...</chapter>
            <chapter id="5">...</chapter>
            <chapter id="6">...</chapter>
        </book>
    </bookshelf>
    """

    def assert_shelf_is_correct(self, shelf):
        self.assertEqual(shelf.name, "My Bookshelf")
        self.assertIs(shelf.undefined, None)
        self.assertRegex(
            repr(shelf),
            r"^<Bookshelf \(({0}, {1}|({1}, {0}))\)>$".format(
                "name=u?'My Bookshelf'", "undefined=None")
        )
        self.assertEqual(repr(shelf), str(shelf))

        books = list(shelf)
        self.assertEqual(books[0].isbn, "978-0-452-28423-4")
        self.assertEqual(books[0].title, "1984")
        self.assertEqual(books[0].author, "Orwell, George")
        self.assertEqual(books[0].author_first_name, "George")
        self.assertEqual(books[0].author_last_name, "Orwell")
        self.assertEqual(list(books[0].revisions), ["1", "2", "3"])
        self.assertEqual(books[0].name_tuple, ("Orwell", "George"))
        self.assertEqual(books[0].name_dict, {"lastname": "Orwell", "firstname": "George"})
        chapters = list(books[0])
        self.assertEqual(len(chapters), 3)
        for i, chapter in enumerate(chapters, start=1):
            self.assertEqual(chapter.text, "...")
        self.assertEqual(books[1].isbn, "0679740678")
        self.assertEqual(books[1].title, "The man in the high castle")
        self.assertEqual(books[1].author, "Dick, Philip K.")
        self.assertEqual(books[1].author_first_name, "Philip K.")
        self.assertEqual(books[1].author_last_name, "Dick")
        for i, chapter in enumerate(books[1], start=4):
            self.assertEqual(chapter.id, str(i))
            self.assertEqual(chapter.text, "...")

    def test_fromfile(self):
        shelf = self.Bookshelf.fromfile(io.StringIO(self.xml))
        self.assert_shelf_is_correct(shelf)

    def test_fromstring(self):
        shelf = self.Bookshelf.fromstring(self.xml)
        self.assert_shelf_is_correct(shelf)
