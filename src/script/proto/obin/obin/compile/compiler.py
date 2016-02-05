__author__ = 'gloryofrobots'
from obin.compile.code.opcode import *
from obin.compile.parse import parser
from obin.compile.parse import nodes
from obin.compile.parse.nodes import (node_type, node_arity,
                                      node_first, node_second, node_third)
from obin.compile.parse.node_type import *
from obin.compile.scope import Scope
from obin.types import space, api, plist
from obin.builtins.internals import internals
from obin.compile.code.source import CodeSource, codeinfo, codeinfo_unknown, SourceInfo
from obin.utils.misc import is_absent_index, string_unquote
from obin.runtime import error


def compile_error(process, compiler, code, node, message):
    line = code.info.get_line(api.to_i(nodes.node_line(node)))
    return error.throw(error.Errors.COMPILE,
                       space.newtuple([
                           space.newstring(message),
                           space.newstring_from_str(nodes.node_value(node)),
                           space.newtuple(list(info(node))),
                           space.newstring(line)
                       ]))


class Compiler:
    def __init__(self, path, src):
        self.scopes = []
        self.depth = -1
        self.source_path = path
        self.source = src


def info(node):
    if nodes.is_empty_node(node):
        return codeinfo_unknown()
    return codeinfo(nodes.node_position(node), nodes.node_line(node), nodes.node_column(node))


########################
# SCOPES
########################


def _enter_scope(process, compiler):
    compiler.depth += 1

    new_scope = Scope()
    compiler.scopes.append(new_scope)
    # print 'starting new scope %d' % (process, compiler.depth, )


def _is_modifiable_binding(process, compiler, name):
    scope = _current_scope(process, compiler)
    if not is_absent_index(scope.get_local_index(name)):
        return True
    if scope.has_outer(name):
        return True

    return False


def _declare_outer(process, compiler, code, outer):
    value = _get_name_value(outer)
    symbol = space.newsymbol_py_str(process, value)
    scope = _current_scope(process, compiler)
    if not scope.is_function_scope():
        compile_error(process, compiler, code, symbol, u"outer variables can be declared only inside functions")

    if scope.has_outer(symbol):
        compile_error(process, compiler, code, symbol, u"outer variable has already been declared")
    scope.add_outer(symbol)


def _declare_arguments(process, compiler, args_count, varargs):
    _current_scope(process, compiler).declare_arguments(args_count, varargs)


def _declare_function_name(process, compiler, name):
    _current_scope(process, compiler).add_function_name(name)


def _declare_reference(process, compiler, symbol):
    assert space.issymbol(symbol)
    scope = _current_scope(process, compiler)
    idx = scope.get_reference(symbol)
    if is_absent_index(idx):
        idx = scope.add_reference(symbol)
    return idx


def _declare_literal(process, compiler, literal):
    assert space.isany(literal)
    scope = _current_scope(process, compiler)
    idx = scope.get_literal(literal)
    if is_absent_index(idx):
        idx = scope.add_literal(literal)
    return idx


def _declare_local(process, compiler, symbol):
    assert space.issymbol(symbol)
    assert not api.isempty(symbol)
    scope = _current_scope(process, compiler)
    idx = scope.get_local_index(symbol)
    if not is_absent_index(idx):
        return idx

    idx = scope.add_local(symbol)
    assert not is_absent_index(idx)
    return idx


def _get_variable_index(process, compiler, name):
    """
        return var_index, is_local_variable
    """
    scope_id = 0
    for scope in reversed(compiler.scopes):
        idx = scope.get_local_index(name)
        if not is_absent_index(idx):
            if scope_id == 0:
                return idx, True
            else:
                # TODO here can be optimisation where we can calculate number of scopes to find back variable
                ref_id = _declare_reference(process, compiler, name)
                return ref_id, False
        scope_id += 1

    # compile_error(process,process, compiler.current_node, "Non reachable variable", name)
    # COMMENT ERROR BECAUSE OF LATER LINKING OF BUILTINS
    ref_id = _declare_reference(process, compiler, name)
    return ref_id, False


def _declare_variable(process, compiler, symbol):
    """
        return var_index, is_local
    """

    scope = _current_scope(process, compiler)
    if scope.has_outer(symbol):
        idx = _declare_reference(process, compiler, symbol)
        return idx, False

    idx = _declare_local(process, compiler, symbol)
    return idx, True


def _exit_scope(process, compiler):
    compiler.depth = compiler.depth - 1
    compiler.scopes.pop()
    # print 'closing scope, returning to %d' % (process, compiler.depth, )


def _current_scope(process, compiler):
    return compiler.scopes[-1]


"""
    HOOKS
"""


def _compile_FLOAT(process, compiler, code, node):
    value = float(nodes.node_value(node))
    idx = _declare_literal(process, compiler, space.newfloat(value))
    code.emit_1(LITERAL, idx, info(node))


def _compile_INT(process, compiler, code, node):
    value = int(nodes.node_value(node))
    idx = _declare_literal(process, compiler, space.newint(value))
    code.emit_1(LITERAL, idx, info(node))


def _emit_integer(process, compiler, code, integer):
    idx = _declare_literal(process, compiler, space.newint(integer))
    code.emit_1(LITERAL, idx, codeinfo_unknown())


def _compile_TRUE(process, compiler, code, node):
    code.emit_0(TRUE, info(node))


