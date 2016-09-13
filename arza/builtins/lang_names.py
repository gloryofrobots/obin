PREFIX = "arza:lang:"

NOT = PREFIX + "not"
ELEM = PREFIX + "elem"
IS = PREFIX + "is"
IS_EMPTY = PREFIX + "is_empty"

ISNOT = PREFIX + "isnot"
KINDOF = PREFIX + "kindof"

# functions used by compiler in code gen
DERIVE = PREFIX + "derive"
IS_INDEXED = PREFIX + "is_indexed"
IS_SEQ = PREFIX + "is_seq"
IS_DICT = PREFIX + "is_dict"
LEN = PREFIX + "len"
TYPE = PREFIX + "deftype"
GENERIC = PREFIX + "defgeneric"
INTERFACE = PREFIX + "definterface"

PARTIAL = PREFIX + "defpartial"

SPECIFY = PREFIX + "specify"
DERIVE = PREFIX + "derive"

SLICE = PREFIX + "slice"
DROP = PREFIX + "drop"
TAKE = PREFIX + "take"

AT = PREFIX + "at"
PUT = PREFIX + "put"

REST = PREFIX + "rest"
FIRST = PREFIX + "first"
CONS = PREFIX + "cons"

EQ = PREFIX + "=="
GE = PREFIX + ">="

HOLE_PREFIX = "@__hole__"

TO_SEQ = PREFIX + "to_seq"
CONCAT = PREFIX + "++"
APPLY = PREFIX + "apply"
NEGATE = PREFIX + "negate"


TINT = PREFIX + "Int"
TFLOAT = PREFIX + "Float"
TBOOL = PREFIX + "Bool"
TCHAR = PREFIX + "Char"
TSYMBOL = PREFIX + "Symbol"
TSTRING = PREFIX + "String"
TLIST = PREFIX + "List"
TTUPLE = PREFIX + "Tuple"
TMAP = PREFIX + "Map"
