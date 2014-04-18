try:
    from ujson import loads
except ImportError:
    from json import loads

from jsonpath_rw import parse

from .._listmodel import ListModel, Role


class JsonListModel(ListModel):
    def set_context(self, content):
        self.context = loads(content)
        self._rows = [match.value
                      for match in parse(self.__rowquery__).find(self.context)]


class JsonRole(Role):
    def query(self, obj, jsonpath):
        try:
            return parse(jsonpath).find(obj.context)[0].value
        except IndexError:
            pass
