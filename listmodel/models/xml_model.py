from cStringIO import StringIO

from lxml import etree

from .._listmodel import ListModel, Role


class XmlListModel(ListModel):
    def set_context(self, content):
        self.context = etree.parse(StringIO(content))
        self._rows = self.context.xpath(self.__rowquery__)


class XmlRole(Role):
    def query(self, obj, xpath):
        try:
            return obj.context.xpath(xpath)[0]
        except IndexError:
            pass
