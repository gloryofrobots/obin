from capy.runtime.routine.routine import complete_native_routine
from capy.runtime import error
from capy.types import api, space, plist, environment

from capy.misc.strutil import encode_unicode_utf8
from capy.misc.platform import rstring, compute_unique_id
from capy.misc import fs
from capy.compile import compiler

from capy.builtins import lang_names


def put_lang_func(process, module, name, func, arity):
    name_without_prefix = name.replace(lang_names.PREFIX, "")
    api.put_native_function(process, module, unicode(name), func, arity)
    api.put_native_function(process, module, unicode(name_without_prefix), func, arity)


def setup(process, module, stdlib):
    api.put_native_function(process, module, u'eval', _eval, 1)
    api.put_native_function(process, module, u'_exit', _exit, -1)
    api.put_native_function(process, module, u'__env__', __env, 0)
    api.put_native_function(process, module, u'DMARK', __dmark, -1)
    api.put_native_function(process, module, u'PL', _print, -1)
    api.put_native_function(process, module, u'address', _id, 1)
    api.put_native_function(process, module, u'time', time, 0)
    api.put_native_function(process, module, u'symbol', _symbol, 1)
    put_lang_func(process, module, lang_names.APPLY, apply, 2)
    put_lang_func(process, module, lang_names.ENV, __env, 0)
    put_lang_func(process, module, lang_names.NOT, __not, 1)
    put_lang_func(process, module, lang_names.IS, __is, 2)
    put_lang_func(process, module, lang_names.ISNOT, __isnot, 2)
    put_lang_func(process, module, lang_names.DEFCLASS, __class, 3)
    put_lang_func(process, module, lang_names.LOAD_MODULE, load_module, 1)
    put_lang_func(process, module, u"array", __array, -1)


# 15.1.2.2

@complete_native_routine
def compile_module(process, routine):
    sourcename = routine.get_arg(0)
    modulename = routine.get_arg(1)
    parent_env = routine.get_arg(2)
    filename = api.to_s(sourcename)
    script = fs.load_file_content(filename)

    # with Timer("--- compile module  %s " % api.to_s(modulename)):
    _module = compiler.compile_env(process, parent_env, modulename, script, sourcename)

    # print("--- compile module  %s seconds %d ---" % (, (time.time() - start_time)))
    env = environment.create_environment(process, _module, parent_env)
    return env


@complete_native_routine
def _id(process, routine):
    this = routine.get_arg(0)
    return space.newstring(unicode(hex(compute_unique_id(this))))


@complete_native_routine
def _print(process, routine):
    args = routine._args.to_l()
    if len(args) == 0:
        return space.newnil()

    builder = rstring.UnicodeBuilder()
    for arg in args[:-1]:
        builder.append(api.to_u(arg))
        builder.append(u' ')

    builder.append(api.to_u(args[-1]))

    u_print_str = builder.build()
    print_str = encode_unicode_utf8(u_print_str)
    print print_str
    return space.newnil()


@complete_native_routine
def __env(process, routine):
    from capy.runtime.routine.code_routine import CodeRoutine
    prev = process.fiber.previous_routine()
    if not isinstance(prev, CodeRoutine):
        return space.newnil()

    return prev.env


# here i can put breakpoints in python debugger
# and pause script execution
@complete_native_routine
def __dmark(process, routine):
    _num = routine.get_arg(0)
    error.affirm_type(_num, space.isint)
    api.d.add_bp(api.to_i(_num))
    return space.newnil()


@complete_native_routine
def __array(process, routine):
    args = routine._args.to_l()
    return space.newarray(args)


def _exit(process, routine):
    print routine._args.to_l()
    raise SystemExit


def _eval(process, routine):
    x = routine.get_arg(0)

    assert space.issymbol(x)
    parent_env = routine.env
    src = api.to_s(x)
    source = compiler.compile_function_source(process, parent_env, src, space.newsymbol(process, u"__eval__"))
    env = space.newenv(space.newsymbol(process, u"__eval__"), source.code.scope, parent_env)

    func = space.newfunc(source.name, source.code, env)
    args = space.newnil()
    api.call(process, func, args)


def apply(process, routine):
    func = routine.get_arg(0)
    args = routine.get_arg(1)
    if space.islist(args):
        args = plist.to_tuple(args)
    elif not space.isarray(args):
        return error.throw_1(error.Errors.TYPE_ERROR, space.newstring(u"expected array"))
    api.call(process, func, args)


@complete_native_routine
def _type(process, routine):
    left = routine.get_arg(0)
    return api.get_type(process, left)


@complete_native_routine
def _symbol(process, routine):
    _str = routine.get_arg(0)
    error.affirm_type(_str, space.isstring)
    return space.newsymbol_string(process, _str)


@complete_native_routine
def __not(process, routine):
    left = routine.get_arg(0)
    error.affirm_type(left, space.isboolean)
    return api.not_(left)


@complete_native_routine
def __class(process, routine):
    name = routine.get_arg(0)
    baseclass = routine.get_arg(1)
    if space.isnil(baseclass):
        baseclass = process.std.classes.Object

    env = routine.get_arg(2)
    _class = space.newcompiledclass(name, baseclass, env)
    return _class


@complete_native_routine
def load_module(process, routine):
    from capy.runtime import load
    module_path = routine.get_arg(0)
    if space.isstring(module_path):
        module_path = space.newsymbol_string(process, module_path)

    error.affirm_type(module_path, space.issymbol)
    module = load.import_class(process, module_path)
    return module


@complete_native_routine
def time(process, routine):
    import time
    return space.newfloat(time.time())


@complete_native_routine
def __is(process, routine):
    left = routine.get_arg(0)
    right = routine.get_arg(1)
    return api.is_(left, right)


@complete_native_routine
def __isnot(process, routine):
    left = routine.get_arg(0)
    right = routine.get_arg(1)
    return api.isnot(left, right)


@complete_native_routine
def __kindof(process, routine):
    left = routine.get_arg(0)
    right = routine.get_arg(1)
    return api.kindof(process, left, right)


@complete_native_routine
def __is_implemented(process, routine):
    left = routine.get_arg(0)
    right = routine.get_arg(1)
    return api.is_implemented(process, left, right)


@complete_native_routine
def __newregister(process, routine):
    method = routine.get_arg(0)
    types = routine.get_arg(1)
    fn = routine.get_arg(2)
    method.register(process, types, fn)
    return fn

@complete_native_routine
def __newdispatch(process, routine):
    from capy.types.protocol import newmethod
    fn = routine.get_arg(0)
    indexes = routine.get_arg(1)
    error.affirm_type(fn, space.isfunction)
    return newmethod(process, fn, indexes)
