import optfunc

@optfunc.run
def foo(filename, v = optfunc.Switch('-v', '--version')):
    "Usage: %s foo bar - do something useful"
    pass
