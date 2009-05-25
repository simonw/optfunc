import optfunc

@optfunc.run
def foo(filename, v = optfunc.Str('-v', '--version')):
    "Usage: %s foo bar - do something useful"
    pass