def _compile_FALSE(process, compiler, code, node):
    code.emit_0(FALSE, info(node))


def _compile_NIL(process, compiler, code, node):
    code.emit_0(NIL, info(node))


def _get_name_value(name):
    if node_type(name) == NT_SPECIAL_NAME:
        value = _get_special_name_value(name)
    elif node_type(name) == NT_NAME:
        value = nodes.node_value(name)
    else:
        assert False, "Invalid call"
    return value


def _emit_pop(code):
    code.emit_0(POP, codeinfo_unknown())


def _emit_dup(code):
    code.emit_0(DUP, codeinfo_unknown())


def _emit_nil(code):
    code.emit_0(NIL, codeinfo_unknown())


def _emit_symbol_name(process, compiler, code, name):
    value = _get_name_value(name)
    symbol = space.newsymbol_py_str(process, value)
    idx = _declare_literal(process, compiler, symbol)
    code.emit_1(LITERAL, idx, info(name))


def _compile_STR(process, compiler, code, node):
    from obin.runistr import unicode_unescape, decode_str_utf8

    try:
        strval = str(nodes.node_value(node))
        strval = decode_str_utf8(strval)
        strval = string_unquote(strval)
        strval = unicode_unescape(strval)
        string = space.newstring(strval)
        idx = _declare_literal(process, compiler, string)
        code.emit_1(LITERAL, idx, info(node))
    except RuntimeError as e:
        compile_error(process, compiler, code, node, unicode(e.args[0]))


def _compile_CHAR(process, compiler, code, node):
    from obin.runistr import unicode_unescape, decode_str_utf8
    # TODO CHAR

    try:
        strval = str(nodes.node_value(node))
        strval = decode_str_utf8(strval)
        strval = string_unquote(strval)
        strval = unicode_unescape(strval)
        string = space.newstring(strval)
        idx = _declare_literal(process, compiler, string)
        code.emit_1(LITERAL, idx, info(node))
    except RuntimeError as e:
        compile_error(process, compiler, code, node, unicode(e.args[0]))


# def _compile_OUTER(process, compiler, code, node):
#     # TODO REMOVE IT
#     assert False, "Why you need it?"
#     name = space.newstring_from_str(node_first(node).value)
#     _declare_outer(process, compiler, name)


def _on_binary_primitive(process, compiler, code, node, name):
    _compile(process, compiler, code, node_first(node))
    _compile(process, compiler, code, node_second(node))
    code.emit_1(CALL_INTERNAL, name, info(node))


def _on_unary_primitive(process, compiler, code, node, name):
    _compile(process, compiler, code, node_first(node))
    code.emit_1(CALL_INTERNAL, name, info(node))


def _compile_BITAND(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.BITAND)


def _compile_BITOR(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.BITOR)


def _compile_BITXOR(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.BITXOR)


def _compile_UNARY_PLUS(process, compiler, code, node):
    _on_unary_primitive(process, compiler, code, node, internals.UPLUS)


def _compile_ADD(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.ADD)


def _compile_MUL(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.MUL)


def _compile_MOD(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.MOD)


def _compile_DIV(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.DIV)


def _compile_UNARY_MINUS(process, compiler, code, node):
    _on_unary_primitive(process, compiler, code, node, internals.UMINUS)


def _compile_SUB(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.SUB)


def _compile_BITNOT(process, compiler, code, node):
    _on_unary_primitive(process, compiler, code, node, internals.BITNOT)


def _compile_NOT(process, compiler, code, node):
    _on_unary_primitive(process, compiler, code, node, internals.NOT)


def _compile_GE(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.GE)


def _compile_GT(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.GT)


def _compile_LE(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.LE)


def _compile_LT(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.LT)


def _compile_IS(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.IS)


def _compile_ISNOT(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.ISNOT)


def _compile_ISA(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.ISA)


def _compile_NOTA(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.NOTA)


def _compile_KINDOF(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.KINDOF)


def _compile_IN(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.IN)


def _compile_NOTIN(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.NOTIN)


def _compile_EQ(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.EQ)


def _compile_NE(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.NE)


def _compile_LSHIFT(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.LSH)


def _compile_RSHIFT(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.RSH)


def _compile_URSHIFT(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.URSH)


def _compile_AND(process, compiler, code, node):
    _compile(process, compiler, code, node_first(node))
    one = code.prealocate_label()
    code.emit_1(JUMP_IF_FALSE_NOPOP, one, info(node))
    _compile(process, compiler, code, node_second(node))
    code.emit_1(LABEL, one, info(node))


def _compile_OR(process, compiler, code, node):
    _compile(process, compiler, code, node_first(node))
    one = code.prealocate_label()
    code.emit_1(JUMP_IF_TRUE_NOPOP, one, info(node))
    _compile(process, compiler, code, node_second(node))
    code.emit_1(LABEL, one, info(node))


def _compile_ASSIGN_MEMBER(process, compiler, code, node):
    member = node_first(node)
    value = node_second(node)
    obj = node_first(member)
    item = node_second(member)

    _compile(process, compiler, code, obj)
    _compile(process, compiler, code, item)
    _compile(process, compiler, code, value)
    code.emit_0(STORE_MEMBER, info(node))


def _compile_ASSIGN_SYMBOL(process, compiler, code, node):
    member = node_first(node)

    obj = node_first(member)
    _compile(process, compiler, code, obj)
    _emit_symbol_name(process, compiler, code, node_second(member))
    _compile(process, compiler, code, node_second(node))
    code.emit_0(STORE_MEMBER, info(node))


