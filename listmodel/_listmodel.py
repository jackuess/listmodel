import json
import types


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

    def dict(self):
        return {role: getattr(self, role) for role in self._roles}

    def json(self):
        return json.dumps(self.dict())


class ListModel(ContextHolder):
    def __iter__(self):
        return self

    def next(self):
        try:
            row = self._rows[self._curr_row]
        except IndexError:
            raise StopIteration
        else:
            self._curr_row += 1
            return self.__rowcls__(context=row)

    def saverows(self):
        for count, row in enumerate(self._rows, start=1):
            self.__rowcls__(context=row).save()
        return count


class Row(ContextHolder):
    pass
