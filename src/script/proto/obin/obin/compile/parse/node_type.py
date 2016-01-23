# ************************ OBIN NODES*****************************
NT_TRUE = 0
NT_FALSE = 1
NT_NIL = 2
NT_UNDEFINED = 3
NT_INT = 4
NT_FLOAT = 5
NT_STR = 6
NT_CHAR = 7
NT_WILDCARD = 8
NT_NAME = 9
NT_SPECIAL_NAME = 10
NT_SYMBOL = 11
NT_FUNC = 12
NT_IF = 13
NT_WHEN = 14
NT_MATCH = 15
NT_TRY = 16
NT_ORIGIN = 17
NT_IMPORT = 18
NT_TRAIT = 19
NT_GENERIC = 20
NT_SPECIFY = 21
NT_RETURN = 22
NT_THROW = 23
NT_BREAK = 24
NT_CONTINUE = 25
NT_FOR = 26
NT_WHILE = 27
NT_REST = 28
NT_MAP = 29
NT_ASSIGN = 30
NT_CALL = 31
NT_CALL_MEMBER = 32
NT_LIST = 33
NT_TUPLE = 34
NT_LOOKUP = 35
NT_LOOKUP_SYMBOL = 36
NT_SLICE = 37
NT_RANGE = 38
NT_MODIFY = 39
NT_CONS = 40
NT_OF = 41
NT_AS = 42
NT_IN = 43
NT_IS = 44
NT_ISNOT = 45
NT_AND = 46
NT_OR = 47
NT_NOT = 48
NT_EQ = 49
NT_LE = 50
NT_GE = 51
NT_NE = 52
NT_BITAND = 53
NT_BITNOT = 54
NT_BITOR = 55
NT_BITXOR = 56
NT_SUB = 57
NT_ADD = 58
NT_MUL = 59
NT_DIV = 60
NT_MOD = 61
NT_LT = 62
NT_GT = 63
NT_RSHIFT = 64
NT_URSHIFT = 65
NT_LSHIFT = 66
NT_UNARY_PLUS = 67
NT_UNARY_MINUS = 68
NT_ADD_ASSIGN = 69
NT_GOTO = 70
NT_SUB_ASSIGN = 71
NT_MUL_ASSIGN = 72
NT_DIV_ASSIGN = 73
NT_MOD_ASSIGN = 74
NT_BITAND_ASSIGN = 75
NT_BITXOR_ASSIGN = 76
NT_BITOR_ASSIGN = 77
# ************************ OBIN NODES REPR *****************************
__NT_REPR__ = ["NT_TRUE", "NT_FALSE", "NT_NIL", "NT_UNDEFINED", "NT_INT", "NT_FLOAT", "NT_STR", "NT_CHAR",
               "NT_WILDCARD", "NT_NAME", "NT_SPECIAL_NAME", "NT_SYMBOL", "NT_FUNC", "NT_IF", "NT_WHEN", "NT_MATCH",
               "NT_TRY", "NT_ORIGIN", "NT_IMPORT", "NT_TRAIT", "NT_GENERIC", "NT_SPECIFY", "NT_RETURN", "NT_THROW",
               "NT_BREAK", "NT_CONTINUE", "NT_FOR", "NT_WHILE", "NT_REST", "NT_MAP", "NT_ASSIGN", "NT_CALL",
               "NT_CALL_MEMBER", "NT_LIST", "NT_TUPLE", "NT_LOOKUP", "NT_LOOKUP_SYMBOL", "NT_SLICE", "NT_RANGE",
               "NT_MODIFY", "NT_CONS", "NT_OF", "NT_AS", "NT_IN", "NT_IS", "NT_ISNOT", "NT_AND", "NT_OR", "NT_NOT",
               "NT_EQ", "NT_LE", "NT_GE", "NT_NE", "NT_BITAND", "NT_BITNOT", "NT_BITOR", "NT_BITXOR", "NT_SUB",
               "NT_ADD", "NT_MUL", "NT_DIV", "NT_MOD", "NT_LT", "NT_GT", "NT_RSHIFT", "NT_URSHIFT", "NT_LSHIFT",
               "NT_UNARY_PLUS", "NT_UNARY_MINUS", "NT_ADD_ASSIGN", "NT_GOTO", "NT_SUB_ASSIGN", "NT_MUL_ASSIGN",
               "NT_DIV_ASSIGN", "NT_MOD_ASSIGN", "NT_BITAND_ASSIGN", "NT_BITXOR_ASSIGN", "NT_BITOR_ASSIGN", ]


def node_type_to_str(ttype):
    return __NT_REPR__[ttype]
