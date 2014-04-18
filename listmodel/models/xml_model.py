from cStringIO import StringIO
import types

from lxml import etree
import requests

from .._listmodel import ListModel, Role


class XmlListModel(ListModel):
    def __init__(self, source):
        try:
            content = requests.get(source).content
        except requests.exceptions.MissingSchema:
            content = source
        finally:
            context = etree.parse(StringIO(content))
            self._curr_row = 0
            self._rows = context.xpath(self.__rowquery__)
            super(XmlListModel, self).__init__(context)

class XmlRole(Role):
    def __init__(self, xpath=None, fget=None):
        if type(xpath) is types.FunctionType:
            self.xpath = None
            self.fget = xpath
        else:
            self.xpath = xpath
            self.fget = fget

    def __call__(self, fget=None):
        self.fget = fget
        return self

    def __get__(self, obj, objtype):
        val = None
        if self.xpath is not None:
            try:
                val = obj.context.xpath(self.xpath)[0]
            except IndexError:
                pass
        if self.fget is not None:
            val = self.fget(obj, val)
        return val
