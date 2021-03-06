from arza.types import space, api


def setup(process, stdlib):
    from arza.builtins import lang_names
    name = lang_names.get_lang_symbol(process, u"_types")
    _module = space.newemptyenv(name)
    setup_types(_module, stdlib.types)
    _module.export_all()
    process.modules.add_env(_module)


def setup_types(module, types):
    api.put(module, types.Any.name, types.Any)
    api.put(module, types.Abstract.name, types.Abstract)
    api.put(module, types.Record.name, types.Record)

    api.put(module, types.Error.name, types.Error)
    api.put(module, types.MatchError.name, types.MatchError)
    api.put(module, types.FunctionMatchError.name, types.FunctionMatchError)
    api.put(module, types.ExceptionMatchError.name, types.ExceptionMatchError)

    api.put(module, types.Number.name, types.Number)
    api.put(module, types.Bool.name, types.Bool)
    api.put(module, types.Char.name, types.Char)
    api.put(module, types.Int.name, types.Int)
    api.put(module, types.Float.name, types.Float)
    api.put(module, types.Symbol.name, types.Symbol)
    api.put(module, types.String.name, types.String)
    api.put(module, types.List.name, types.List)
    api.put(module, types.Vector.name, types.Vector)
    api.put(module, types.Tuple.name, types.Tuple)
    api.put(module, types.Map.name, types.Map)
    api.put(module, types.Function.name, types.Function)
    api.put(module, types.Partial.name, types.Partial)
    api.put(module, types.Generic.name, types.Generic)
    api.put(module, types.FiberChannel.name, types.FiberChannel)
    api.put(module, types.Coroutine.name, types.Coroutine)
    api.put(module, types.Interface.name, types.Interface)
    api.put(module, types.Datatype.name, types.Datatype)
    api.put(module, types.Env.name, types.Env)
    api.put(module, types.Module.name, types.Module)
    api.put(module, types.Array.name, types.Array)
    api.put(module, types.AssocArray.name, types.AssocArray)
    api.put(module, types.PID.name, types.PID)

