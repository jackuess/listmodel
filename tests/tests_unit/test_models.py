import unittest

from listmodel import QueryAttr


class TestQueryAttr(unittest.TestCase):
    def setUp(self):
        class DocumentProxy(object):
            def execute_query(self, query):
                if query == "bar":
                    return "foobar"
                else:
                    return "nobar"

        class Data(object):
            pass
        self.Data = Data
        self.Data.__document__ = DocumentProxy()

    def test_should_return_query_of_obj(self):
        self.Data.foo = QueryAttr("bar")

        self.assertEqual(self.Data().foo, "foobar")

    def test_should_return_return_of_decorated_function(self):
        def foo(self, value):
            return value.upper()
        self.Data.foo = QueryAttr("bar")(foo)

        self.assertEqual(self.Data().foo, "FOOBAR")
