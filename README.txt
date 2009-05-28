optfunc
=======

Parse command line options in Python using function introspection.

I can never remember how to use any of Python's regular command line parsing
libraries.

optfunc uses introspection to make a Python function available as a command
line utility. It's syntactic sugar around optparse from the standard library.

Very early stages at the moment. Here's what the API looks like so far:

    import optfunc
    
    def upper(filename, verbose = False):
        "Usage: %s <filename> [--verbose] - output file content in uppercase"
        s = open(filename).read()
        if verbose:
            print "Processing %s bytes..." % len(s)
        print s.upper()
    
    if __name__ == '__main__':
        optfunc.run(upper)
        run(upper)

And here's the resulting command-line interface:

    $ python demo.py -h
    Usage: demo.py <filename> [--verbose] - output file content in uppercase

    Options:
      -h, --help     show this help message and exit
      -v, --verbose  

TODO: Support for different types of argument, *args and **kwargs, and more.
