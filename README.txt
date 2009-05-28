optfunc
=======

Parse command line options in Python using function introspection.

Post feedback here: http://simonwillison.net/2009/May/28/optfunc/

I can never remember how to use any of Python's regular command line parsing
libraries.

optfunc uses introspection to make a Python function available as a command
line utility. It's syntactic sugar around optparse from the standard library.

Here's what the API looks like so far:

    import optfunc
    
    def upper(filename, verbose = False):
        "Usage: %prog <file> [--verbose] - output file content in uppercase"
        s = open(filename).read()
        if verbose:
            print "Processing %s bytes..." % len(s)
        print s.upper()
    
    if __name__ == '__main__':
        optfunc.run(upper)

And here's the resulting command-line interface:

    $ python demo.py --help
    Usage: demo.py <filename> [--verbose] - output file content in uppercase
    
    Options:
      -h, --help     show this help message and exit
      -v, --verbose  

optfunc also supports two decorators for stuff I couldn't work out how to 
shoehorn in to a regular function definition. geocode.py shows them in action:

    @optfunc.notstrict
    @optfunc.arghelp('list_geocoders', 'list available geocoders and exit')
    def geocode(s, api_key='', geocoder='google', list_geocoders=False):
        # ...

@notstrict means "don't throw an error if one of the required positional 
arguments is missing" - in the above example we use this because we still want
the list_geocoders argument to work even if a string has not been provided.

@arghelp('arg-name', 'help text') allows you to provide help on individual 
arguments, which will then be displayed when --help is called.

TODO:

* Support for different argument types (int, string, filehandle, choices)
* Special handling for 'stdin' as an argument name
* Proper unix error semantics (sys.exit(1) etc)
* Allow the function to be a generator, print iterations to stdout
* Support for *args (I don't think **kwargs makes sense for optfunc)