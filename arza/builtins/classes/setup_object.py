
from arza.types import api, space
from arza.runtime import error
from arza.runtime.routine.routine import complete_native_routine


def setup(process, stdlib):
    _class = stdlib.classes.Object
    setup_class(process, _class)

def setup_class(process, _class):
    api.put_native_function(process, _class, u'__len__', length, 1)
    api.put_native_function(process, _class, u'__is_empty__', is_empty, 1)
    api.put_native_function(process, _class, u'__put__', put, 3)
    api.put_native_function(process, _class, u'__at__', at, 2)
    api.put_native_function(process, _class, u'__elem__', elem, 2)
    api.put_native_function(process, _class, u'__del__', delete, 2)
    api.put_native_function(process, _class, u'__eq__', equal, 2)
    api.put_native_function(process, _class, u'__ne__', not_equal, 2)
    api.put_native_function(process, _class, u'__str__', to_string, 1)
    api.put_native_function(process, _class, u'__repr__', to_repr, 1)



@complete_native_routine
def length(process, routine):
    arg0 = routine.get_arg(0)

    return api.length(arg0)


@complete_native_routine
def is_empty(process, routine):
    arg0 = routine.get_arg(0)

    return api.is_empty(arg0)


@complete_native_routine
def put(process, routine):
    arg2 = routine.get_arg(2)

    arg1 = routine.get_arg(1)

    arg0 = routine.get_arg(0)

    return api.put(arg2, arg0, arg1)


@complete_native_routine
def at(process, routine):
    arg1 = routine.get_arg(1)

    arg0 = routine.get_arg(0)

    return api.at(arg1, arg0)


@complete_native_routine
def elem(process, routine):
    arg1 = routine.get_arg(1)

    arg0 = routine.get_arg(0)

    return api.contains(arg1, arg0)


@complete_native_routine
def delete(process, routine):
    arg1 = routine.get_arg(1)

    arg0 = routine.get_arg(0)

    return api.delete(arg1, arg0)


@complete_native_routine
def equal(process, routine):
    arg1 = routine.get_arg(1)

    arg0 = routine.get_arg(0)

    return api.equal(arg1, arg0)


@complete_native_routine
def not_equal(process, routine):
    arg1 = routine.get_arg(1)

    arg0 = routine.get_arg(0)

    return api.not_equal(arg1, arg0)


@complete_native_routine
def to_string(process, routine):
    arg0 = routine.get_arg(0)

    return api.to_string(arg0)


@complete_native_routine
def to_repr(process, routine):
    arg0 = routine.get_arg(0)

    return api.to_repr(arg0)