def _emit_store_name(process, compiler, code, namenode):
    name = space.newsymbol_py_str(process, nodes.node_value(namenode))
    _emit_store(process, compiler, code, name, namenode)


def _emit_store(process, compiler, code, name, namenode):
    index = _declare_local(process, compiler, name)

    name_index = _declare_literal(process, compiler, name)
    code.emit_2(STORE_LOCAL, index, name_index, info(namenode))


#########################################################

PATTERN_DATA = """
    match [1, 2, 3]:
        case {age=41, name="Bob"}: (name, age) end
        case {name="Bob", surname=("Alice", "Dou")}: (surname, name) end
    end
"""


def _compile_match(process, compiler, code, node, patterns):
    from obin.compile.match import transform
    from obin.compile.parse.nodes import create_goto_node
    from obin.compile import MATCH_SYS_VAR
    name = space.newsymbol_py_str(process, MATCH_SYS_VAR)
    name_index = _declare_literal(process, compiler, name)
    index = _declare_local(process, compiler, name)
    code.emit_2(STORE_LOCAL, index, name_index, codeinfo_unknown())

    endmatch = code.prealocate_label()
    graph = transform(process, compiler, code, node, patterns, create_goto_node(endmatch))
    _compile(process, compiler, code, graph)
    code.emit_1(LABEL, endmatch, codeinfo_unknown())


def _compile_MATCH(process, compiler, code, node):
    exp = node_first(node)
    patterns = node_second(node)
    _compile(process, compiler, code, exp)
    _compile_match(process, compiler, code, node, patterns)


def _compile_GOTO(process, compiler, code, node):
    # TODO REMOVE THIS SHIT
    # WE NEED TO REMOVE POPS ON GOTO BECAUSE OF AUTOMATIC POP INSERTION
    # GOTO USED ONLY FOR JUMPS ON PATTERN MATCHING BECAUSE IN PM WE PRODUCE TREE OF IFS
    # AND NEED JUMP FROM SUCCESS BRANCH. IT'S ACTUALLY SIMPLIFIES COMPILATION BUT LEEDS TO THIS BAD DESIGN
    # SOLUTION: REMOVE AUTO POPS, SOMEHOW

    last_code = code.last()
    if last_code[0] == POP:
        code.remove_last()

    value = int(nodes.node_value(node))
    code.emit_1(JUMP, value, codeinfo_unknown())


#########################################################
#####
# DESTRUCT DESTRUCT
####
def _compile_destruct(process, compiler, code, node):
    _compile(process, compiler, code, node_second(node))
    return _compile_destruct_recur(process, compiler, code, node_first(node))


def _is_optimizable_unpack_seq_pattern(node):
    items = node_first(node)
    for child in items:
        if child is None:
            print ""
        if node_type(child) != NT_NAME:
            return False
    return True


def _compile_destruct_recur(process, compiler, code, node):
    if node_type(node) == NT_TUPLE:
        # x,y,z = foo() optimisation to single unpack opcode
        if _is_optimizable_unpack_seq_pattern(node):
            return _compile_destruct_unpack_seq(process, compiler, code, node)
        else:
            return _compile_destruct_recur_seq(process, compiler, code, node)
    elif node_type(node) == NT_MAP:
        return _compile_destruct_recur_map(process, compiler, code, node)
    else:
        compile_error(process, compiler, code, node, u"unsupported assignment syntax")


def _compile_destruct_recur_map(process, compiler, code, node):
    pairs = node_first(node)
    for pair in pairs:
        _emit_dup(code)

        key = pair[0]
        value = pair[1]
        varname = None
        if nodes.is_empty_node(value):
            varname = key
        elif node_type(value) == NT_NAME:
            varname = value

        _emit_map_key(process, compiler, code, key)

        code.emit_0(MEMBER, info(key))

        if varname is None:
            _compile_destruct_recur(process, compiler, code, value)
            _emit_pop(code)
        else:
            _emit_store_name(process, compiler, code, varname)
            _emit_pop(code)


##################################################
# DESTRUCT SEQUENCE
##################################################

def _compile_destruct_recur_seq_rest(process, compiler, code, last_item, last_index):
    _emit_dup(code)
    varname = node_first(last_item)
    _emit_integer(process, compiler, code, last_index)
    _emit_nil(code)
    code.emit_0(SLICE, codeinfo_unknown())
    _emit_store_name(process, compiler, code, varname)
    _emit_pop(code)


def _compile_destruct_recur_seq_item(process, compiler, code, item, index):
    _emit_dup(code)

    varname = None
    if node_type(item) == NT_NAME:
        varname = item

    idx = _declare_literal(process, compiler, space.newint(index))
    code.emit_1(LITERAL, idx, info(item))
    code.emit_0(MEMBER, info(item))

    if varname is None:
        _compile_destruct_recur(process, compiler, code, item)
        _emit_pop(code)
    else:
        _emit_store_name(process, compiler, code, varname)
        _emit_pop(code)


def _compile_destruct_recur_seq(process, compiler, code, node):
    items = node_first(node)
    length = len(items)

    last_index = length - 1

    for i in range(last_index):
        item = items[i]
        _compile_destruct_recur_seq_item(process, compiler, code, item, i)

    last_item = items[last_index]
    if node_type(last_item) == NT_REST:
        _compile_destruct_recur_seq_rest(process, compiler, code, last_item, last_index)
    else:
        _compile_destruct_recur_seq_item(process, compiler, code, last_item, last_index)


