from pinsert import pinsert

v=10
s=30
t=s/v
vars = {
    'velocity': v,
    'time': t,
    'distance': s,
    'name': 'andrey'
}

pinsert('tex/test.tex', vars, crash_on_error=False)
