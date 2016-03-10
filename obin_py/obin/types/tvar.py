from obin.types import api, space
from obin.types.root import W_Any
from obin.runtime import error


# TODO STM

class W_TVar(W_Any):
    def __init__(self, value):
        self.value = value

    def _to_string_(self):
        return "TVar(%s)" % api.to_s(self.value)

    def _type_(self, process):
        return process.std.types.TVar


def read(var):
    return var.value


def swap(var, value):
    var.value = value