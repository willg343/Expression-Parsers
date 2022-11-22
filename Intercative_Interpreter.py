import re

vals,signs = {},{'/':float.__truediv__,'*':float.__mul__,'+':float.__add__,'-':float.__sub__,'%':float.__mod__}

def rep(e):
    (a,b),(c,d) = ((i[0]=='-',i.strip('-')) for i in e.groups()[::2])
    return str(signs.get(e[2])((1,-1)[a]*float(vals.get(b,b)),(1,-1)[c]*float(vals.get(d,d))))

calcs = (('%*/',r'(-?\w+(?:\.\d+)?(?:e-?\d+)?) ([%/*]) (-?\w+(?:\.\d+)?(?:e-?\d+)?)',rep),
         ('+-',r'(-?\w+(?:\.\d+)?(?:e-?\d+)?) ([+-]) (-?\w+(?:\.\d+)?(?:e-?\d+)?)',rep))

def calc(st):
    exp = re.sub(r'(?<=[)\w+*%/-])(?=[+*%/-])|(?<=[\w)][+*%/-])(?=[\w(+*%/-])',' ',st.replace(' ',''));print(exp)
    while '(' in exp:
        
        s,n,b = re.search(r'((-?\d*)\(([^()]*)\))',exp).groups()        
        exp = exp.replace(s,str(int(n and (n,-1)[n=='-'] or 1)*compute(b)))
    
    return float(exp) if re.match(r'-?\d+(\.\d+)?(e-?\d+)?$',exp) else compute(exp)

def compute(exp):   
    for a,b,c in calcs:
        while any(i in exp for i in a) and re.match(r'(-?\w+(?:\.\d+)?(?:e-?\d+)? [+/*%-] )+',exp):
            exp = re.sub(b,c,exp,1)
    return (1,-1)[exp[0]=='-']*float(vals.get(exp.strip('-'),exp.strip('-')))

class Interpreter:
    @staticmethod
    def input(e):
        if re.search(r'\w\s+\w',e): raise Exception

        var = re.match(r'([A-Za-z]\w*)=(.+)$',e.replace(' ',''))
        if var:
            vals.update({var[1]:calc(var[2])})
            return vals[var[1]]
            
        return '' if e.isspace() or not e else calc(e)
