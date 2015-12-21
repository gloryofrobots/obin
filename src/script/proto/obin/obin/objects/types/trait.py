from root import W_Cell
from obin.runtime.exception import *
from obin.objects import api


class W_Trait(W_Cell):
    _type_ = 'Trait'
    _immutable_fields_ = ['_type_']

    def __init__(self, name):
        super(W_Cell, self).__init__()
        self._name_ = name
        self.__id = int(id(self))

    def _totrait_(self):
        return self

    def _tostring_(self):
        return u"<trait %s>" % (self._name_.value())

    def __hash__(self):
        return self.__id

    def __eq__(self, other):
        return other.__id == self.__id