from obin.types import api


def presetup(process, module, stdlib):
    # setup_traits(process, module, stdlib)
    # setup_methods(process, module, stdlib)
    # setup_types(process, module, stdlib)
    import obin.builtins.prelude
    obin.builtins.prelude.setup(process, module, stdlib)

    # MODULES
    import obin.builtins.modules.module_core_types
    obin.builtins.modules.module_core_types.setup(process, stdlib)

    import obin.builtins.modules.module_tvar
    obin.builtins.modules.module_tvar.setup(process, stdlib)

    import obin.builtins.modules.module_list
    obin.builtins.modules.module_list.setup(process, stdlib)

    import obin.builtins.modules.module_fiber
    obin.builtins.modules.module_fiber.setup(process, stdlib)

    import obin.builtins.modules.module_bit
    obin.builtins.modules.module_bit.setup(process, stdlib)

    module.export_all()

def postsetup(process):
    from obin.builtins import hotpath as hp
    from obin.types import space
    prelude = process.modules.prelude

    _s = lambda ustr: space.newsymbol(process, ustr)
    # ---------------AUTOGENERATED---------------------
    method = api.at(prelude, _s(u"=="))
    method.set_hotpath(hp.hp_eq)
    method = api.at(prelude, _s(u"!="))
    method.set_hotpath(hp.hp_ne)
    method = api.at(prelude, _s(u"<="))
    method.set_hotpath(hp.hp_le)
    method = api.at(prelude, _s(u"negate"))
    method.set_hotpath(hp.hp_uminus)
    method = api.at(prelude, _s(u"+"))
    method.set_hotpath(hp.hp_add)
    method = api.at(prelude, _s(u"-"))
    method.set_hotpath(hp.hp_sub)
    method = api.at(prelude, _s(u"*"))
    method.set_hotpath(hp.hp_mul)
    method = api.at(prelude, _s(u"/"))
    method.set_hotpath(hp.hp_div)
    method = api.at(prelude, _s(u"mod"))
    method.set_hotpath(hp.hp_mod)
    method = api.at(prelude, _s(u"contains"))
    method.set_hotpath(hp.hp_contains)
    method = api.at(prelude, _s(u"++"))
    method.set_hotpath(hp.hp_concat)
    method = api.at(prelude, _s(u"cons"))
    method.set_hotpath(hp.hp_cons)
    method = api.at(prelude, _s(u"first"))
    method.set_hotpath(hp.hp_first)
    method = api.at(prelude, _s(u"rest"))
    method.set_hotpath(hp.hp_rest)
    method = api.at(prelude, _s(u"slice"))
    method.set_hotpath(hp.hp_slice)
    method = api.at(prelude, _s(u"take"))
    method.set_hotpath(hp.hp_take)
    method = api.at(prelude, _s(u"drop"))
    method.set_hotpath(hp.hp_drop)

def setup_traits(process, module, stdlib):
    traits = stdlib.traits
    # ---------------AUTOGENERATED---------------------
    api.put(module, traits.Any.name, traits.Any)
    api.put(module, traits.Eq.name, traits.Eq)
    api.put(module, traits.Ord.name, traits.Ord)
    api.put(module, traits.Num.name, traits.Num)
    api.put(module, traits.Collection.name, traits.Collection)
    api.put(module, traits.Seq.name, traits.Seq)
    api.put(module, traits.Callable.name, traits.Callable)
    api.put(module, traits.Indexed.name, traits.Indexed)


