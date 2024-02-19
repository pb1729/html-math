import unicodedata

# Constants
GREEK_LETTERS = set(list('ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω'))

MATH_FORMULA = 'math-formula'
MATH_FORMULA_ROOT = 'math-formula-root'
MATH_TABLE = 'math-table'
MATH_MATRIX = 'math-matrix'
MATH_BOX_MATRIX = 'math-box-matrix'
MATH_FRACTION = 'math-fraction'
MATH_SS = 'math-ss'
MATH_NARY = 'math-nary'

SIZE_MULTIPLIERS = {
    # Note: These should be kept consistent with the definitions in html_math.css!
    MATH_FRACTION: 0.75,
    MATH_SS: 0.67,
    MATH_NARY: 0.67,
}

LATEX_SYMBOL_TABLE = {
    "¬": "neg",
    "⊺": "top",
    "⟂": "bot",
    "∨": "lor",
    "∧": "land",
    "⇒": "implies",
    "⇔": "iff",
    "☐": "Box",
    "∇": "nabla",
    "ℝ": "mathbb{R}",
    "𝓛": "mathcal{L}",
    "→": "to",
    "≤": "leq",
    "≥": "geq",
    "⟨": "langle",
    "⟩": "rangle",
    "~": "sim",
}

LATEX_NARY_SYMBOL_TABLE = {
    "∑": "sum",
    "∏": "prod",
    "∫": "int",
    # more here if needed: http://xahlee.info/comp/unicode_math_operators.html
}

def greek_letter_to_latex(letter):
    words = unicodedata.name(letter).split(" ")
    ans = words[-1].casefold()
    if "CAPITAL" in words:
        return words[-1][0] + ans[1:]
    else:
        return ans
LATEX_GREEK_LETTER_TABLE = {}
for letter in GREEK_LETTERS:
    LATEX_GREEK_LETTER_TABLE[letter] = greek_letter_to_latex(letter)


def html_escape(s):
    return (s
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace(' ', '&nbsp;')
    )


def html_tag(tag, classes, content, attribs=''):
    class_list = ' '.join(classes)
    return '<%s class="%s"%s>%s</%s>' % (tag, class_list, attribs, content, tag)

class BaseMath:
    ''' Base class for representing math. '''
    def to_raw(self):
        return '<b>&nbsp;UNIMPLEMENTED&nbsp;</b>'
    def to_latex(self):
        return '\\text{ UNIMPLEMENTED }'
    def est_height(self):
        return 1.

class ListMath(BaseMath):
    ''' Math data consisting of a tree of chunks of math that can be concatenated together. '''
    def __init__(self, maths=None):
        if maths is not None:
            self.maths = maths
        else:
            self.maths = []
    def to_raw(self):
        return ''.join([math.to_raw() for math in self.maths])
    def to_latex(self):
        return ''.join([math.to_latex() for math in self.maths])
    def est_height(self):
        if len(self.maths) == 0: return 0.01
        return max(math.est_height() for math in self.maths)
    def add(self, x):
        self.maths.append(x)

class ArrayMath(ListMath):
    ''' Array of math data, mainly intended for consumption by functions rather than direct use. '''
    def to_raw(self):
        return '[%s]' % (', '.join([math.to_raw() for math in self.maths]))
    def to_latex(self):
        return '\\left[%s\\right]' % (', '.join([math.to_latex() for math in self.maths]))

class RootFormulaMath(BaseMath):
    ''' Top level class that is the root holding an entire formula. '''
    def __init__(self, math):
        self.math = math
    def to_raw(self):
        return html_tag('span', [MATH_FORMULA_ROOT, MATH_FORMULA], self.math.to_raw())
    def to_latex(self):
        return self.math.to_latex()
    def est_height(self):
        return self.math.est_height()

class VariableMath(BaseMath):
    ''' Math data that just consists of a variable. '''
    def __init__(self, varnm):
        self.varnm = varnm
        self.i = True
        self.b = False
    def to_raw(self):
        ans = html_escape(self.varnm)
        if self.b: ans = '<b>%s</b>' % ans
        if self.i: ans = '<i>%s</i>' % ans
        return ans
    def to_latex(self):
        if self.varnm in LATEX_GREEK_LETTER_TABLE:
            return "\\%s " % LATEX_GREEK_LETTER_TABLE[self.varnm]
        if self.b: return "\\mathbf{%s}" % self.varnm
        return self.varnm

