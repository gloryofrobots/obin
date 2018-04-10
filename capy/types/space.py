from capy.misc.platform import jit
from capy.types.boolean import W_True, W_False
from capy.types.void import W_Void, W_Nil
from capy.types.root import W_UniqueType

w_True = W_True()
w_False = W_False()
w_Interrupt = W_UniqueType()
w_Void = W_Void()
w_Nil = W_Nil()

jit.promote(w_True)
jit.promote(w_Nil)
jit.promote(w_False)
jit.promote(w_Void)
jit.promote(w_Interrupt)


def isany(value):
    from capy.types.root import W_Root
    return isinstance(value, W_Root)


def isatomictype(value):
    return isvaluetype(value) or isstring(value)


def isvaluetype(value):
    from capy.types.root import W_ValueType
    return isinstance(value, W_ValueType)


def isuniquetype(w):
    from capy.types.root import W_UniqueType
    return isinstance(w, W_UniqueType)


########################################################

# TODO CHECK FOR BIGINT OVERFLOW
def newint(i):
    from capy.types.integer import W_Integer
    return W_Integer(i)


def isint(w):
    from capy.types.integer import W_Integer
    return isinstance(w, W_Integer)


def newfloat(f):
    assert isinstance(f, float)
    from capy.types.floating import W_Float
    return W_Float(f)


def isfloat(w):
    from capy.types.floating import W_Float
    return isinstance(w, W_Float)


def newnumber(value):
    from capy.misc.platform import rarithmetic
    if isinstance(value, float):
        return newfloat(value)
    try:
        return newint(rarithmetic.ovfcheck(value))
    except OverflowError:
        return newfloat(float(value))


def isnumber(w):
    return isint(w) or isfloat(w)


########################################################

def newchar(c):
    assert isinstance(c, unicode)
    from capy.types.character import W_Char
    return W_Char(ord(c))


def ischar(w):
    from capy.types.character import W_Char
    return isinstance(w, W_Char)


########################################################

def newstring_s(s):
    assert isinstance(s, str)
    return newstring(unicode(s))


def newstring(s):
    assert isinstance(s, unicode)
    from capy.types.string import W_String
    return W_String(s)


def isstring(w):
    from capy.types.string import W_String
    return isinstance(w, W_String)


########################################################

def newsymbol(process, s):
    assert isinstance(s, unicode)
    return process.symbols.symbol(s)


def newsymbol_s(process, s):
    assert isinstance(s, str)
    return process.symbols.symbol_s(s)


def newsymbol_string(process, s):
    assert isstring(s)
    return process.symbols.symbol_string(s)


def issymbol(w):
    from capy.types.symbol import W_Symbol
    return isinstance(w, W_Symbol)


########################################################

def newinterrupt():
    return w_Interrupt


def isinterrupt(value):
    return value is w_Interrupt


########################################################

def newvoid():
    return w_Void


def isvoid(value):
    return value is w_Void


########################################################

def newnil():
    return w_Nil


def isnil(value):
    return value is w_Nil


########################################################

def newbool(val):
    assert isinstance(val, bool)
    if val:
        return w_True
    return w_False


def isboolean(value):
    return value is w_False or value is w_True


def istrue(value):
    return value is w_True


def isfalse(value):
    return value is w_False


########################################################
def newfunc_from_source(source, env):
    return newfunc(source.name, source.code, env)


def newfunc(name, bytecode, scope):
    from capy.types.function import W_Function
    assert issymbol(name)
    obj = W_Function(name, bytecode, scope)
    return obj


def newfuncsource(name, bytecode):
    from capy.types.function import W_FunctionSource
    assert issymbol(name)
    obj = W_FunctionSource(name, bytecode)
    return obj


def newnativemethod(name, function, arity):
    from capy.types.native_function import W_NativeFunction
    assert issymbol(name)
    obj = W_NativeFunction(name, function, arity, False)
    return obj


