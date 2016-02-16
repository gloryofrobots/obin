from jinja2 import Template
def render(body, data):
    tpl = Template(body)
    return tpl.render(data)

I = "Int"
N = "Number"
F = "Float"
A = "Any"
V = "Vector"
T = "Tuple"
L = "List"
S = "String"
M = "Map"

def arg(index):
    return dict(name="arg%d" % index, index=index, source_index=index)

def generic(name, script_name, implementations, hot_path):
    g = dict(name=name, script_name=script_name, implementations=implementations, hot_path=hot_path)
    if g['implementations']:
        for f in g['implementations']:
            f['generic'] = g
    return g

def impl(types, args, func_name, wrapper_name=None, module_name="operations", process_as_0_arg=True):
    return dict(types=types, args=args, func_name=func_name,
                wrapper_name=wrapper_name if wrapper_name else func_name,
                module_name=module_name, process_as_0_arg=process_as_0_arg)

def unary(t, *args, **kwargs):
    return impl((t,), [arg(0)], *args, **kwargs)

def binary(t1, t2, *args, **kwargs):
    return impl((t1,t2), [arg(0), arg(1)], *args, **kwargs)

   




def hotpath_name(name):
    return 'hp_%s' % name 

def print_implementations(generics):
    print "    # ---------------AUTOGENERATED---------------------"
    TPL_IMPL = """
    @complete_native_routine
    def builtin_{{wrapper_name}}(process, routine):
        {% for arg in args %}{{arg.name}} = routine.get_arg({{arg.index}}) 
        {% endfor %}
        return {{module_name}}.{{func_name}}({%if process_as_0_arg %}process,{% endif %}{% for arg in args|sort(attribute='source_index') %}{{arg.name}}{% if not loop.last %}, {% endif %}{% endfor %})
    """

    for G in generics:
        if not G['implementations']:
            continue
        for func in G['implementations']:
            print render(TPL_IMPL, func)


def print_declarations(generics):
    print "        # ---------------AUTOGENERATED---------------------"
    TPL_HOT = "        self.%s = newgeneric_hotpath(symbols.symbol(u\"%s\"), hotpath.%s)"
    TPL = "        self.%s = newgeneric(symbols.symbol(u\"%s\"))"
    for G in generics:
        varname = G['name']
        funcname = G['script_name']
        impls = G['implementations']
        hot_path = G['hot_path']
        if not hot_path:
            print TPL % (varname, funcname)
        else:
            print TPL_HOT % (varname, funcname, hotpath_name(varname))

def print_builtin_puts(generics):
    print "        # ---------------AUTOGENERATED---------------------"
    for G in generics:
        varname = G['name']
        S = "    api.put(module, generics.%s.name, generics.%s)" % (varname, varname)
        print S

    
def print_reify(generics):
    print "    # ---------------AUTOGENERATED---------------------"
    REIFY_TPL = """
    specify_single(process, generics.{{generic.name}},
                     newtuple([{% for type in types %}traits.{{type}}, {% endfor %}]),
                     newnativefunc(newsymbol(process, u"{{func_name}}"), wrappers.builtin_{{func_name}}, {{types|length}}))
    """
    for G in generics:
        for impl in G["implementations"]:
            print render(REIFY_TPL, impl)

GENERICS = [
    generic("uplus", "__uplus__", [
            unary(N, "uplus_n"),
    ], True),
    generic("uminus", "__uminus__", [
            unary(I, "uminus_i"),
            unary(F, "uminus_f"),
            unary(N, "uminus_n"),
    ], True),
    generic("not_", "not", [
            unary(A, "not_w"),
    ], True),
    generic("eq", "==", [
            binary(A,A, "eq_w"),
    ], True),
    generic("ne", "!=", [
            binary(A, A, "noteq_w"),
    ], True),
    generic("in_", "in", [
            binary(A, A, "in_w"),
    ], True),
    generic("notin", "notin", [
            binary(A, A, "notin_w"),
    ], True),
    generic("compare", "compare", None, False),
    generic("add", "+", [
            binary(I,I, "add_i_i", module_name='number'),
            binary(F,F, "add_f_f", module_name='number'),
            binary(N,N, "add_n_n", module_name='number'),
    ], True),
    generic("sub", "-", [
            binary(I,I, "sub_i_i", module_name='number'),
            binary(F,F, "sub_f_f", module_name='number'),
            binary(N,N, "sub_n_n", module_name='number'),
    ], True),
     generic("mul", "*", [
            binary(I,I, "mul_i_i", module_name='number'),
            binary(F,F, "mul_f_f", module_name='number'),
            binary(N,N, "mul_n_n", module_name='number'),
    ], True),
    generic("div", "/", [
            binary(I,I, "div_i_i", module_name='number'),
            binary(F,F, "div_f_f", module_name='number'),
            binary(N,N, "div_n_n", module_name='number'),
    ], True),
    generic("mod", "%", [
            binary(F,F, "mod_f_f", module_name='number'),
            binary(N,N, "mod_n_n", module_name='number'),
    ], True),
   
    generic("gt", ">", [
            binary(I,I, "compare_gt_i_i", module_name='number'),
            binary(F,F, "compare_gt_f_f", module_name='number'),
            binary(N,N, "compare_gt_n_n", module_name='number'),
    ], True),
    generic("ge", ">=", [
            binary(I,I, "compare_ge_i_i", module_name='number'),
            binary(F,F, "compare_ge_f_f", module_name='number'),
            binary(N,N, "compare_ge_n_n", module_name='number'),
    ], True),
     generic("le", "<=", [
            binary(I,I, "compare_le_i_i", module_name='number'),
            binary(F,F, "compare_le_f_f", module_name='number'),
            binary(N,N, "compare_le_n_n", module_name='number'),
    ], True),
    generic("lt", "<", [
            binary(I,I, "compare_lt_i_i", module_name='number'),
            binary(F,F, "compare_lt_f_f", module_name='number'),
            binary(N,N, "compare_lt_n_n", module_name='number'),
    ], True),
    generic("bitnot", "~", [
           unary(I, "bitnot_i", module_name='number'),
    ], True),
    generic("bitor", "|", [
           unary(I, "bitor_i_i", module_name='number'),
    ], True),
    generic("bitxor", "^", [
           unary(I, "bitxor_i_i", module_name='number'),
    ], True),
    generic("bitand", "&", [
           unary(I, "bitand_i_i", module_name='number'),
    ], True),
    generic("lsh", "<<", [
           binary(I,I, "lsh_i_i", module_name='number'),
    ], True),
    generic("rsh", ">>", [
           binary(I,I, "rsh_i_i", module_name='number'),
    ], True),
    generic("ursh", ">>>", [
           binary(I,I, "ursh_i_i", module_name='number'),
    ], True),
    generic("cons", "::", [
            binary(L, L, "cons", module_name="plist", process_as_0_arg=False),
    ], True),
    generic("concat", "++", [
            binary(L, L, "concat", wrapper_name='concat_l', module_name="plist", process_as_0_arg=False),
            binary(S, S, "concat", wrapper_name='concat_s', module_name="string", process_as_0_arg=False),
            binary(T, T, "concat", wrapper_name='concat_t', module_name="tupl", process_as_0_arg=False),
    ], True),
]


print_declarations(GENERICS)

# print_implementations(GENERICS)
# print_builtin_puts(GENERICS)
# print_reify(GENERICS)
