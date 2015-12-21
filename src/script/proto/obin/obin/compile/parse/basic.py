from obin.compile.parse.token_type import (TT_UNKNOWN, TT_ENDSTREAM, TT_RCURLY,
                                           TT_DOT, TT_LSQUARE, TT_NAME, TT_COMMA, TT_SEMI)

from obin.compile.parse.tokens import token_type_to_str

def parse_error(parser, message, args=None, node=None):
    if not node:
        error_message = "Parse Error %d:%d %s" % (parser.token.line, parser.token.pos, message)
    else:
        error_message = "Parse Error %d:%d %s" % (node.line, node.position, message)

    raise RuntimeError(error_message, args)


class Handler(object):
    def __init__(self):
        self.nud = None
        self.led = None
        self.std = None
        self.lbp = None
        self.rbp = None
        self.value = None


def set_handler(parser, ttype, h):
    parser.handlers[ttype] = h
    return handler(parser, ttype)


def node_handler(parser, node):
    return handler(parser, node.type)


def handler(parser, ttype):
    assert ttype < TT_UNKNOWN
    try:
        return parser.handlers[ttype]
    except:
        return set_handler(parser, ttype, Handler())
        # parser.handlers[ttype] = Handler()
        # return handler(parser, ttype)
        # error(parser, "Handler not exists %s" % TT_TO_STR(ttype))


def nud(parser, node):
    handler = node_handler(parser, node)
    if not handler.nud:
        parse_error(parser, "Unknown token", args=(node, str(parser.token)))
    return handler.nud(parser, node)


def std(parser, node):
    handler = node_handler(parser, node)
    if not handler.std:
        parse_error(parser, "Unknown token", args=node)

    return handler.std(parser, node)


def has_nud(parser, node):
    handler = node_handler(parser, node)
    return handler.nud is not None


def has_led(parser, node):
    handler = node_handler(parser, node)
    return handler.led is not None


def has_std(parser, node):
    handler = node_handler(parser, node)
    return handler.std is not None


def rbp(parser, node):
    handler = node_handler(parser, node)
    return handler.rbp


def lbp(parser, node):
    handler = node_handler(parser, node)
    return handler.lbp


def led(parser, node, left):
    handler = node_handler(parser, node)
    if not handler.led:
        parse_error(parser, "Unknown token", args=node)

    return handler.led(parser, node, left)


def set_nud(parser, ttype, fn):
    h = handler(parser, ttype)
    h.nud = fn


def set_std(parser, ttype, fn):
    h = handler(parser, ttype)
    h.std = fn


def set_led(parser, ttype, lbp, fn):
    h = handler(parser, ttype)
    h.lbp = lbp
    h.led = fn


def set_lbp(parser, ttype, _lbp):
    h = handler(parser, ttype)
    h.lbp = _lbp


def check_token_type(parser, type):
    if parser.token_type != type:
        parse_error(parser, "Expected token type %s got token %s" % ((token_type_to_str(type)), parser.token))


def check_token_types(parser, types):
    if parser.token_type not in types:
        parse_error(parser, "Expected token type one of %s got token %s" %
                    ([token_type_to_str(type) for type in types], parser.token))


def advance(parser):
    if parser.isend():
        return None

    return parser.next()


def advance_expected(parser, ttype):
    check_token_type(parser, ttype)

    if parser.isend():
        return None

    return parser.next()


def endofexpression(parser):
    if parser.isend():
        return None
    if parser.is_newline_occurred:
        # print "NL"
        return parser.node
    if parser.token_type == TT_SEMI:
        # print "SEMI"
        return advance(parser)

    parse_error(parser, "Expressions must end with new line or ;")


def expression(parser, _rbp):
    previous = parser.node
    # print "******"
    # print "rbp ", _rbp
    # print "previous", previous

    advance(parser)
    # print "current", parser.token

    left = nud(parser, previous)
    # print "left", left.value
    while True:
        if parser.is_newline_occurred:
            break
        _lbp = lbp(parser, parser.node)
        if _rbp >= _lbp:
            break
        previous = parser.node
        advance(parser)
        left = led(parser, previous, left)

    return left


def statement(parser):
    node = parser.node

    if has_std(parser, node):
        advance(parser)
        value = std(parser, node)
        # endofexpression(parser)
        return value

    value = expression(parser, 0)
    endofexpression(parser)
    return value


def token_is_one_of(parser, types):
    return parser.token_type in types


def statements(parser, endlist=None):
    if not endlist:
        endlist = [TT_RCURLY, TT_ENDSTREAM]

    s = None
    stmts = []
    while True:
        if token_is_one_of(parser, endlist):
            break
        s = statement(parser)

        if s is None:
            continue
        stmts.append(s)

    length = len(stmts)
    if length == 0:
        return None
    elif length == 1:
        return stmts[0]

    return stmts


def itself(parser, node):
    return node


def nud_constant(parser, node):
    h = node_handler(parser, node)
    node.value = h.value
    node.init(0)
    return node


def constant(parser, ttype, value):
    h = handler(parser, ttype)
    h.value = value
    set_nud(parser, ttype, nud_constant)


def led_infix(parser, node, left):
    h = node_handler(parser, node)
    node.init(2)
    node.setfirst(left)
    exp = None
    while exp is None:
        exp = expression(parser, h.lbp)

    node.setsecond(exp)
    return node


def infix(parser, ttype, lbp, led=led_infix):
    set_led(parser, ttype, lbp, led)


def led_infixr(parser, node, left):
    h = node_handler(parser, node)
    node.init(2)

    node.setfirst(left)
    exp = expression(parser, h.lbp - 1)
    node.setsecond(exp)

    return node


def infixr(parser, ttype, lbp, led=led_infixr):
    set_led(parser, ttype, lbp, led)


def led_infixr_assign(parser, node, left):
    node.init(2)
    ltype = left.type
    if ltype != TT_DOT and ltype != TT_LSQUARE and ltype != TT_NAME and ltype != TT_COMMA:
        parse_error(parser, "Bad lvalue in assignment", left)
    node.setfirst(left)
    exp = expression(parser, 9)
    node.setsecond(exp)

    return node


def assignment(parser, ttype):
    infixr(parser, ttype, 10, led_infixr_assign)


def prefix_nud(parser, node):
    node.init(1)
    exp = expression(parser, 70)
    node.setfirst(exp)
    return node


def prefix(parser, ttype, nud=prefix_nud):
    set_nud(parser, ttype, nud)


def stmt(parser, ttype, std):
    set_std(parser, ttype, std)


def literal(parser, ttype):
    set_nud(parser, ttype, itself)


def symbol(parser, ttype, bp=0, nud=None):
    h = handler(parser, ttype)
    h.lbp = bp
    if not nud:
        return
    set_nud(parser, ttype, nud)


def skip(parser, ttype):
    while parser.token_type == ttype:
        advance(parser)


def empty(parser, node):
    return None