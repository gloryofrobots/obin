from obin.compile.code.opcode import *

# ************************************************

__OPCODE_REPR__ = ["UNDEFINED", "NULL", "TRUE", "FALSE", "LITERAL", "OUTER", "LOCAL", "FUNCTION", "INTEGER", "DUP",
                   "NEXT", "IMPORT", "IMPORT_MEMBER", "GENERIC", "TRAIT", "LABEL", "STORE_OUTER", "STORE_LOCAL",
                   "ITERATOR", "RETURN", "CALL_INTERNAL", "CALL", "CALL_METHOD", "JUMP", "JUMP_IF_FALSE_NOPOP",
                   "JUMP_IF_TRUE_NOPOP", "JUMP_IF_FALSE", "JUMP_IF_TRUE", "JUMP_IF_ITERATOR_EMPTY", "MEMBER_DOT",
                   "MEMBER", "POP", "THROW", "CONCAT", "STORE_MEMBER", "SLICE", "UNPACK_SEQUENCE", "PUSH_MANY",
                   "VECTOR", "TUPLE", "OBJECT", "REIFY", ]

# ************************************************

__UNKNOWN_CHANGE__ = -128

__STACK_CHANGES__ = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1,
                     -1, -1, -2, -3, __UNKNOWN_CHANGE__, __UNKNOWN_CHANGE__, __UNKNOWN_CHANGE__, __UNKNOWN_CHANGE__,
                     __UNKNOWN_CHANGE__, __UNKNOWN_CHANGE__, ]


# ************************************************

def opcode_to_str(p):
    return __OPCODE_REPR__[p]


# SOME OPCODES CHANGE STACK SIZE DEPENDING ON RUNTIME VALUES. MAXIMAL CHANGES USED FOR THIS OPCODES,
# SO STACK CAN BE LARGER THEN IT NECESSARY
def opcode_estimate_stack_change(opcode):
    assert isinstance(opcode, tuple)
    assert len(opcode) == 3
    tag = opcode[0]
    assert isinstance(tag, int)

    change = __STACK_CHANGES__[tag]
    # print opcode_to_str(tag), change
    if change != __UNKNOWN_CHANGE__:
        return change

    arg1 = opcode[1]
    arg2 = opcode[2]

    assert isinstance(arg1, int)
    assert isinstance(arg2, int)

    if tag == PUSH_MANY:
        return -1 * arg1 + 1
    elif tag == OBJECT:
        return -1 * arg1 + arg2 + 1
    elif tag == VECTOR:
        return -1 * arg1 + 1
    elif tag == UNPACK_SEQUENCE:
        return arg1 - 1
    elif tag == TUPLE:
        return -1 * arg1 + 1
    # pop generic from stack too
    elif tag == REIFY:
        return -1 * (arg1 + 1) + 1
    return 0


def opcode_info(routine, opcode):
    from obin.runtime.internals import internal_to_str

    tag = opcode[0]
    arg1 = opcode[1]
    arg2 = opcode[2]
    # ********************************
    if tag == LOCAL:
        literal = routine.literals[arg2]
        return 'LOCAL %s (%d)' % (literal, arg1)
    # ********************************
    elif tag == OUTER:
        literal = routine.literals[arg2]
        return 'OUTER %s (%d)' % (literal, arg1)
    # ********************************
    elif tag == LITERAL:
        literal = routine.literals[arg1]
        return 'LITERAL %s (%d)' % (literal, arg1)
    # ********************************
    elif tag == STORE_LOCAL:
        literal = routine.literals[arg2]
        return 'STORE_LOCAL %s (%d)' % (literal, arg1)
    # ********************************
    elif tag == STORE_OUTER:
        literal = routine.literals[arg2]
        return 'STORE_OUTER %s (%d)' % (literal, arg1)
    # ********************************
    elif tag == IMPORT:
        literal = routine.literals[arg1]
        return 'IMPORT %s' % (literal,)
    # ********************************
    elif tag == IMPORT_MEMBER:
        literal = routine.literals[arg1]
        return 'IMPORT_MEMBER %s' % (literal,)
    # ********************************
    elif tag == CALL_INTERNAL:
        return 'CALL_PRIMITIVE %s ' % (internal_to_str(arg1))
    # ********************************
    elif tag == FUNCTION:
        return 'LOAD_FUNCTION'
    else:
        return "<%s, %s, %s>" % (opcode_to_str(tag), str(arg1), str(arg2))


def is_jump_opcode(tag):
    if tag >= JUMP and tag <= JUMP_IF_ITERATOR_EMPTY:
        return True
    return False


def is_label_opcode(tag):
    return tag == LABEL
