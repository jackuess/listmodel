from cStringIO import StringIO
import types

from lxml import etree
import requests


class Role(object):
    def __init__(self, val):
        self.val = val

    def __get__(self, obj, objtype):
        if type(self.val) is types.FunctionType:
            return self.val(obj)
        else:
            return self.val


class ContextMeta(type):
    def __new__(cls, name, bases, dct):
        roles = [name_ for name_, value in dct.iteritems()
                 if isinstance(value, Role)]
        dct['_roles'] = roles
        return type.__new__(cls, name, bases, dct)


class ContextHolder(object):
    __metaclass__ = ContextMeta

    def __init__(self, context):
        self.context = context

    def __repr__(self):
        fields = ', '.join(['%s=%r' % (role, getattr(self, role))
                           for role in self._roles])
        return '<%s (%s)>' % (self.__class__.__name__, fields)


class XmlListModel(ContextHolder):
    def __init__(self, source):
        try:
            content = requests.get(source).content
        except requests.exceptions.MissingSchema:
            content = source
        finally:
            context = etree.parse(StringIO(content))
            self._curr_row = 0
            self._rows = context.xpath(self.__query__)
            super(XmlListModel, self).__init__(context)

    def __iter__(self):
        return self

    def next(self):
        try:
            row = self._rows[self._curr_row]
        except IndexError:
            raise StopIteration
        else:
            self._curr_row += 1
            return self.__rowhandler__(context=row)

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


class Row(ContextHolder):
    pass
