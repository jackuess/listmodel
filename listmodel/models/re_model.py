import re

from .._listmodel import ListModel, Role

def _get_match(match):
    try:
        return match.group(1)
    except IndexError:
        return match.group(0)
    except AttributeError:
        pass


class ReListModel(ListModel):
    def set_context(self, content):
        self.context = content
        self._rows = [_get_match(match)
                      for match
                      in re.finditer(self.__rowquery__, content, re.DOTALL)]


class ReRole(Role):
    def query(self, obj, regex):
        return _get_match(re.search(regex, obj.context, re.DOTALL))
