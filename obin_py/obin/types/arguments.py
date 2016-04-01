from obin.types.root import W_Hashable, W_Root
from sequence import W_SequenceIterator
from obin.runtime import error
from obin.runtime.stack import Stack
from obin.types import api, space, plist
from obin.misc import platform


class W_Arguments(W_Root):
    def __init__(self, stack, pointer, length):
        assert isinstance(length, int)
        assert length >= 0
        assert length < stack.size()
        assert isinstance(stack, Stack)

        assert isinstance(pointer, int)
        assert pointer > 0
        assert pointer <= stack.pointer()
        self.pointer = pointer
        self.start = pointer - length
        self.stack = stack
        self.length = length

    def to_l(self):
        l = [self.get(i) for i in range(self.length)]
        return l

    def get(self, i):
        index = self.start + i
        return self.stack.get(index)

    def _type_(self, process):
        return process.std.types.Tuple

    def _contains_(self, obj):
        i = self._get_index_(obj)
        return platform.is_absent_index(i)

    def _at_(self, index):
        from obin.types.space import newvoid, isint
        assert isint(index)
        i = api.to_i(index)
        if i < 0 or i > self.length - 1:
            return newvoid()

        return self.get(i)


    def _at_index_(self, i):
        return self.get(i)

    def _get_index_(self, obj):
        for i in range(self.length):
            item = self.get(i)
            if api.equal_b(item, obj):
                return i
        return platform.absent_index()

    def _iterator_(self):
        return W_SequenceIterator(self)

    def _length_(self):
        return self.length

    def _equal_(self, other):
        from obin.types import space
        if not space.is_tuple_or_arguments(other):
            return False

        if self._length_() != other._length_():
            return False

        for el1, el2 in zip(self.to_l(), other.to_l()):
            if not api.equal_b(el1, el2):
                return False

        return True

    def _to_string_(self):
        repr = ", ".join([v._to_string_() for v in self.to_l()])
        return "{> %s <}" % repr


def type_check(t):
    error.affirm_type(t, space.isarguments)


def to_list(t):
    type_check(t)
    return space.newlist(t.elements)


def drop(t, count):
    error.affirm_type(t, space.isarguments)
    assert isinstance(count, int)
    if count == 0:
        return space.newtuple(t.to_l())

    if count >= t.length:
        error.throw_2(error.Errors.SLICE_ERROR, space.newstring(u"Can not drop so much items"), space.newint(count))

    return space.newtuple(t.to_l()[count:t.length])
    # return W_Arguments(t.stack, t.pointer - count + 1, t.length - count)
