from cStringIO import StringIO

from lxml import etree

from .._listmodel import ListModel, Role


class XmlListModel(ListModel):
    __parsercls__ = etree.XMLParser
    __parseropts__ = {}

    def set_context(self, content):
        self.context = etree.parse(StringIO(content),
                                   self.__parsercls__(**self.__parseropts__))
        self._rows = self.context.xpath(self.__rowquery__)


class XmlRole(Role):
    def query(self, obj, xpath):
        if xpath.startswith('//'):
            xpath = '.' + xpath

        try:
            return obj.context.xpath(xpath)[0]
        except IndexError:
            pass


class HtmlListModel(XmlListModel):
    __parsercls__ = etree.HTMLParser


class HtmlRole(XmlRole):
    pass