def _compile_destruct_unpack_seq(process, compiler, code, node):
    _emit_dup(code)
    names = node_first(node)
    length = len(names)
    code.emit_1(UNPACK_SEQUENCE, length, info(node))
    # TODO FIX IT
    if length > 1:
        for name in names[0:length - 1]:
            _emit_store_name(process, compiler, code, name)
            _emit_pop(code)
    last_name = names[length - 1]
    _emit_store_name(process, compiler, code, last_name)
    _emit_pop(code)


################################################################################

def _compile_ASSIGN(process, compiler, code, node):
    left = node_first(node)
    if node_type(left) == NT_LOOKUP_SYMBOL:
        return _compile_ASSIGN_SYMBOL(process, compiler, code, node)
    elif node_type(left) == NT_LOOKUP:
        return _compile_ASSIGN_MEMBER(process, compiler, code, node)
    elif node_type(left) == NT_TUPLE or node_type(left) == NT_MAP:
        return _compile_destruct(process, compiler, code, node)

    _compile(process, compiler, code, node_second(node))
    _emit_store_name(process, compiler, code, left)


def _compile_node_name_lookup(process, compiler, code, node):
    name_value = _get_name_value(node)
    name = space.newsymbol_py_str(process, name_value)

    index, is_local = _get_variable_index(process, compiler, name)
    name_index = _declare_literal(process, compiler, name)
    if is_local:
        code.emit_2(LOCAL, index, name_index, info(node))
    else:
        code.emit_2(OUTER, index, name_index, info(node))


def _get_special_name_value(node):
    # REMOVE BACKTICKS `xxx`
    return nodes.node_value(node)[1:len(nodes.node_value(node)) - 1]


def _compile_SPECIAL_NAME(process, compiler, code, node):
    _compile_node_name_lookup(process, compiler, code, node)


def _compile_NAME(process, compiler, code, node):
    _compile_node_name_lookup(process, compiler, code, node)


def _compile_SYMBOL(process, compiler, code, node):
    name = node_first(node)
    _emit_symbol_name(process, compiler, code, name)


def _compile_RETURN(process, compiler, code, node):
    expr = node_first(node)
    if nodes.is_empty_node(expr):
        _emit_nil(code)
    else:
        _compile(process, compiler, code, expr)

    code.emit_0(RETURN, info(node))


def _compile_THROW(process, compiler, code, node):
    expr = node_first(node)
    if nodes.is_empty_node(expr):
        _emit_nil(code)
    else:
        _compile(process, compiler, code, expr)

    code.emit_0(THROW, info(node))


# TODO MAKE NAMES from SYMBOLS in parser
def _emit_map_key(process, compiler, code, key):
    if node_type(key) == NT_NAME:
        # in case of names in object literal we must convert them to symbols
        _emit_symbol_name(process, compiler, code, key)
    else:
        _compile(process, compiler, code, key)


def _compile_MODIFY(process, compiler, code, node):
    obj = node_first(node)
    modifications = node_second(node)
    _compile(process, compiler, code, obj)

    for m in modifications:
        key = m[0]
        value = m[1]
        _emit_map_key(process, compiler, code, key)
        _compile(process, compiler, code, value)
        code.emit_0(STORE_MEMBER, info(key))


def _compile_MAP(process, compiler, code, node):
    items = node_first(node)
    for c in items:
        key = c[0]
        value = c[1]
        if nodes.is_empty_node(value):
            _compile_NIL(process, compiler, code, value)
        else:
            _compile(process, compiler, code, value)

        _emit_map_key(process, compiler, code, key)

    code.emit_1(MAP, len(items), info(node))


def _compile_TUPLE(process, compiler, code, node):
    items = node_first(node)
    for c in items:
        _compile(process, compiler, code, c)

    code.emit_1(TUPLE, len(items), info(node))


def _compile_LIST(process, compiler, code, node):
    items = node_first(node)
    for c in items:
        _compile(process, compiler, code, c)

    code.emit_1(LIST, len(items), info(node))


# def _emit_list(process, compiler, code, node):
#     items = node_first(node)
#
#     for c in items:
#         _compile(process, compiler, code, c)
#
#     code.emit_1(LIST, len(items))


def _compile_BREAK(process, compiler, code, node):
    _emit_nil(code)
    if not code.emit_break():
        compile_error(process, compiler, code, node, u"break outside loop")


def _compile_CONTINUE(process, compiler, code, node):
    _emit_nil(code)
    if not code.emit_continue():
        compile_error(process, compiler, code, node, u"continue outside loop")


