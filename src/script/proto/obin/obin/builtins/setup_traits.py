from obin.types import api

def setup(process, module, stdlib):
    traits = stdlib.traits
    api.put(module, traits.Any.name, traits.Any)
    api.put(module, traits.Boolean.name, traits.Boolean)
    api.put(module, traits.True.name, traits.True)
    api.put(module, traits.False.name, traits.False)
    api.put(module, traits.Nil.name, traits.Nil)
    api.put(module, traits.Undefined.name, traits.Undefined)
    api.put(module, traits.Char.name, traits.Char)
    api.put(module, traits.Number.name, traits.Number)
    api.put(module, traits.Integer.name, traits.Integer)
    api.put(module, traits.Float.name, traits.Float)
    api.put(module, traits.Symbol.name, traits.Symbol)
    api.put(module, traits.String.name, traits.String)
    api.put(module, traits.Enumerable.name, traits.Enumerable)
    api.put(module, traits.Collection.name, traits.Collection)
    api.put(module, traits.List.name, traits.List)
    api.put(module, traits.Vector.name, traits.Vector)
    api.put(module, traits.Tuple.name, traits.Tuple)
    api.put(module, traits.Map.name, traits.Map)
    api.put(module, traits.Callable.name, traits.Callable)
    api.put(module, traits.Function.name, traits.Function)
    api.put(module, traits.Fiber.name, traits.Fiber)
    api.put(module, traits.Generic.name, traits.Generic)
    api.put(module, traits.Primitive.name, traits.Primitive)
    api.put(module, traits.Environment.name, traits.Environment)
    api.put(module, traits.TVar.name, traits.TVar)
    api.put(module, traits.Module.name, traits.Module)
    api.put(module, traits.Behavior.name, traits.Behavior)
    api.put(module, traits.Trait.name, traits.Trait)


