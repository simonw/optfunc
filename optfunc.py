from optparse import OptionParser, make_option
import sys, inspect

class ErrorCollectingOptionParser(OptionParser):
    def __init__(self, *args, **kwargs):
        self._errors = []
        # can't use super() because OptionParser is an old style class
        OptionParser.__init__(self, *args, **kwargs)
    
    def error(self, msg):
        self._errors.append(msg)

class Var(object):
    def __init__(
        self, short=None, long=None, default=None, help=None, required=False
        ):
        self.short = short
        self.long = long
        self.default = default
        self.help = help
        self.required = required
    
    def convert(self, data):
        return data
    
    def make_option(self, name):
        return make_option(self.short, self.long, action='store', dest=name)

class Str(Var):
    covert = str

class Bool(Var):
    def convert(self, data):
        return str(data).strip() not in ('0', '', 'false', 'False')

class Int(Var):
    convert = int

class Choice(Var):
    def __init__(self, **kwargs):
        self.choices = kwargs.pop('choices')
        super(Choice, self).__init__(self, **kwargs)
    
    def convert(self, data):
        if data not in self.choices:
            raise ValueError, 'Valid options: %s' % (', '.join(self.choices))
        return data

def func_to_optionparser(func):
    args, varargs, varkw, defaultvals = inspect.getargspec(func)
    defaultvals = defaultvals or ()
    options = dict(zip(args[-len(defaultvals):], defaultvals))
    if defaultvals:
        required_args = args[:-len(defaultvals)]
    else:
        required_args = args
    
    # Now build the OptionParser
    opt = ErrorCollectingOptionParser()
    for name, option in options.items() :
        opt.add_option(option.make_option(name))
    
    return opt, required_args

def resolve_args(func, argv):
    parser, required_args = func_to_optionparser(func)
    options, args = parser.parse_args(argv)
    
    # Do we have correct number af required args?
    if len(required_args) != len(args):
        raise TypeError, 'Requires %d arguments, got %d' % (
            len(required_args), len(args)
        )
    
    for i, name in enumerate(required_args):
        setattr(options, name, args[i])
    
    return options.__dict__, parser._errors

def run(func, argv=None):
    argv = argv or sys.argv[1:]
    resolved, errors = resolve_args(func, argv)
    if not errors:
        return func(**resolved)
    else:
        print "ERRORS: %s" % errors
