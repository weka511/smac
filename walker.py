from os import walk
from re import match

def get_python(files):
    return [file for file in files if file.endswith('.py')]

n      = 0
name   = ''
header = 'https://github.com/weka511/smac/tree/master/'
nbsp   = '&nbsp;'
Lines  = {}
for i in range(9):
    Lines[i+1]=[]
for root,d,files in walk('.'):
    if root.startswith(r'.\.git'): continue
    m = match(r'\.\\((homework)|(lecture)|(tutorial))_(\d+)$',root)
    if m:
        name = m.group(1)
        n    = int(m.group(5))

    if n>0:
        for i,file in enumerate(get_python(files)):
            if i==0:
                Lines[n].append(f'{n}|[{name.title()}]({header}{name}_{n})|{file}|')
            else:
                Lines[n].append (f'{nbsp}|{nbsp}|{file}|')

for key,value in Lines.items():
    for v in value:
        print (v)
