from obin.runtime.exception import ObinReferenceError

class References(object):
    _virtualizable2_ = ['_refs_[*]']
    _settled_ = True

    def __init__(self, env, size):
        self._refs_ = [None] * size
        self._resizable_ = not bool(size)
        self.env = env

    def _resize_refs(self, index):
        if index >= len(self._refs_):
            self._refs_ += ([None] * (1 + index - len(self._refs_)))

    def _get_refs(self, index):
        if index > len(self._refs_):
            print
        assert index < len(self._refs_)
        assert index >= 0

        if self._resizable_:
            self._resize_refs(index)

        return self._refs_[index]

    def _set_refs(self, index, value):
        if self._resizable_:
            self._resize_refs(index)
        assert index < len(self._refs_)
        assert index >= 0
        self._refs_[index] = value

    def store_ref(self, symbol, index, value):
        ref = self._get_refs(index)

        if ref is not None:
            ref.put_value(value)
            return

        ref = self.env.get_reference(symbol)
        if not ref:
            raise ObinReferenceError("Unable to store reference", symbol, index, value)

        ref.put_value(value)
        self._set_refs(index, ref)

    def get_ref(self, symbol, index):
        ref = self._get_refs(index)

        if ref is None:
            ref = self.env.get_reference(symbol)
            if not ref:
                raise ObinReferenceError(symbol)
            self._set_refs(index, ref)

        return ref.get_value()


class Reference(object):
    _immutable_fields_ = ['env', 'name', 'index']
    _settled_ = True

    def __init__(self, env, referenced, index):
        assert env is not None
        self.env = env
        self.name = referenced
        self.index = index

    def get_value(self):
        return self.env.get_local(self.index)

    def put_value(self, value):
        self.env.set_local(self.index, value)