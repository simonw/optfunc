from optfunc import run, Str

def upper(filename, v = Str('-v', '--version')):
    "Usage: %s foo bar - do something useful"
    print open(filename).read().upper()

if __name__ == '__main__':
    run(upper)
