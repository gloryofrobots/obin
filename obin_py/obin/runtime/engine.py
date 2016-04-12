from obin.types import space, api
from obin.builtins import builtins
from obin.runtime.process import Process
from obin.runtime import process_data, error
from obin.runtime.load import import_module, evaluate_module_file

PRELUDE_FILE = u"prelude"
# PRELUDE_FILE = u"prelude_test"
# PRELUDE_FILE = u"syntax"
# PRELUDE_FILE = u"affirm"

def newprocess(libdirs):
    core_prelude = space.newemptyenv(space.newstring(u"prelude"))
    proc_data = process_data.create(libdirs, core_prelude)
    process = Process(proc_data)
    builtins.presetup(process, core_prelude, process.std)
    return process


def load_prelude(process, script_name):
    result = import_module(process, space.newsymbol(process, script_name))
    if process.is_terminated():
        # error here
        return result

    process.modules.set_prelude(result)
    return None


def load_module(process, script_name):
    result = import_module(process, space.newsymbol(process, script_name))
    if process.is_terminated():
        # error here
        return result
    return None


# TODO MOVE ALL OF IT TO PROCESS
def initialize(libdirs):
    path = space.newlist([space.newstring_s(p) for p in libdirs])

    process = newprocess(path)
    err = load_prelude(process, PRELUDE_FILE)
    if err is not None:
        return process, err

    process.std.postsetup(process)
    builtins.postsetup(process)
    error.initialise(process)

    modules = [u"err", u"bool", u"int", u"bit", u"float",
               u"string", u"symbol",
               u"list",
               u"tuple", u"map", u"seq", u"lazy"]
    for module_name in modules:
        err = load_module(process, module_name)
        if err is not None:
            return process, err


    print "INITIALIZED"
    return process, None


def evaluate_file(process, filename):
    try:
        module = evaluate_module_file(process, space.newsymbol(process, u"__main__"), filename)
    except error.ObinSignal as e:
        return e.signal

    main = api.at(module, space.newsymbol(process, u"main"))
    result = process.subprocess(main, space.newtuple([space.newunit()]))

    if process.is_terminated():
        # error here
        return result

    return space.newtuple([space.newsymbol(process, u"ok"), result])
