optfunc
=======

Parse command line options in Python using function introspection.

I can never remember how to use any of Python's regular command line parsing
libraries.

optfunc uses introspection to make a Python function available as a command
line utility. It's syntactic sugar around optparse from the standard library.

Very early stages at the moment. Here's what the API looks like so far:

    import optfunc
    
    def upper(filename, v = optfunc.Str('-v', '--version')):
        "Usage: %s foo bar - do something useful"
        print open(filename).read().upper()
    
    if __name__ == '__main__':
        optfunc.run(upper)

TODO: Support for different types of argument, *args and **kwargs, and more.
