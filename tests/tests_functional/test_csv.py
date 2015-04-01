import io
import unittest

from listmodel import CsvRow, QueryAttr


class TestCsvRow(unittest.TestCase):
    def test_positional(self):
        csv = u"""1,2
4,3
"""

        class MyDoc(CsvRow):
            foo = QueryAttr(0)
            bar = QueryAttr(1)

        docs = list(MyDoc.fromfile(io.StringIO(csv)))
        self.assertEqual(docs[0].foo, "1")
        self.assertEqual(docs[0].bar, "2")
        self.assertEqual(docs[1].foo, "4")
        self.assertEqual(docs[1].bar, "3")

    def test_header(self):
        csv = u"""Foo,Bar
1,2
4,3
"""

        class MyDoc(CsvRow):
            @QueryAttr("Foo")
            def foo(self, value):
                return int(value)

            bar = QueryAttr("Bar", factory=float)

        docs = list(MyDoc.fromfile(io.StringIO(csv), read_header=True))
        self.assertEqual(docs[0].foo, 1)
        self.assertEqual(docs[0].bar, 2.0)
        self.assertEqual(docs[1].foo, 4)
        self.assertEqual(docs[1].bar, 3.0)
