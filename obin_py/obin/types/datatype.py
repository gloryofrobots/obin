from obin.types.root import W_Hashable
from obin.types import api, space, plist, pmap
from obin.misc import platform
from obin.runtime import error


class W_Record(W_Hashable):
    def __init__(self, type, values):
        W_Hashable.__init__(self)
        self.values = values
        self.type = type

    def _dispatch_(self, process, generic):
        impl = self.type.get_method(generic)

        if space.isvoid(impl) and self.type.union is not None:
            impl = self.type.union.get_method(generic)

        return impl

    def _to_string_(self):
        res = []

        for f in self.type.fields:
            i = api.at(self.type.descriptors, f)
            v = api.at_index(self.values, api.to_i(i))
            res.append("%s = %s" % (api.to_s(f), api.to_s(v)))

        return "%s {%s}" % (api.to_s(self.type), ", ".join(res))

    def _to_repr_(self):
        res = []

        for f in self.type.fields:
            i = api.at(self.type.descriptors, f)
            v = api.at_index(self.values, api.to_i(i))
            res.append("%s = %s" % (api.to_r(f), api.to_r(v)))

        return "%s {%s}" % (api.to_r(self.type), ", ".join(res))

    def _type_(self, process):
        return self.type

    def _at_(self, name):
        if space.isint(name):
            return self._at_index_(api.to_i(name))

        idx = api.lookup(self.type.descriptors, name, space.newvoid())
        if space.isvoid(idx):
            error.throw_1(error.Errors.KEY_ERROR, name)
        return api.at(self.values, idx)

    def _at_index_(self, idx):
        # accessing protected method instead of api.at_index for avoiding multiple 0 < idx < length check
        return self.values._at_index_(idx)

    def _put_(self, name, value):
        idx = api.lookup(self.type.descriptors, name, space.newvoid())
        if space.isvoid(idx):
            error.throw_1(error.Errors.KEY_ERROR, name)

        newvalues = api.put(self.values, name, value)
        return W_Record(self.type.descriptors, newvalues)

    def _length_(self):
        return api.length(self.values)

    def _equal_(self, other):
        if not isinstance(other, W_Record):
            return False
        if not api.equal_b(self.type, other.type):
            return False
        return api.equal_b(self.values, other.values)

    def keys(self):
        return self.type.fields

    def values(self):
        return self.values

    def index_of(self, val):
        idx = self.values.index(val)
        if platform.is_absent_index(idx):
            error.throw_1(error.Errors.VALUE_ERROR, val)
        return idx


def descriptors(fields):
    d = space.newmap()
    for i in range(len(fields)):
        f = fields[i]
        d = api.put(d, f, space.newint(i))
    return d


class W_Extendable(W_Hashable):
    def __init__(self):
        W_Hashable.__init__(self)
        self.interfaces = plist.empty()
        self.methods = space.newmap()
        self.derived_generics = plist.empty()

    def is_interface_implemented(self, interface):
        return plist.contains(self.interfaces, interface)

    def add_interface(self, iface):
        self.interfaces = plist.cons(iface, self.interfaces)

    def register_derived(self, generic):
        if self.is_derived(generic):
            return error.throw_3(error.Errors.RUNTIME_ERROR,
                                 space.newstring(u"Generic has already derived"), self, generic)

        self.derived_generics = plist.cons(generic, self.derived_generics)

    def is_derived(self, generic):
        if plist.contains(self.derived_generics, generic):
            return True
        return False

    def add_method(self, generic, method):
        if self.is_generic_implemented(generic):
            if not self.is_derived(generic):
                return error.throw_2(error.Errors.IMPLEMENTATION_ERROR, self,
                                     space.newstring(u"Generic has already implemented"))

            self.remove_method(generic)
        api.put(self.methods, generic, method)

    def add_methods(self, implementations):
        for impl in implementations:
            generic = api.at_index(impl, 0)
            if self.is_generic_implemented(generic):
                if not self.is_derived(generic):
                    return error.throw_2(error.Errors.IMPLEMENTATION_ERROR, self,
                                         space.newstring(u"Generic has already implemented"))

                self.remove_method(generic)

        for impl in implementations:
            generic = api.at_index(impl, 0)
            method = api.at_index(impl, 1)
            self.add_method(generic, method)

    def is_generic_implemented(self, generic):
        return api.contains_b(self.methods, generic)

    def get_method(self, generic):
        void = space.newvoid()
        impl = api.lookup(self.methods, generic, void)
        return impl

    def remove_method(self, generic):
        api.delete(self.methods, generic)


