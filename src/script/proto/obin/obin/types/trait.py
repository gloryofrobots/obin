from obin.types.root import W_Hashable
from obin.types import api
from obin.misc import platform


class W_Trait(W_Hashable):
    # _immutable_fields_ = ['_name_']

    def __init__(self, name):
        W_Hashable.__init__(self)
        self.name = name

    def _behavior_(self, process):
        return process.std.behaviors.Trait

    def _compute_hash_(self):
        return int((1 - platform.random()) * 10000000)

    def _to_string_(self):
        return api.to_s(self.name)
        # return "<trait %s>" % (api.to_s(self.name))

    def _equal_(self, other):
        return other is self
