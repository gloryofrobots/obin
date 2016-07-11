__author__ = 'gloryofrobots'
from discriminator import *
from obin.types.root import W_Any
from obin.types import space, api
from obin.runtime import error


class Argument(W_Any):
    # return new discriminator for argument or choose existed one
    def __init__(self, position):
        self.position = position

    def find_old_discriminator(self, discriminators):
        raise NotImplementedError()

    def make_discriminator(self):
        raise NotImplementedError()

    def discriminator(self, discriminators):
        d = self.find_old_discriminator(discriminators)
        if d:
            return d

        d = self.make_discriminator()
        discriminators.append(d)
        return d


class PredicateArgument(Argument):
    def __init__(self, position, predicate):
        Argument.__init__(self, position)
        self.predicate = predicate

    def find_old_discriminator(self, discriminators):
        position = self.position
        predicate = self.predicate
        for d in discriminators:
            if isinstance(d, PredicateDiscriminator) \
                    and d.position == position \
                    and d.predicate is predicate:
                return d

        return None

    def make_discriminator(self):
        return PredicateDiscriminator(self.position, self.predicate)

    def _equal_(self, other):
        if not isinstance(other, PredicateArgument):
            return False
        if other.predicate is self.predicate \
                and other.position == self.position:
            return True
        return False

    def _hash_(self):
        # TODO FIX IT. GIVE RPYTHON SOME HASH TO THINK
        return 1024 + self.position

    def __repr__(self):
        return str(self.predicate)

    def __str__(self):
        return self.__repr__()


class ArgumentAny(Argument):
    def find_old_discriminator(self, discriminators):
        position = self.position
        for d in discriminators:
            if d.__class__ is AnyDiscriminator \
                    and d.position == position:
                return d

        return None

    def make_discriminator(self):
        return AnyDiscriminator(self.position)

    def __repr__(self):
        return "Any"

    def __str__(self):
        return self.__repr__()

    def _equal_(self, other):
        if not isinstance(other, ArgumentAny):
            return False
        return self.position == other.position

    def _hash_(self):
        return 256 + self.position


class ArgumentTrait(Argument):
    def __init__(self, position, trait):
        Argument.__init__(self, position)
        self.trait = trait

    def find_old_discriminator(self, discriminators):
        position = self.position
        trait = self.trait
        for d in discriminators:

            if isinstance(d, TraitDiscriminator) \
                    and d.position == position \
                    and d.trait == trait:
                return d

        return None

    def make_discriminator(self):
        return TraitDiscriminator(self.position, self.trait)

    def _equal_(self, other):
        if other.__class__ is self.__class__ \
                and other.trait == self.trait \
                and other.position == self.position:
            return True
        return False

    def __repr__(self):
        return str(self.trait)

    def __str__(self):
        return self.__repr__()

    def _hash_(self):
        return self.trait._hash_()


class ArgumentType(Argument):
    def __init__(self, position, type):
        Argument.__init__(self, position)
        self.type = type

    def find_old_discriminator(self, discriminators):
        position = self.position
        type = self.type
        for d in discriminators:

            if isinstance(d, TypeDiscriminator) \
                    and d.position == position \
                    and d.type == type:
                return d

        return None

    def make_discriminator(self):
        return TypeDiscriminator(self.position, self.type)

    def _equal_(self, other):
        if other.__class__ is self.__class__ \
                and other.type == self.type \
                and other.position == self.position:
            return True
        return False

    def __repr__(self):
        return str(self.type)

    def __str__(self):
        return self.__repr__()

    def _hash_(self):
        return self.type._hash_()


class BaseSignature:
    def __init__(self, method):
        self.method = method

    def equal(self, other):
        raise NotImplementedError()

    def get_argument(self, index):
        raise NotImplementedError()


class Signature(BaseSignature):
    def __init__(self, args, method):
        BaseSignature.__init__(self, method)
        self.args = args
        self.arity = len(args)

    def equal(self, other):
        args1 = self.args
        args2 = other.args
        for i in range(0, len(args1)):
            arg1 = args1[i]
            arg2 = args2[i]
            if not api.equal_b(arg1, arg2):
                return False

        return True

    def get_argument(self, index):
        return self.args[index]


def _get_trait_predicate(process, trait, index):
    traits = process.std.traits

    if traits.Any is trait:
        arg = ArgumentAny(index)
    else:
        arg = ArgumentTrait(index, trait)

    return arg


def _get_type_predicate(process, _type, index):
    types = process.std.types
    if types.Map is _type:
        arg = PredicateArgument(index, space.ismap)
    elif types.Vector is _type:
        arg = PredicateArgument(index, space.isvector)
    elif types.String is _type:
        arg = PredicateArgument(index, space.isstring)
    elif types.Function is _type:
        arg = PredicateArgument(index, space.isfunction)
    elif types.Int is _type:
        arg = PredicateArgument(index, space.isint)
    elif types.Float is _type:
        arg = PredicateArgument(index, space.isfloat)
    elif types.Tuple is _type:
        arg = PredicateArgument(index, space.istuple)
    elif types.Generic is _type:
        arg = PredicateArgument(index, space.isgeneric)
    elif types.Nil is _type:
        arg = PredicateArgument(index, space.isvoid)
    elif types.Bool is _type:
        arg = PredicateArgument(index, space.isboolean)
    elif types.False is _type:
        arg = PredicateArgument(index, space.isfalse)
    elif types.True is _type:
        arg = PredicateArgument(index, space.istrue)
    else:
        arg = ArgumentType(index, _type)

    return arg


def newsignature(process, args, method):
    arity = api.length_i(args)
    sig_args = []

    for index in range(arity):
        kind = api.at_index(args, index)
        if space.istrait(kind):
            arg = _get_trait_predicate(process, kind, index)
        elif space.isdatatype(kind):
            arg = _get_type_predicate(process, kind, index)
        else:
            return error.throw_2(error.Errors.TYPE,
                                 space.newstring(u"Invalid signature type. Expected type or trait"), kind)

        sig_args.append(arg)

    return Signature(sig_args, method)


def new_base_signature(method):
    return BaseSignature(method)