class W_DataType(W_Extendable):
    def __init__(self, name, fields, constructor):
        W_Extendable.__init__(self)

        self.name = name
        self.fields = fields

        if plist.is_empty(self.fields):
            self.is_singleton = True
        else:
            self.is_singleton = False

        self.descriptors = descriptors(self.fields)
        self.ctor = constructor
        self.union = None

    def has_constructor(self):
        return not space.isvoid(self.ctor)

    def create_instance(self, process, env):
        undef = space.newvoid()
        values = []

        for f in self.fields:
            v = api.lookup(env, f, undef)
            if space.isvoid(v):
                error.throw_2(error.Errors.CONSTRUCTOR_ERROR,
                              space.newstring(u"Missing required field. Check recursive constructor call"), f)
            values.append(v)

        return W_Record(self, space.newpvector(values))
        # return W_Record(self, plist.plist(values))

    def _dispatch_(self, process, method):
        impl = space.newvoid()
        if self.union is not None:
            impl = self.union.get_method(method)

        if space.isvoid(impl):
            _type = api.get_type(process, self)
            impl = _type.get_method(method)

        return impl

    # TODO CREATE CALLBACK OBJECT
    def _to_routine_(self, stack, args):
        from obin.runtime.routine.routine import create_callback_routine
        routine = create_callback_routine(stack, self.create_instance, self.ctor, args)
        return routine

    def _call_(self, process, args):
        if not self.has_constructor():
            error.throw_2(error.Errors.CONSTRUCTOR_ERROR,
                          space.newstring(u"There are no constructor for type"), self)

        process.call_object(self, args)

    def _type_(self, process):
        return process.std.types.Datatype

    def _compute_hash_(self):
        return int((1 - platform.random()) * 10000000)

    def _to_string_(self):
        return api.to_s(self.name)
        # return "<trait %s>" % (api.to_s(self.name))

    def _to_repr_(self):
        return self._to_string_()

    def _equal_(self, other):
        return other is self


class W_Union(W_Extendable):
    def __init__(self, name, types):
        W_Extendable.__init__(self)
        self.name = name
        self.types_list = types
        self.types_map = space.newpmap([])
        for _t in self.types_list:
            self.types_map = api.put(self.types_map, _t.name, _t)

        self.length = api.length_i(self.types_list)

    def _at_(self, key):
        return api.at(self.types_map, key)

    def _length_(self):
        return self.length

    def has_type(self, _type):
        return plist.contains(self.types_list, _type)

    def _dispatch_(self, process, generic):
        # print "UNION DISPATCH", method
        impl = self.get_method(generic)
        # print "UNION IMPL1", impl
        if space.isvoid(impl):
            _type = self._type_(process)
            impl = _type.get_method(generic)
            # print "UNION IMPL2", impl
        return impl

    def _type_(self, process):
        return process.std.types.Union

    def _compute_hash_(self):
        return int((1 - platform.random()) * 10000000)

    def _to_string_(self):
        return "<type %s>" % api.to_s(self.name)

    def _to_repr_(self):
        return self._to_string_()

    def _equal_(self, other):
        return other is self

    def to_list(self):
        return self.types_list


def union_to_list(union):
    error.affirm_type(union, space.isunion)
    return union.to_list()


def get_union(process, w):
    if not space.isdatatype(w):
        _t = api.get_type(process, w)
    else:
        _t = w

    if _t.union is not None:
        return _t.union
    return error.throw_2(error.Errors.TYPE_ERROR, space.newstring(u"Type is not part of any union"), _t)


def record_index_of(record, obj):
    error.affirm_type(record, space.isrecord)
    return record.index_of(obj)


def record_keys(record):
    error.affirm_type(record, space.isrecord)
    return record.keys()


def record_values(record):
    error.affirm_type(record, space.isrecord)
    return record.values()


def _is_exist_implementation(method, impl):
    impl_method = api.at_index(impl, 0)
    return api.equal_b(impl_method, method)


def newtype(process, name, fields, constructor):
    _datatype = W_DataType(name, fields, constructor)
    if process.std.initialized is False:
        return _datatype

    derive_default(process, _datatype)
    return _datatype


def newunion(process, name, types):
    error.affirm_type(name, space.issymbol)
    error.affirm_type(types, space.islist)
    for _t in types:
        if _t.union is not None:
            return error.throw_3(error.Errors.TYPE_ERROR, _t, _t.union,
                                 space.newstring(u"Type already exists in union"))
    _union = W_Union(name, types)
    for _t in types:
        _t.union = _union

    if process.std.initialized is False:
        return _union
    derive_default(process, _union)
    return _union


def derive_default(process, _type):
    derived = process.std.derived.get_derived(_type)
    # print "DERIVE DEFAULT", _type, traits
    for impl in derived:
        methods = _normalise_implementations(impl)
        for pair in methods:
            generic = pair[0]
            _type.register_derived(generic)
        _type.add_methods(methods)


def _normalise_implementations(implementations):
    if space.ispmap(implementations):
        methods = plist.empty()
        for pair in implementations.to_l():
            generic = pair[0]
            method = pair[1]
            methods = plist.cons(space.newtuple([generic, method]), methods)
    elif space.istrait(implementations):
        methods = plist.empty()
        for pair in implementations.methods.to_l():
            generic = pair[0]
            method = pair[1]
            methods = plist.cons(space.newtuple([generic, method]), methods)
    elif space.islist(implementations):
        methods = implementations
    else:
        return error.throw_2(error.Errors.TYPE_ERROR,
                             space.newstring(u"Invalid trait implementation source. Expected one of Map,List,Type"),
                             implementations)
    return methods


def extend_type(_type, implementations):
    error.affirm_type(_type, space.isextendable)
    for impl in implementations:
        extend_type_with(_type, impl)

    return _type


def extend_type_with(_type, implementations):
    error.affirm_type(_type, space.isextendable)
    methods = _normalise_implementations(implementations)
    if space.isunion(_type):
        for _t in _type.types_list:
            _t.add_methods(methods)

    return _type.add_methods(methods)
