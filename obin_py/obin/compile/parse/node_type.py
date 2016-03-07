# ************************ OBIN NODES*****************************
NT_GOTO = 0
NT_TRUE = 1
NT_FALSE = 2
NT_INT = 3
NT_FLOAT = 4
NT_STR = 5
NT_CHAR = 6
NT_WILDCARD = 7
NT_NAME = 8
NT_SYMBOL = 9
NT_UNION = 10
NT_TYPE = 11
NT_MAP = 12
NT_LIST = 13
NT_TUPLE = 14
NT_UNIT = 15
NT_COMMA = 16
NT_FUN = 17
NT_FENV = 18
NT_CONDITION = 19
NT_TERNARY_CONDITION = 20
NT_WHEN = 21
NT_MATCH = 22
NT_TRY = 23
NT_MODULE = 24
NT_IMPORT = 25
NT_IMPORT_HIDING = 26
NT_IMPORT_FROM = 27
NT_IMPORT_FROM_HIDING = 28
NT_EXPORT = 29
NT_LOAD = 30
NT_TRAIT = 31
NT_IMPLEMENT = 32
NT_BIND = 33
NT_THROW = 34
NT_BREAK = 35
NT_CONTINUE = 36
NT_FOR = 37
NT_WHILE = 38
NT_REST = 39
NT_ASSIGN = 40
NT_CALL = 41
NT_JUXTAPOSITION = 42
NT_UNDEFINE = 43
NT_LOOKUP = 44
NT_LOOKUP_SYMBOL = 45
NT_LOOKUP_MODULE = 46
NT_HEAD = 47
NT_TAIL = 48
NT_DROP = 49
NT_RANGE = 50
NT_MODIFY = 51
NT_OF = 52
NT_AS = 53
NT_VAR = 54
NT_LAZY = 55
NT_AND = 56
NT_OR = 57
# ************************ OBIN NODES REPR *****************************
__NT_REPR__ = ["NT_GOTO", "NT_TRUE", "NT_FALSE", "NT_INT", "NT_FLOAT", "NT_STR", "NT_CHAR", "NT_WILDCARD", "NT_NAME",
               "NT_SYMBOL", "NT_UNION", "NT_TYPE", "NT_MAP", "NT_LIST", "NT_TUPLE", "NT_UNIT", "NT_COMMA", "NT_FUN",
               "NT_FENV", "NT_CONDITION", "NT_TERNARY_CONDITION", "NT_WHEN", "NT_MATCH", "NT_TRY", "NT_MODULE",
               "NT_IMPORT", "NT_IMPORT_HIDING", "NT_IMPORT_FROM", "NT_IMPORT_FROM_HIDING", "NT_EXPORT", "NT_LOAD",
               "NT_TRAIT", "NT_IMPLEMENT", "NT_BIND", "NT_THROW", "NT_BREAK", "NT_CONTINUE", "NT_FOR", "NT_WHILE",
               "NT_REST", "NT_ASSIGN", "NT_CALL", "NT_JUXTAPOSITION", "NT_UNDEFINE", "NT_LOOKUP", "NT_LOOKUP_SYMBOL",
               "NT_LOOKUP_MODULE", "NT_HEAD", "NT_TAIL", "NT_DROP", "NT_RANGE", "NT_MODIFY", "NT_OF", "NT_AS", "NT_VAR",
               "NT_LAZY", "NT_AND", "NT_OR", ]


def node_type_to_str(ttype):
    return __NT_REPR__[ttype]
