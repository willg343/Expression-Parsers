import re
from operator import add, sub, mul, mod, truediv

vars, signs = dict(), {'+':add, '-':sub, '*': mul, '/': truediv,'%': mod}
convert = lambda inp: re.sub(r'[+-]+', lambda signs: ('+','-')[signs[0].count('-')%2], inp.replace(' ',''))
calculate = lambda n1, op, n2:  str(float(signs[op](float(vars.get(n1, n1)), float(vars.get(n2, n2)))))
PATTERN = re.compile(r"((?:(?:(?<=^)|(?<=[*/%+-]))[-+])?\w+(?:\.\d+)?(?:e-?\d+)?|[*/%+-])")


def process(split_exp, default_signs = '+-', idx = 0):
    while 1:
        if idx==len(split_exp)-1: return split_exp if default_signs == '+-' else process(split_exp)
        if split_exp[idx+1] in default_signs:
            split_exp[idx:idx+3] = [calculate(*split_exp[idx:idx+3])]
            continue
        idx+=1

def calc(exp):
    while '(' in exp or ')' in exp:
        exp = re.sub(r'[(]([^()]+)[)]', lambda x:''.join(process(PATTERN.findall(x[1]), '%/*')), convert(exp))
    result = process(PATTERN.findall(convert(exp)),'%/*')[0]
    return float(vars.get(result,result))
 
class Interpreter:
    @staticmethod
    def input(exp):
        if re.search(r'\w\s+\w',exp): raise Exception

        var = re.match(r'([A-Za-z]\w*)=(.+)$',exp.replace(' ',''))
        if var:
            vars.update({var[1]:calc(var[2])})
            return vars[var[1]]

        return '' if exp.isspace() or not exp else calc(exp)
