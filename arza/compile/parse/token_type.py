# ************************ OBIN TOKENS*****************************
TT_ENDSTREAM = 0
TT_INT = 1
TT_FLOAT = 2
TT_STR = 3
TT_MULTI_STR = 4
TT_CHAR = 5
TT_NAME = 6
TT_TICKNAME = 7
TT_TYPENAME = 8
TT_OPERATOR = 9
TT_VOID = 10
TT_NIL = 11
TT_FUN = 12
TT_MATCH = 13
TT_WITH = 14
TT_CASE = 15
TT_BREAK = 16
TT_CONTINUE = 17
TT_WHILE = 18
TT_DEF = 19
TT_CLASS = 20
TT_EXTENDS = 21
TT_IF = 22
TT_ELIF = 23
TT_ELSE = 24
TT_THEN = 25
TT_WHEN = 26
TT_OF = 27
TT_LET = 28
TT_IN = 29
TT_IS = 30
TT_AS = 31
TT_NOT = 32
TT_AND = 33
TT_OR = 34
TT_TRUE = 35
TT_FALSE = 36
TT_TRY = 37
TT_THROW = 38
TT_CATCH = 39
TT_FINALLY = 40
TT_IMPORT = 41
TT_INCLUDE = 42
TT_FROM = 43
TT_HIDING = 44
TT_HIDE = 45
TT_EXPORT = 46
TT_USE = 47
TT_FOR = 48
TT_RECEIVE = 49
TT_AFTER = 50
TT_END_EXPR = 51
TT_NEWLINE = 52
TT_INDENT = 53
TT_DEDENT = 54
TT_INFIXL = 55
TT_INFIXR = 56
TT_PREFIX = 57
TT_ELLIPSIS = 58
TT_WILDCARD = 59
TT_GOTO = 60
TT_ARROW = 61
TT_FAT_ARROW = 62
TT_BACKARROW = 63
TT_DISPATCH = 64
TT_AT_SIGN = 65
TT_DOUBLE_AT = 66
TT_DOLLAR = 67
TT_SHARP = 68
TT_JUXTAPOSITION = 69
TT_LCURLY = 70
TT_RCURLY = 71
TT_COMMA = 72
TT_ASSIGN = 73
TT_INFIX_DOT_LCURLY = 74
TT_INFIX_DOT_LSQUARE = 75
TT_LPAREN = 76
TT_RPAREN = 77
TT_LSQUARE = 78
TT_RSQUARE = 79
TT_DOT = 80
TT_COLON = 81
TT_DOUBLE_COLON = 82
TT_TRIPLE_COLON = 83
TT_DOUBLE_DOT = 84
TT_BACKTICK_NAME = 85
TT_BACKTICK_OPERATOR = 86
TT_UNKNOWN = 87
# ************************ OBIN TOKENS REPR *****************************
__TT_REPR__ = [u"TT_ENDSTREAM", u"TT_INT", u"TT_FLOAT", u"TT_STR", u"TT_MULTI_STR", u"TT_CHAR", u"TT_NAME",
               u"TT_TICKNAME", u"TT_TYPENAME", u"TT_OPERATOR", u"TT_VOID", u"TT_NIL", u"TT_FUN", u"TT_MATCH",
               u"TT_WITH", u"TT_CASE", u"TT_BREAK", u"TT_CONTINUE", u"TT_WHILE", u"TT_DEF", u"TT_CLASS", u"TT_EXTENDS",
               u"TT_IF", u"TT_ELIF", u"TT_ELSE", u"TT_THEN", u"TT_WHEN", u"TT_OF", u"TT_LET", u"TT_IN", u"TT_IS",
               u"TT_AS", u"TT_NOT", u"TT_AND", u"TT_OR", u"TT_TRUE", u"TT_FALSE", u"TT_TRY", u"TT_THROW", u"TT_CATCH",
               u"TT_FINALLY", u"TT_IMPORT", u"TT_INCLUDE", u"TT_FROM", u"TT_HIDING", u"TT_HIDE", u"TT_EXPORT",
               u"TT_USE", u"TT_FOR", u"TT_RECEIVE", u"TT_AFTER", u"TT_END_EXPR", u"TT_NEWLINE", u"TT_INDENT",
               u"TT_DEDENT", u"TT_INFIXL", u"TT_INFIXR", u"TT_PREFIX", u"TT_ELLIPSIS", u"TT_WILDCARD", u"TT_GOTO",
               u"TT_ARROW", u"TT_FAT_ARROW", u"TT_BACKARROW", u"TT_DISPATCH", u"TT_AT_SIGN", u"TT_DOUBLE_AT",
               u"TT_DOLLAR", u"TT_SHARP", u"TT_JUXTAPOSITION", u"TT_LCURLY", u"TT_RCURLY", u"TT_COMMA", u"TT_ASSIGN",
               u"TT_INFIX_DOT_LCURLY", u"TT_INFIX_DOT_LSQUARE", u"TT_LPAREN", u"TT_RPAREN", u"TT_LSQUARE",
               u"TT_RSQUARE", u"TT_DOT", u"TT_COLON", u"TT_DOUBLE_COLON", u"TT_TRIPLE_COLON", u"TT_DOUBLE_DOT",
               u"TT_BACKTICK_NAME", u"TT_BACKTICK_OPERATOR", u"TT_UNKNOWN", ]


def token_type_to_u(ttype):
    return __TT_REPR__[ttype]


def token_type_to_s(ttype):
    return str(__TT_REPR__[ttype])