def newnativefunc(name, function, arity):
    from capy.types.native_function import W_NativeFunction
    assert issymbol(name)
    obj = W_NativeFunction(name, function, arity, True)
    return obj


def isfunction(value):
    from capy.types.function import W_Function
    from capy.types.native_function import W_NativeFunction
    return isinstance(value, W_Function) or isinstance(value, W_NativeFunction)


def isnativefunction(value):
    from capy.types.native_function import W_NativeFunction
    return isinstance(value, W_NativeFunction)


########################################################


def newiodevice(_file):
    from capy.types.iodevice import W_IODevice
    return W_IODevice(_file)


def isiodevice(w):
    from capy.types.iodevice import W_IODevice
    return isinstance(w, W_IODevice)


########################################################

def newtable(args):
    from capy.types.table import create_assoc_array
    return create_assoc_array(args)


def newemptytable():
    from capy.types.table import create_empty_assoc_array
    return create_empty_assoc_array()


def istable(value):
    from capy.types.table import W_Table
    return isinstance(value, W_Table)


########################################################

def newemptyarray():
    return newarray([])


def newarray(items):
    assert isinstance(items, list)
    verify_list_DEBUG(items)
    from capy.types.array import W_Array
    obj = W_Array(items)
    return obj


def isarray(value):
    from capy.types.array import W_Array
    return isinstance(value, W_Array)


########################################################

def newlist(items):
    from capy.types.plist import plist
    verify_list_DEBUG(items)
    return plist(items)


def islist(value):
    from capy.types.plist import W_PList
    return isinstance(value, W_PList)


def verify_list_DEBUG(items):
    for i in items:
        assert isany(i), i


########################################################


def newarguments(stack, index, length):
    from capy.types.arguments import W_Arguments
    return W_Arguments(stack, index, length)


def isarguments(w):
    from capy.types.arguments import W_Arguments
    return isinstance(w, W_Arguments)


#########################################################

def newscope():
    from capy.types.scope import W_Scope
    return W_Scope()


def isscope(w):
    from capy.types.scope import W_Scope
    return isinstance(w, W_Scope)


########################################################

def newenvsource(name, code):
    assert name is None or issymbol(name)
    from capy.types.environment import W_EnvSource
    obj = W_EnvSource(name, code)
    return obj


def newenv(name, scope, outer_environment):
    from capy.types.environment import W_Env
    env = W_Env(name, scope, outer_environment)
    return env


def newemptyenv(name):
    return newenv(name, newscope().finalize(None, None), None)


def isenv(w):
    from capy.types.environment import W_Env
    return isinstance(w, W_Env)


########################################################

def newclass(name, base, slots):
    from capy.types.objects import newclass
    return newclass(name, base, slots)


def newemptyclass(name, base):
    return newclass(name, base, newemptytable())


def newcompiledclass(name, base, env):
    from capy.types.objects import newcompiledclass
    return newcompiledclass(name, base, env)


def isclass(_class):
    from capy.types.objects import W_Class
    return isinstance(_class, W_Class)


def isobject(_obj):
    from capy.types.objects import W_Object
    return isinstance(_obj, W_Object)


########################################################

def isoperator(w):
    from capy.compile.parse.basic import W_Operator
    return isinstance(w, W_Operator)


############################################################

def newcoroutine(process, fn):
    from capy.types.coroutine import newcoroutine
    assert isfunction(fn)
    return newcoroutine(process, fn)


def iscoroutine(co):
    from capy.types.coroutine import W_Coroutine
    return isinstance(co, W_Coroutine)


############################################################

def newpid(process):
    from capy.types import pid
    return pid.newpid(process)


def ispid(value):
    from capy.types.pid import W_PID
    return isinstance(value, W_PID)


############################################################

def safe_w(obj):
    if not isany(obj):
        s = "<PyObj type:%s, repr:%s>" % (type(obj), repr(obj))
        return newstring_s(s)
    return obj