def _compile_func_args_and_body(process, compiler, code, name, params, body):
    funcname = _get_symbol_name_or_empty(process, name)
    _enter_scope(process, compiler)

    funccode = newcode(compiler)

    if nodes.is_empty_node(params):
        _declare_arguments(process, compiler, 0, False)
    else:
        args = node_first(params)
        length = len(args)
        funccode.emit_0(ARGUMENTS, codeinfo_unknown())

        last_param = args[length - 1]
        is_variadic = True if node_type(last_param) == NT_REST else False
        _declare_arguments(process, compiler, length, is_variadic)
        _compile_destruct_recur(process, compiler, funccode, params)

    if not api.isempty(funcname):
        _declare_function_name(process, compiler, funcname)

    _compile(process, compiler, funccode, body)
    current_scope = _current_scope(process, compiler)
    scope = current_scope.finalize()
    _exit_scope(process, compiler)
    # print "LOCALS:", str(scope.variables.keys())
    # print "REFS:", str(scope.references)
    compiled_code = funccode.finalize_compilation(scope)
    # print [str(c) for c in compiled_code.opcodes]
    # print "-------------------------"

    source = space.newfuncsource(funcname, compiled_code)
    source_index = _declare_literal(process, compiler, source)
    code.emit_1(FUNCTION, source_index, info(name))


def _compile_case_function(process, compiler, code, name, cases):
    funcname = _get_symbol_name_or_empty(process, name)
    _enter_scope(process, compiler)

    funccode = newcode(compiler)

    _declare_arguments(process, compiler, 0, True)

    if not api.isempty(funcname):
        _declare_function_name(process, compiler, funcname)

    funccode.emit_0(ARGUMENTS, codeinfo_unknown())

    _compile_match(process, compiler, funccode, name, cases)
    current_scope = _current_scope(process, compiler)
    scope = current_scope.finalize()
    _exit_scope(process, compiler)

    compiled_code = funccode.finalize_compilation(scope)

    source = space.newfuncsource(funcname, compiled_code)
    source_index = _declare_literal(process, compiler, source)
    code.emit_1(FUNCTION, source_index, info(name))


def _get_symbol_name_or_empty(process, name):
    if nodes.is_empty_node(name):
        return space.newsymbol(process, u"")
    else:
        return space.newsymbol_py_str(process, nodes.node_value(name))


def _compile_DEF(process, compiler, code, node):
    name = node_first(node)
    funcname = _get_symbol_name_or_empty(process, name)

    funcs = node_second(node)
    # single function
    if len(funcs) == 1:
        func = funcs[0]
        params = func[0]
        body = func[1]
        _compile_func_args_and_body(process, compiler, code, name, params, body)
    else:
        _compile_case_function(process, compiler, code, name, funcs)

    if api.isempty(funcname):
        return

    index = _declare_local(process, compiler, funcname)

    funcname_index = _declare_literal(process, compiler, funcname)
    code.emit_2(STORE_LOCAL, index, funcname_index, info(node))


def _compile_branch(process, compiler, code, condition, body, endif):
    _compile(process, compiler, code, condition)
    end_body = code.prealocate_label()
    code.emit_1(JUMP_IF_FALSE, end_body, info(condition))
    _compile(process, compiler, code, body)
    code.emit_1(JUMP, endif, codeinfo_unknown())
    code.emit_1(LABEL, end_body, codeinfo_unknown())


def _compile_WHEN(process, compiler, code, node):
    condition = node_first(node)
    truebranch = node_second(node)
    falsebranch = node_third(node)
    endif = code.prealocate_label()
    _compile_branch(process, compiler, code, condition, truebranch, endif)
    _compile(process, compiler, code, falsebranch)
    code.emit_1(LABEL, endif, codeinfo_unknown())


def _compile_IF(process, compiler, code, node):
    branches = node_first(node)

    endif = code.prealocate_label()
    length = len(branches)
    for i in range(length - 1):
        branch = branches[i]
        _compile_branch(process, compiler, code, branch[0], branch[1], endif)

    elsebranch = branches[length - 1]
    if nodes.is_empty_node(elsebranch):
        _emit_nil(code)
    else:
        _compile(process, compiler, code, elsebranch[1])

    code.emit_1(LABEL, endif, codeinfo_unknown())


def _compile_TRY(process, compiler, code, node):
    trynode = node_first(node)
    catch = node_second(node)
    catchvar = catch[0]
    catchnode = catch[1]
    finallynode = node_third(node)
    finallylabel = code.prealocate_label()

    catchlabel = code.prealocate_label()
    code.emit_1(PUSH_CATCH, catchlabel, codeinfo_unknown())
    _compile(process, compiler, code, trynode)
    code.emit_0(POP_CATCH, codeinfo_unknown())
    code.emit_1(JUMP, finallylabel, codeinfo_unknown())

    # exception on top of the stack due to internal process/routine logic
    code.emit_1(LABEL, catchlabel, codeinfo_unknown())
    if not nodes.is_empty_node(catchvar):
        _emit_store_name(process, compiler, code, catchvar)
    else:
        _emit_pop(code)

    _compile(process, compiler, code, catchnode)

    code.emit_1(JUMP, finallylabel, codeinfo_unknown())
    code.emit_1(LABEL, finallylabel, codeinfo_unknown())
    if not nodes.is_empty_node(finallynode):
        _compile(process, compiler, code, finallynode)


############################
# IMPORT
#############################

def _dot_to_string(process, compiler, node):
    if node_type(node) == NT_LOOKUP_SYMBOL:
        return _dot_to_string(process, compiler, node_first(node)) + '.' + nodes.node_value(node_second(node))
    else:
        return nodes.node_value(node)


