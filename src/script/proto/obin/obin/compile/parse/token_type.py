# ************************ OBIN TOKENS*****************************
TT_ENDSTREAM = 0
TT_INT = 1
TT_FLOAT = 2
TT_STR = 3
TT_CHAR = 4
TT_NAME = 5
TT_ID = 6
TT_NEWLINE = 7
TT_OPERATOR = 8
TT_BREAK = 9
TT_CASE = 10
TT_CONTINUE = 11
TT_ELSE = 12
TT_FOR = 13
TT_WHILE = 14
TT_IF = 15
TT_WHEN = 16
TT_ELIF = 17
TT_OF = 18
TT_AS = 19
TT_MATCH = 20
TT_DEF = 21
TT_FUN = 22
TT_VAR = 23
TT_LAZY = 24
TT_AND = 25
TT_OR = 26
TT_TRUE = 27
TT_FALSE = 28
TT_NIL = 29
TT_TRY = 30
TT_THROW = 31
TT_CATCH = 32
TT_FINALLY = 33
TT_MODULE = 34
TT_IMPORT = 35
TT_EXPORT = 36
TT_LOAD = 37
TT_USE = 38
TT_TRAIT = 39
TT_GENERIC = 40
TT_SPECIFY = 41
TT_END = 42
TT_RETURN = 43
TT_ISA = 44
TT_NOTA = 45
TT_KINDOF = 46
TT_ELLIPSIS = 47
TT_WILDCARD = 48
TT_GOTO = 49
TT_ARROW = 50
TT_AT_SIGN = 51
TT_SEMI = 52
TT_COLON = 53
TT_LCURLY = 54
TT_RCURLY = 55
TT_COMMA = 56
TT_ASSIGN = 57
TT_LPAREN = 58
TT_RPAREN = 59
TT_LSQUARE = 60
TT_RSQUARE = 61
TT_DOT = 62
TT_DOUBLE_DOT = 63
TT_BACKTICK = 64
TT_UNKNOWN = 65
# ************************ OBIN TOKENS REPR *****************************
__TT_REPR__ = [u"TT_ENDSTREAM", u"TT_INT", u"TT_FLOAT", u"TT_STR", u"TT_CHAR", u"TT_NAME", u"TT_ID", u"TT_NEWLINE",
               u"TT_OPERATOR", u"TT_BREAK", u"TT_CASE", u"TT_CONTINUE", u"TT_ELSE", u"TT_FOR", u"TT_WHILE", u"TT_IF",
               u"TT_WHEN", u"TT_ELIF", u"TT_OF", u"TT_AS", u"TT_MATCH", u"TT_DEF", u"TT_FUN", u"TT_VAR", u"TT_LAZY",
               u"TT_AND", u"TT_OR", u"TT_TRUE", u"TT_FALSE", u"TT_NIL", u"TT_TRY", u"TT_THROW", u"TT_CATCH",
               u"TT_FINALLY", u"TT_MODULE", u"TT_IMPORT", u"TT_EXPORT", u"TT_LOAD", u"TT_USE", u"TT_TRAIT",
               u"TT_GENERIC", u"TT_SPECIFY", u"TT_END", u"TT_RETURN", u"TT_ISA", u"TT_NOTA", u"TT_KINDOF",
               u"TT_ELLIPSIS", u"TT_WILDCARD", u"TT_GOTO", u"TT_ARROW", u"TT_AT_SIGN", u"TT_SEMI", u"TT_COLON",
               u"TT_LCURLY", u"TT_RCURLY", u"TT_COMMA", u"TT_ASSIGN", u"TT_LPAREN", u"TT_RPAREN", u"TT_LSQUARE",
               u"TT_RSQUARE", u"TT_DOT", u"TT_DOUBLE_DOT", u"TT_BACKTICK", u"TT_UNKNOWN", ]


def token_type_to_str(ttype):
    return __TT_REPR__[ttype]
