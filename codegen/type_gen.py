from tpl import render

def mktype(name, super="self.Any"):
    t = dict(name=name, super=super)
    return t

TYPES = [
    mktype("Any", "space.newunit()"),
    mktype("Abstract"),
    mktype("Record"),
    mktype("Number"),
    mktype("Bool"),
    mktype("Char"),
    mktype("Int", "self.Number"),
    mktype("Float", "self.Number"),
    mktype("Symbol"),
    mktype("String"),
    mktype("List"),
    mktype("Vector"),
    mktype("Tuple"),
    mktype("Map"),
    mktype("Function"),
    mktype("Partial"),
    mktype("Generic"),
    mktype("FiberChannel"),
    mktype("Coroutine"),
    mktype("Interface"),
    mktype("Datatype"),
    mktype("Env"),

    mktype("Array"),
    mktype("AssocArray"),
]

def gen_declaration():
    import sys
    p = sys.stdout.write
    print "    # ---------------AUTOGENERATED---------------------"

    DT_TPL = \
    """
    self.{{name}} = newtype(_s(u"{{name}}"), {{super}})"""
    for t in TYPES:
        print render(DT_TPL, t)


def gen_puts():
    print "    # ---------------AUTOGENERATED---------------------"
    def t_put(t):
        return "    api.put(module, types.%s.name, types.%s)" % (t["name"], t["name"])

    for t in TYPES:
        print t_put(t)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def gen_export():
    names = [type["name"] for type in TYPES]
    type_chunks = list(chunks(names, 10))
    lines = [", ".join(line) for line in type_chunks]
    exports = ",\n                             ".join(lines)

    TPL = "from obin:lang:_types import ({{exports}})"
    print render(TPL, dict(exports=exports))

gen_declaration()

gen_puts()
#
gen_export()