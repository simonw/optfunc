import optfunc

@optfunc.run
def foo(filename, v = optfunc.String('-v', '--version')):
    "Usage: %s foo bar - do something useful"
    pass
