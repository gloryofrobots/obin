class Generics:
    def __init__(self):
        from obin.objects.space import newgeneric, newstring

        ## AUTOGENERATED generic_gen.py
        self.Add = newgeneric(newstring(u"+"))
        self.Sub = newgeneric(newstring(u"-"))
        self.Mul = newgeneric(newstring(u"*"))
        self.Div = newgeneric(newstring(u"/"))
        self.Mod = newgeneric(newstring(u"%"))
        self.UnaryPlus = newgeneric(newstring(u"__unary_plus__"))
        self.UnaryMinus = newgeneric(newstring(u"__unary_minus__"))
        self.Not = newgeneric(newstring(u"not"))
        self.Equal = newgeneric(newstring(u"=="))
        self.NotEqual = newgeneric(newstring(u"!="))
        self.Compare = newgeneric(newstring(u"compare"))
        self.In = newgeneric(newstring(u"contains"))
        self.GreaterThen = newgeneric(newstring(u">"))
        self.GreaterEqual = newgeneric(newstring(u">="))
        self.BitNot = newgeneric(newstring(u"!"))
        self.BitOr = newgeneric(newstring(u"^"))
        self.BitXor = newgeneric(newstring(u"~"))
        self.BitAnd = newgeneric(newstring(u"&"))
        self.LeftShift = newgeneric(newstring(u"<<"))
        self.RightShift = newgeneric(newstring(u">>"))
        self.UnsignedRightShift = newgeneric(newstring(u">>>"))

        self.Len = newgeneric(newstring(u"len"))
        self.Str = newgeneric(newstring(u"str"))
        self.List = newgeneric(newstring(u"list"))


class Behaviors:
    def __init__(self, traits):
        self.create_builtins(traits)
        # from obin.objects.space import newmap
        # self.behaviors = newmap()
        # self.create_cache = newmap()
        # self.attach_cache = newmap()
        # self.detach_cache = newmap()

    def create_builtins(self, traits):
        from obin.objects.space import newlist, newbehavior
        self.True = newbehavior(newlist([traits.True, traits.Boolean, traits.Any]))
        self.False = newbehavior(newlist([traits.False, traits.Boolean, traits.Any]))
        self.Nil = newbehavior(newlist([traits.Nil, traits.Any]))
        self.Undefined = newbehavior(newlist([traits.Undefined, traits.Any]))
        self.Char = newbehavior(newlist([traits.Char, traits.Any]))
        self.Integer = newbehavior(newlist([traits.Integer, traits.Number, traits.Any]))
        self.Float = newbehavior(newlist([traits.Float, traits.Number, traits.Any]))
        self.Symbol = newbehavior(newlist([traits.Symbol, traits.Callable, traits.Any]))

        self.String = newbehavior(newlist([traits.String, traits.Enumerable, traits.Collection, traits.Any]))
        self.List = newbehavior(newlist([traits.List, traits.Enumerable, traits.Collection, traits.Any]))
        self.Vector = newbehavior(newlist([traits.Vector, traits.Enumerable, traits.Collection, traits.Any]))
        self.Tuple = newbehavior(newlist([traits.Tuple, traits.Enumerable, traits.Collection, traits.Any]))
        self.Map = newbehavior(newlist([traits.Map, traits.Enumerable, traits.Collection, traits.Any]))

        self.Function = newbehavior(newlist([traits.Function, traits.Callable, traits.Any]))
        self.Origin = newbehavior(newlist([traits.Origin, traits.Function, traits.Callable, traits.Any]))
        self.Fiber = newbehavior(newlist([traits.Fiber, traits.Callable, traits.Any]))
        self.Generic = newbehavior(newlist([traits.Generic, traits.Callable, traits.Any]))
        self.Primitive = newbehavior(newlist([traits.Primitive, traits.Callable, traits.Any]))

        self.Module = newbehavior(newlist([traits.Module, traits.Collection, traits.Any]))
        self.Behavior = newbehavior(newlist([traits.Behavior, traits.Any]))


class Traits:
    def __init__(self):
        from obin.objects.space import newtrait, newstring
        self.Any = newtrait(newstring(u"Any"))
        self.Boolean = newtrait(newstring(u"Boolean"))
        self.True = newtrait(newstring(u"True"))
        self.False = newtrait(newstring(u"False"))
        self.Nil = newtrait(newstring(u"Nil"))
        self.Undefined = newtrait(newstring(u"Undefined"))
        self.Char = newtrait(newstring(u"Char"))
        self.Number = newtrait(newstring(u"Number"))
        self.Integer = newtrait(newstring(u"Integer"))
        self.Float = newtrait(newstring(u"Float"))
        self.Symbol = newtrait(newstring(u"Symbol"))
        self.String = newtrait(newstring(u"String"))
        self.Enumerable = newtrait(newstring(u"Enumerable"))
        self.Collection = newtrait(newstring(u"Collection"))
        self.List = newtrait(newstring(u"List"))
        self.Vector = newtrait(newstring(u"Vector"))
        self.Tuple = newtrait(newstring(u"Tuple"))
        self.Map = newtrait(newstring(u"Map"))
        self.Callable = newtrait(newstring(u"Callable"))
        self.Function = newtrait(newstring(u"Function"))
        self.Origin = newtrait(newstring(u"Origin"))
        self.Fiber = newtrait(newstring(u"Fiber"))
        self.Generic = newtrait(newstring(u"Generic"))
        self.Primitive = newtrait(newstring(u"Primitive"))
        self.Module = newtrait(newstring(u"Module"))
        self.Behavior = newtrait(newstring(u"Behavior"))

class Std:
    def __init__(self):
        self.traits = Traits()
        self.behaviors = Behaviors(self.traits)
        self.generics = Generics()

