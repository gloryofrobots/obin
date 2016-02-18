# ************************ OBIN TOKENS*****************************
TT_ENDSTREAM = 0
TT_INT = 1
TT_FLOAT = 2
TT_STR = 3
TT_CHAR = 4
TT_NAME = 5
TT_OPERATOR = 6
TT_NEWLINE = 7
TT_BREAK = 8
TT_CASE = 9
TT_CONTINUE = 10
TT_ELSE = 11
TT_FOR = 12
TT_WHILE = 13
TT_IF = 14
TT_WHEN = 15
TT_ELIF = 16
TT_OF = 17
TT_AS = 18
TT_MATCH = 19
TT_DEF = 20
TT_FUN = 21
TT_VAR = 22
TT_LAZY = 23
TT_AND = 24
TT_OR = 25
TT_TRUE = 26
TT_FALSE = 27
TT_NIL = 28
TT_TRY = 29
TT_THROW = 30
TT_CATCH = 31
TT_FINALLY = 32
TT_MODULE = 33
TT_IMPORT = 34
TT_EXPORT = 35
TT_TRAIT = 36
TT_GENERIC = 37
TT_SPECIFY = 38
TT_END = 39
TT_RETURN = 40
TT_ISA = 41
TT_NOTA = 42
TT_KINDOF = 43
TT_IN = 44
TT_IS = 45
TT_ISNOT = 46
TT_NOTIN = 47
TT_NOT = 48
TT_ELLIPSIS = 49
TT_WILDCARD = 50
TT_GOTO = 51
TT_ARROW = 52
TT_AT_SIGN = 53
TT_SEMI = 54
TT_SHARP = 55
TT_LCURLY = 56
TT_RCURLY = 57
TT_COMMA = 58
TT_ASSIGN = 59
TT_LPAREN = 60
TT_RPAREN = 61
TT_LSQUARE = 62
TT_RSQUARE = 63
TT_DOT = 64
TT_COLON = 65
TT_DOUBLE_DOT = 66
TT_BACKTICK = 67
TT_UNKNOWN = 68
# ************************ OBIN TOKENS REPR *****************************
__TT_REPR__ = [u"TT_ENDSTREAM", u"TT_INT", u"TT_FLOAT", u"TT_STR", u"TT_CHAR", u"TT_NAME", u"TT_OPERATOR",
               u"TT_NEWLINE", u"TT_BREAK", u"TT_CASE", u"TT_CONTINUE", u"TT_ELSE", u"TT_FOR", u"TT_WHILE", u"TT_IF",
               u"TT_WHEN", u"TT_ELIF", u"TT_OF", u"TT_AS", u"TT_MATCH", u"TT_DEF", u"TT_FUN", u"TT_VAR", u"TT_LAZY",
               u"TT_AND", u"TT_OR", u"TT_TRUE", u"TT_FALSE", u"TT_NIL", u"TT_TRY", u"TT_THROW", u"TT_CATCH",
               u"TT_FINALLY", u"TT_MODULE", u"TT_IMPORT", u"TT_EXPORT", u"TT_TRAIT", u"TT_GENERIC", u"TT_SPECIFY",
               u"TT_END", u"TT_RETURN", u"TT_ISA", u"TT_NOTA", u"TT_KINDOF", u"TT_IN", u"TT_IS", u"TT_ISNOT",
               u"TT_NOTIN", u"TT_NOT", u"TT_ELLIPSIS", u"TT_WILDCARD", u"TT_GOTO", u"TT_ARROW", u"TT_AT_SIGN",
               u"TT_SEMI", u"TT_SHARP", u"TT_LCURLY", u"TT_RCURLY", u"TT_COMMA", u"TT_ASSIGN", u"TT_LPAREN",
               u"TT_RPAREN", u"TT_LSQUARE", u"TT_RSQUARE", u"TT_DOT", u"TT_COLON", u"TT_DOUBLE_DOT", u"TT_BACKTICK",
               u"TT_UNKNOWN", ]


def token_type_to_str(ttype):
    return __TT_REPR__[ttype]