def _compile_LOAD(process, compiler, code, node):
    exp = node_first(node)
    if node_type(exp) == NT_AS:
        import_name = node_second(exp)
        module_path = _dot_to_string(process, compiler, node_first(exp))
    elif node_type(exp) == NT_LOOKUP_SYMBOL:
        import_name = node_second(exp)
        module_path = _dot_to_string(process, compiler, exp)
    else:
        assert node_type(exp) == NT_NAME
        import_name = exp
        module_path = nodes.node_value(exp)

    module_path_literal = _declare_literal(process, compiler, space.newsymbol_py_str(process, module_path))
    code.emit_1(LOAD, module_path_literal, info(node))

    _emit_store_name(process, compiler, code, import_name)


def _compile_MODULE(process, compiler, code, node):
    name_node = node_first(node)
    body = node_second(node)

    compiled_code = compile_ast(process, compiler, body)
    # _enter_scope(process, compiler)
    #
    # modulecode = newcode(compiler)
    #
    # _compile(process, compiler, modulecode, body)
    # current_scope = _current_scope(process, compiler)
    # scope = current_scope.finalize()
    # _exit_scope(process, compiler)
    # compiled_code = modulecode.finalize_compilation(scope)

    module_name = space.newsymbol_py_str(process, _get_name_value(name_node))
    module = space.newmodule(module_name, compiled_code, None)
    module_index = _declare_literal(process, compiler, module)
    code.emit_1(MODULE, module_index, info(node))

    _emit_store(process, compiler, code, module_name, name_node)
    # module_name_index = _declare_local(process, compiler, module_name)
    # module_name_literal_index = _declare_literal(process, compiler, module_name)
    # code.emit_2(STORE_LOCAL, module_name_index, module_name_literal_index, info(name_node))


def _compile_GENERIC(process, compiler, code, node):
    name_node = node_first(node)
    name_value = _get_name_value(name_node)

    name = space.newsymbol_py_str(process, name_value)

    name_index = _declare_literal(process, compiler, name)
    index = _declare_local(process, compiler, name)
    code.emit_1(GENERIC, name_index, info(node))
    code.emit_2(STORE_LOCAL, index, name_index, info(name_node))

    if node_arity(node) == 2:
        methods = node_second(node)
        _emit_specify(process, compiler, code, node, methods)


def _compile_TRAIT(process, compiler, code, node):
    names = node_first(node)
    for name in names:
        name = space.newsymbol_py_str(process, nodes.node_value(name))
        index = _declare_local(process, compiler, name)

        name_index = _declare_literal(process, compiler, name)
        code.emit_1(TRAIT, name_index, info(node))
        code.emit_2(STORE_LOCAL, index, name_index, info(node))


def _emit_specify(process, compiler, code, node, methods):
    for method in methods:
        method_args = method[0]
        method_body = method[1]
        args = []
        signature = []
        for arg in method_args:
            if node_type(arg) == NT_OF:
                args.append(node_first(arg))
                signature.append(node_second(arg))
            else:
                args.append(arg)
                signature.append(None)

        for trait in signature:
            if trait is None:
                _emit_nil(code)
            else:
                _compile(process, compiler, code, trait)

        code.emit_1(TUPLE, len(signature), info(node))

        args_node = nodes.create_tuple_node(node, args)
        _compile_func_args_and_body(process, compiler, code, nodes.empty_node(), args_node,
                                    method_body)
        code.emit_1(TUPLE, 2, info(node))

    code.emit_1(SPECIFY, len(methods), info(node))


def _compile_SPECIFY(process, compiler, code, node):
    name = node_first(node)
    _compile_node_name_lookup(process, compiler, code, name)
    methods = node_second(node)
    _emit_specify(process, compiler, code, node, methods)


def _compile_FOR(process, compiler, code, node):
    source = node_second(node)
    body = node_third(node)
    _compile(process, compiler, code, source)
    code.emit_0(ITERATOR, info(node))
    # load the "last" iterations result
    _emit_nil(code)
    precond = code.emit_startloop_label()
    code.continue_at_label(precond)
    finish = code.prealocate_endloop_label(False)
    # update = code.prealocate_updateloop_label()

    code.emit_1(JUMP_IF_ITERATOR_EMPTY, finish, codeinfo_unknown())

    # put next iterator value on stack
    code.emit_0(NEXT, codeinfo_unknown())

    vars = node_first(node)
    name = space.newsymbol_py_str(process, nodes.node_value(vars[0]))
    index = _declare_local(process, compiler, name)

    name_index = _declare_literal(process, compiler, name)
    code.emit_2(STORE_LOCAL, index, name_index, info(node))
    _emit_pop(code)

    _compile(process, compiler, code, body)
    # code.emit_updateloop_label(update)

    code.emit_1(JUMP, precond, codeinfo_unknown())
    code.emit_endloop_label(finish)


def _compile_WHILE(process, compiler, code, node):
    condition = node_first(node)
    body = node_second(node)
    _emit_nil(code)
    startlabel = code.emit_startloop_label()
    code.continue_at_label(startlabel)
    _compile(process, compiler, code, condition)
    endlabel = code.prealocate_endloop_label()
    code.emit_1(JUMP_IF_FALSE, endlabel, codeinfo_unknown())
    _emit_pop(code)
    _compile(process, compiler, code, body)
    code.emit_1(JUMP, startlabel, codeinfo_unknown())
    code.emit_endloop_label(endlabel)
    code.done_continue()


def _compile_CONS(process, compiler, code, node):
    _on_binary_primitive(process, compiler, code, node, internals.CONS)