class RegularMath(BaseMath):
    ''' Math data that consists of some other symbol that isn't a variable. '''
    def __init__(self, symb):
        self.symb = symb
    def to_raw(self):
        return html_escape(self.symb)
    def to_latex(self):
        if self.symb in LATEX_SYMBOL_TABLE:
            return "\\%s " % LATEX_SYMBOL_TABLE[self.symb]
        elif self.symb in LATEX_NARY_SYMBOL_TABLE:
            return "\\%s " % LATEX_NARY_SYMBOL_TABLE[self.symb]
        elif all([is_variable(c) for c in self.symb]):
            return "\\text{%s}" % self.symb
        else:
            return self.symb

class TableMath(BaseMath):
    ''' Represents a wide variety of possible notations, matrices, fractions, super/sub-scripts, etc. '''
    def __init__(self, rows, *classes):
        self.rows = rows
        self.classes = [MATH_TABLE] + list(classes)
    def to_raw(self):
        ans = []
        for i, row in enumerate(self.rows):
            ans.append('<tr>')
            for elem in row:
                ans.append('<td>')
                ans.append(html_tag('span', [MATH_FORMULA], elem.to_raw()))
                ans.append('</td>')
            ans.append('</tr>')
        return html_tag('table', self.classes, ''.join(ans))
    def to_latex(self):
        def is_empty(math):
            return isinstance(math, RegularMath) and math.symb == " "
        if MATH_NARY in self.classes:
            rows = [row[0] for row in self.rows]
            if len(rows) == 1:   sup, symb, sub = None, *rows, None
            elif len(rows) == 2: sup, symb, sub = None, *rows
            elif len(rows) == 3: sup, symb, sub = rows
            else: raise ValueError("unsupported n-ary number of rows")
            ans = symb.to_latex()
            if sub is not None: ans += "_{%s}" % sub.to_latex()
            if sup is not None: ans += "^{%s}" % sup.to_latex()
            return ans
        if MATH_SS in self.classes:
            ans = ""
            sup = self.rows[0][0]
            sub = self.rows[1][0]
            if not is_empty(sup):
                ans += "^{%s}" % sup.to_latex()
            if not is_empty(sub):
                ans += "_{%s}" % sub.to_latex()
            return ans
        elif MATH_FRACTION in self.classes:
            return "\\frac{%s}{%s}" % (self.rows[0][0].to_latex(), self.rows[1][0].to_latex())
        else: # make a table
            ans = ["\\begin{pmatrix}"] # for now only pmatrix is supported :/
            for i, row in enumerate(self.rows):
                ans.append(" & ".join([elem.to_latex() for elem in row]))
                ans.append(" \\\\")
            ans.append("\\end{pmatrix}")
            return "".join(ans)
    def est_height(self):
        multiplier = 1.
        for cls in self.classes:
            if cls in SIZE_MULTIPLIERS:
                multiplier *= SIZE_MULTIPLIERS[cls]
        return multiplier * sum(
            max(math.est_height() for math in row)
            for row in self.rows
        )

class ScaleMath(BaseMath):
    ''' Scales the math it contains by a fixed amount. '''
    def __init__(self, math, scale):
        self.math = math
        self.scale = scale
    def to_raw(self):
        percent_scale = int(100 * self.scale)
        style_str = ' style="font-size:%d%s;"' % (percent_scale, '%')
        return html_tag('span', [MATH_FORMULA], self.math.to_raw(), style_str)
    def to_latex(self): # do nothing
        return self.math.to_latex()
    def est_height(self):
        return self.scale * self.math.est_height()

def unpack_math_type(math, typ):
    if isinstance(math, typ):
        return math
    elif isinstance(math, ListMath) and len(math.maths) == 1 and isinstance(math.maths[0], typ):
        return math.maths[0]
    else:
        raise Exception('Error: Expected %s or a ListMath containing it, but got %s.'
            % (typ.__name__, type(math).__name__))

def array_args_to_rows(args):
    rows = []
    for arg in args:
        row_array = unpack_math_type(arg, ArrayMath)
        rows.append(row_array.maths)
    return rows

def table(*args):
    return TableMath(array_args_to_rows(args))

def matrix(*args):
    return TableMath(array_args_to_rows(args), MATH_MATRIX)

def box_matrix(*args):
    return TableMath(array_args_to_rows(args), MATH_MATRIX, MATH_BOX_MATRIX)

def fraction(a, b):
    return TableMath([[a], [b]], MATH_FRACTION)

