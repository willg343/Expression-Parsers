"""
Changed the fully regex-based approach to expression calculation and testing, making it only a part of the replacement algorithm.
The testing algorithm now relies on arrays.
Development in progress.
"""

import re, operator

signs = {'+':operator.add, '-':operator.sub, '*': operator.mul, '/': operator.truediv, '%': operator.mod}
convert = lambda inp: re.sub(r'[+-]+', lambda signs: ('+','-')[signs[0].count('-')%2], inp.replace(' ',''))
calculate = lambda num1, op, num2:  str(float(signs[op](float(num1), float(num2))))
PATTERN = re.compile(r"((?:(?:(?<=^)|(?<=[*/%+-]))[-+])?\d+(?:\.\d+)?(?:e-?\d+)?|[*/%+-])")

def process(split_exp, default_signs = '+-', idx = 0):
    while 1:
        if idx==len(split_exp)-1: return split_exp if default_signs == '+-' else process(split_exp)
        if split_exp[idx+1] in default_signs:
            split_exp[idx:idx+3] = [calculate(*split_exp[idx:idx+3])]
            continue
        idx+=1
        
def calc(exp):
    while '(' in exp or ')' in exp:
        exp = re.sub(r'[(]([^()]+)[)]', lambda x:''.join(process(PATTERN.findall(x[1]), '*/%')), convert(exp))
    return float(process(PATTERN.findall(convert(exp)),'*/%')[0])