def _compile_LOOKUP_SYMBOL(process, compiler, code, node):
    obj = node_first(node)
    _compile(process, compiler, code, obj)
    _emit_symbol_name(process, compiler, code, node_second(node))
    code.emit_0(MEMBER, info(node))


def _emit_SLICE(process, compiler, code, obj, slice):
    start = node_first(slice)
    end = node_second(slice)

    _compile(process, compiler, code, obj)

    if nodes.is_wildcard_node(start):
        _emit_nil(code)
    else:
        _compile(process, compiler, code, start)

    if nodes.is_wildcard_node(end):
        _emit_nil(code)
    else:
        _compile(process, compiler, code, end)

    code.emit_0(SLICE, info(slice))


def _compile_LOOKUP(process, compiler, code, node):
    # TODO OPTIMISATION FOR INDEX LOOKUP
    obj = node_first(node)
    expr = node_second(node)
    if node_type(expr) == NT_RANGE:
        return _emit_SLICE(process, compiler, code, obj, expr)

    _compile(process, compiler, code, obj)
    _compile(process, compiler, code, expr)
    code.emit_0(MEMBER, info(node))


def _compile_args_list(process, compiler, code, args):
    args_count = 0

    for arg in args:
        _compile(process, compiler, code, arg)
        args_count += 1

    return args_count


def _compile_CALL_MEMBER(process, compiler, code, node):
    obj = node_first(node)
    method = node_second(node)
    args = node_third(node)
    # print "_compile_LPAREN_MEMBER", obj, method, args

    args_count = _compile_args_list(process, compiler, code, args)

    _compile(process, compiler, code, obj)
    _emit_symbol_name(process, compiler, code, method)
    # TODO LITERAL HERE
    # declare_symbol(process, compiler,name)

    code.emit_1(CALL_METHOD, args_count, info(node))


def _compile_CALL(process, compiler, code, node):
    func = node_first(node)
    args = node_second(node)

    # print "_compile_LPAREN", func, args

    arg_count = _compile_args_list(process, compiler, code, args)

    _compile(process, compiler, code, func)

    code.emit_1(CALL, arg_count, info(node))


####
# MAIN SWITCH
####


def _compile(process, compiler, code, ast):
    if nodes.is_list_node(ast):
        _compile_nodes(process, compiler, code, ast)
    else:
        _compile_node(process, compiler, code, ast)


def _compile_nodes(process, compiler, code, ast):
    length = plist.length(ast)
    if length > 1:
        nodes_except_last = plist.slice(ast, 0, length - 1)
        for node in nodes_except_last:
            _compile(process, compiler, code, node)
            _emit_pop(code)

    if length > 0:
        last_node = plist.nth(ast, length - 1)
        _compile(process, compiler, code, last_node)

    return
    nodes = ast.items

    if len(nodes) > 1:
        for node in nodes[:-1]:
            _compile(process, compiler, code, node)
            _emit_pop(code)

    if len(nodes) > 0:
        node = nodes[-1]
        _compile(process, compiler, code, node)


