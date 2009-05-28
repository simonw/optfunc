import optfunc

def upper(filename, verbose = False):
    "Usage: %prog <filename> [--verbose] - output file content in uppercase"
    s = open(filename).read()
    if verbose:
        print "Processing %s bytes..." % len(s)
    print s.upper()

if __name__ == '__main__':
    optfunc.run(upper)
