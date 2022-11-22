import re,operator

signs = {'/':operator.truediv,'*':operator.mul,'+':operator.add,'-':operator.sub}
ret,rep = lambda c: re.match(r'\d+$',c) and int(c) or float(c),\
          lambda c:str(signs.get(c[2])(float(c[1]),float(c[3])))
calcs = [ 
('*/',r'(-?\d+(?:\.\d+)?(?:e-?\d+)?) ([/*]) (-?\d+(?:\.\d+)?(?:e-?\d+)?)',rep),
('+-',r'(-?\d+(?:\.\d+)?(?:e-?\d+)?) ([+-]) (-?\d+(?:\.\d+)?(?:e-?\d+)?)',rep)
]

def calc(st):
    
    exp = re.sub(r'(?<=[)\d+*%/-])(?=[+*%/-])|(?<=[\d)][+*%/-])(?=[\d(+*%/-])',' ',st.replace(' ',''))

    while '(' in exp:
        
        s,s1,s2 = re.search(r'((-?)\(([^()]*)\))',exp).groups()        
        exp = exp.replace(s,str(int((1,-1)[s1=='-'])*float(compute(s2))))

    return ret(exp) if re.match(r'-?\d+(\.\d+)?(e-?\d+)?$',exp) else ret(compute(exp))


def compute(exp):   

    for a,b,c in calcs:
        while any(i in exp for i in a) and not re.match(r'-?\d+(\.\d+)?(e-?\d+)?$',exp):
            exp = re.sub(b,c,exp,1)

    return exp if exp else ''
