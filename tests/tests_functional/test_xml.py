import io
import unittest

from listmodel import XMLDoc, QueryAttr


class TestXMLDoc(unittest.TestCase):
    if not hasattr(unittest.TestCase, "assertRegex"):
        assertRegex = unittest.TestCase.assertRegexpMatches

    class Bookshelf(XMLDoc):
        class Iterable(XMLDoc):
            __name__ = "Book"
            __query__ = "/bookshelf/book"

            class Iterable(XMLDoc):
                __query__ = "chapter"

                id = QueryAttr("@id")
                text = QueryAttr("text()")

            isbn = QueryAttr("isbn/text()")
            title = QueryAttr("title/text()")
            author = QueryAttr("author/text()")

            @QueryAttr("author/text()")
            def author_first_name(self, value):
                return value.split(", ")[1]

            @QueryAttr("author/text()")
            def author_last_name(self, value):
                return value.split(", ")[0]

        name = QueryAttr("/bookshelf/name/text()")
        undefined = QueryAttr("/bookshelf/undefined/text()")

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
                "name='My Bookshelf'", "undefined=None")
        )
        self.assertEqual(repr(shelf), str(shelf))

        books = list(shelf)
        self.assertEqual(books[0].isbn, "978-0-452-28423-4")
        self.assertEqual(books[0].title, "1984")
        self.assertEqual(books[0].author, "Orwell, George")
        self.assertEqual(books[0].author_first_name, "George")
        self.assertEqual(books[0].author_last_name, "Orwell")
        for i, chapter in enumerate(books[0], start=1):
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
