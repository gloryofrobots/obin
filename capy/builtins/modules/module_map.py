from capy.types import pmap, space, api
from capy.runtime.routine.routine import complete_native_routine
from capy.runtime import error


def setup(process, stdlib):
    _module_name = space.newsymbol(process, u'arza:lang:_map')
    _module = space.newemptyenv(_module_name)
    api.put_native_function(process, _module, u'to_list', _to_list, 1)

    _module.export_all()
    process.classes.add_env(_module)


@complete_native_routine
def _to_list(process, routine):
    arg0 = routine.get_arg(0)

    return pmap.to_list(arg0)