def ss(a, b):
    return TableMath([[a], [b]], MATH_SS)

def superscript(a):
    return ss(a, RegularMath(' '))

def subscript(b):
    return ss(RegularMath(' '), b)

def at(_):
    return RegularMath('@')

def vector_font(x):
    v = unpack_math_type(x, VariableMath)
    v.b = True
    return v

def matrix_font(x):
    v = unpack_math_type(x, VariableMath)
    v.i = False
    v.b = True
    return v

def surround(left, middle, right):
    scale_factor = middle.est_height()
    return ListMath([
        ScaleMath(left, scale_factor),
        middle,
        ScaleMath(right, scale_factor)
    ])

def n_ary(symb, lower=None, upper=None):
    ''' n-ary sum, n-ary product, etc. '''
    contents = [[ScaleMath(symb, 2.4)]]
    if lower is not None: contents = contents + [[lower]]
    if upper is not None: contents = [[upper]] + contents
    return TableMath(contents, MATH_NARY)

fn_table = {
    'tab': table,
    'mat': matrix,
    'box': box_matrix,
    'fr': fraction,
    'ss': ss,
    '^': superscript,
    '_': subscript,
    'at': at,
    'v': vector_font,
    'M': matrix_font,
    'p': surround,
    'na': n_ary,
}

class CallMath(BaseMath):
    ''' Math that consists of a call to some function. '''
    def __init__(self, fun, args):
        self.fun = fun
        self.args = args
        self.result = None
    def compute_result(self):
        if self.result is None:
            if self.fun in fn_table:
                self.result = fn_table[self.fun](*self.args)
            else:
                # all other functions (eg. exp, sin, cos, mod) will be non-italic text
                self.result = ListMath([RegularMath(self.fun), *self.args])
    def to_raw(self):
        self.compute_result()
        return self.result.to_raw()
    def to_latex(self):
        self.compute_result()
        return self.result.to_latex()
    def est_height(self):
        self.compute_result()
        return self.result.est_height()


def is_variable(c):
    return (ord('a') <= ord(c) <= ord('z')) or (ord('A') <= ord(c) <= ord('Z')) or (c in GREEK_LETTERS)

def ERR(i, s, msg):
    return Exception('Error around "%s": %s' % (s[i-4:i+4], msg))

def get_function_name(s, i_at):
    i = i_at + 1
    i_open_in_slice = s[i:].find('«') # indexes s[i:]
    if i_open_in_slice == -1: raise ERR(i, s, 'Expected to find a "«".')
    i_open = i + i_open_in_slice # indexes s
    function_name = s[i:i_open]
    if '@' in function_name: raise ERR(i, s, 'Did not expect a function name containing "@".')
    if '»' in function_name: raise ERR(i, s, 'Did not except a function name containing "»".')
    if ' ' in function_name: raise ERR(i, s, 'Did not except a function name containing " ".')
    return i_open, function_name    

def parse(s, arglist=None, depth=0):
    ''' Parse a string into a tree of BaseMath objects.
    Return behavior depends on depth:
        - depth = 0 : return the Math object parsed from the string s
        - depth > 0 : return the index into the string s from which parsing should continue
    '''
    i = 0
    curr_arg = ListMath()
    while i < len(s):
        if s[i] == '@':
            i, function_name = get_function_name(s, i)
            i += 1
            callee_arglist = []
            i += parse(s[i:], callee_arglist, depth + 1)
            curr_arg.add(CallMath(function_name, callee_arglist))
        elif s[i] == '«':
            i += 1
            array_arglist = []
            i += parse(s[i:], array_arglist, depth + 1)
            curr_arg.add(ArrayMath(array_arglist))
        elif s[i] == '⎖':
            if depth == 0:
                raise ERR(i, s, 'Unenclosed "⎖".')
            arglist.append(curr_arg)
            curr_arg = ListMath()
            i += 1
        elif s[i] == '»':
            if depth == 0:
                raise ERR(i, s, 'Encountered "»" with no corresponding "«".')
            arglist.append(curr_arg)
            return i + 1
        else:
            if is_variable(s[i]):
                curr_arg.add(VariableMath(s[i]))
            else:
                curr_arg.add(RegularMath(s[i]))
            i += 1
    if depth > 0:
        raise ERR(i, s, 'Reached end of string without closing all delimiters.')
    return RootFormulaMath(curr_arg)
            

def html_math(s):
    return parse(s).to_raw()

def latex_math(s):
    return parse(s).to_latex()

