from optfunc import run, Str

def foo(filename, v = Str('-v', '--version')):
    "Usage: %s foo bar - do something useful"
    pass

if __name__ == '__main__':
    run(foo)