def _compile_node(process, compiler, code, node):
    ntype = node_type(node)

    if NT_TRUE == ntype:
        _compile_TRUE(process, compiler, code, node)
    elif NT_FALSE == ntype:
        _compile_FALSE(process, compiler, code, node)
    elif NT_NIL == ntype:
        _compile_NIL(process, compiler, code, node)
    elif NT_INT == ntype:
        _compile_INT(process, compiler, code, node)
    elif NT_FLOAT == ntype:
        _compile_FLOAT(process, compiler, code, node)
    elif NT_STR == ntype:
        _compile_STR(process, compiler, code, node)
    elif NT_CHAR == ntype:
        _compile_CHAR(process, compiler, code, node)
    elif NT_NAME == ntype:
        _compile_NAME(process, compiler, code, node)
    elif NT_SPECIAL_NAME == ntype:
        _compile_SPECIAL_NAME(process, compiler, code, node)
    elif NT_SYMBOL == ntype:
        _compile_SYMBOL(process, compiler, code, node)

    elif NT_DEF == ntype:
        _compile_DEF(process, compiler, code, node)

    elif NT_IF == ntype:
        _compile_IF(process, compiler, code, node)
    elif NT_WHEN == ntype:
        _compile_WHEN(process, compiler, code, node)
    elif NT_MATCH == ntype:
        _compile_MATCH(process, compiler, code, node)
    elif NT_TRY == ntype:
        _compile_TRY(process, compiler, code, node)

    elif NT_LOAD == ntype:
        _compile_LOAD(process, compiler, code, node)
    elif NT_MODULE == ntype:
        _compile_MODULE(process, compiler, code, node)
    elif NT_TRAIT == ntype:
        _compile_TRAIT(process, compiler, code, node)
    elif NT_GENERIC == ntype:
        _compile_GENERIC(process, compiler, code, node)
    elif NT_SPECIFY == ntype:
        _compile_SPECIFY(process, compiler, code, node)

    elif NT_RETURN == ntype:
        _compile_RETURN(process, compiler, code, node)
    elif NT_THROW == ntype:
        _compile_THROW(process, compiler, code, node)

    elif NT_BREAK == ntype:
        _compile_BREAK(process, compiler, code, node)
    elif NT_CONTINUE == ntype:
        _compile_CONTINUE(process, compiler, code, node)
    elif NT_FOR == ntype:
        _compile_FOR(process, compiler, code, node)
    elif NT_WHILE == ntype:
        _compile_WHILE(process, compiler, code, node)

    elif NT_CALL == ntype:
        _compile_CALL(process, compiler, code, node)
    elif NT_CALL_MEMBER == ntype:
        _compile_CALL_MEMBER(process, compiler, code, node)

    elif NT_LIST == ntype:
        _compile_LIST(process, compiler, code, node)
    elif NT_TUPLE == ntype:
        _compile_TUPLE(process, compiler, code, node)
    elif NT_MAP == ntype:
        _compile_MAP(process, compiler, code, node)

    elif NT_LOOKUP == ntype:
        _compile_LOOKUP(process, compiler, code, node)
    elif NT_LOOKUP_SYMBOL == ntype:
        _compile_LOOKUP_SYMBOL(process, compiler, code, node)

    elif NT_MODIFY == ntype:
        _compile_MODIFY(process, compiler, code, node)
    elif NT_CONS == ntype:
        _compile_CONS(process, compiler, code, node)

    elif NT_IN == ntype:
        _compile_IN(process, compiler, code, node)
    elif NT_NOTIN == ntype:
        _compile_NOTIN(process, compiler, code, node)
    elif NT_IS == ntype:
        _compile_IS(process, compiler, code, node)
    elif NT_ISNOT == ntype:
        _compile_ISNOT(process, compiler, code, node)
    elif NT_ISA == ntype:
        _compile_ISA(process, compiler, code, node)
    elif NT_NOTA == ntype:
        _compile_NOTA(process, compiler, code, node)
    elif NT_KINDOF == ntype:
        _compile_KINDOF(process, compiler, code, node)

    elif NT_AND == ntype:
        _compile_AND(process, compiler, code, node)
    elif NT_OR == ntype:
        _compile_OR(process, compiler, code, node)
    elif NT_NOT == ntype:
        _compile_NOT(process, compiler, code, node)
    elif NT_EQ == ntype:
        _compile_EQ(process, compiler, code, node)
    elif NT_LE == ntype:
        _compile_LE(process, compiler, code, node)
    elif NT_GE == ntype:
        _compile_GE(process, compiler, code, node)
    elif NT_NE == ntype:
        _compile_NE(process, compiler, code, node)
    elif NT_BITAND == ntype:
        _compile_BITAND(process, compiler, code, node)
    elif NT_BITNOT == ntype:
        _compile_BITNOT(process, compiler, code, node)
    elif NT_BITOR == ntype:
        _compile_BITOR(process, compiler, code, node)
    elif NT_BITXOR == ntype:
        _compile_BITXOR(process, compiler, code, node)
    elif NT_SUB == ntype:
        _compile_SUB(process, compiler, code, node)
    elif NT_ADD == ntype:
        _compile_ADD(process, compiler, code, node)
    elif NT_MUL == ntype:
        _compile_MUL(process, compiler, code, node)
    elif NT_DIV == ntype:
        _compile_DIV(process, compiler, code, node)
    elif NT_MOD == ntype:
        _compile_MOD(process, compiler, code, node)
    elif NT_LT == ntype:
        _compile_LT(process, compiler, code, node)
    elif NT_GT == ntype:
        _compile_GT(process, compiler, code, node)

    elif NT_RSHIFT == ntype:
        _compile_RSHIFT(process, compiler, code, node)
    elif NT_URSHIFT == ntype:
        _compile_URSHIFT(process, compiler, code, node)
    elif NT_LSHIFT == ntype:
        _compile_LSHIFT(process, compiler, code, node)

    elif NT_UNARY_PLUS == ntype:
        _compile_UNARY_PLUS(process, compiler, code, node)
    elif NT_UNARY_MINUS == ntype:
        _compile_UNARY_MINUS(process, compiler, code, node)

    elif NT_GOTO == ntype:
        _compile_GOTO(process, compiler, code, node)

    elif NT_ASSIGN == ntype:
        _compile_ASSIGN(process, compiler, code, node)
    else:
        compile_error(process, compiler, code, node, u"Unknown node")


def newcode(compiler):
    return CodeSource(SourceInfo(compiler.source_path, compiler.source))


def compile_ast(process, compiler, ast):
    code = newcode(compiler)
    _enter_scope(process, compiler)
    _declare_arguments(process, compiler, 0, False)
    _compile(process, compiler, code, ast)
    scope = _current_scope(process, compiler)
    final_scope = scope.finalize()
    _exit_scope(process, compiler)
    compiled_code = code.finalize_compilation(final_scope)
    return compiled_code


def compile(process, src, sourcename):
    ast = parser.parse_string(src)
    # print ast
    compiler = Compiler(sourcename, src)
    code = compile_ast(process, compiler, ast)
    return code


def compile_module(process, modulename, src, sourcename):
    code = compile(process, src, sourcename)
    module = space.newmodule(modulename, code, None)
    return module


def compile_function_source(process, src, name):
    code = compile(process, src, name)
    fn = space.newfuncsource(name, code)
    return fn


def print_code(code):
    from code.opcode import opcode_to_str
    print "\n".join([str((opcode_to_str(c[0]), str(c[1:]))) for c in code.opcodes])

# CODE = compile(None, PATTERN_DATA)
# CODE = compile(None, """
#     A[1.._];
#     A[2..3];
#     A[_.._];
#     A[_..4];
#     A[5];
# """)
# print_code(CODE)
