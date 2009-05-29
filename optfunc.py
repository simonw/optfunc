from optparse import OptionParser, make_option
import sys, inspect, re

single_char_prefix_re = re.compile('^[a-zA-Z0-9]_')

class ErrorCollectingOptionParser(OptionParser):
    def __init__(self, *args, **kwargs):
        self._errors = []
        self._custom_names = {}
        # can't use super() because OptionParser is an old style class
        OptionParser.__init__(self, *args, **kwargs)
    
    def parse_args(self, argv):
        options, args = OptionParser.parse_args(self, argv)
        for k,v in options.__dict__.iteritems():
            if k in self._custom_names:
                options.__dict__[self._custom_names[k]] = v
                del options.__dict__[k]
        return options, args

    def error(self, msg):
        self._errors.append(msg)

def func_to_optionparser(func):
    args, varargs, varkw, defaultvals = inspect.getargspec(func)
    defaultvals = defaultvals or ()
    options = dict(zip(args[-len(defaultvals):], defaultvals))
    argstart = 0
    if func.__name__ == '__init__':
        argstart = 1
    if defaultvals:
        required_args = args[argstart:-len(defaultvals)]
    else:
        required_args = args[argstart:]
    
    # Build the OptionParser:
    opt = ErrorCollectingOptionParser(usage = func.__doc__)
    
    helpdict = getattr(func, 'optfunc_arghelp', {})
    
    # Add the options, automatically detecting their -short and --long names
    shortnames = set(['h'])
    for funcname, example in options.items():
        # They either explicitly set the short with x_blah...
        name = funcname
        if single_char_prefix_re.match(name):
            short = name[0]
            name = name[2:]
            opt._custom_names[name] = funcname
        # Or we pick the first letter from the name not already in use:
        else:
            for short in name:
                if short not in shortnames:
                    break
        
        shortnames.add(short)
        short_name = '-%s' % short
        long_name = '--%s' % name.replace('_', '-')
        if example in (True, False, bool):
            action = 'store_true'
        else:
            action = 'store'
        opt.add_option(make_option(
            short_name, long_name, action=action, dest=name, default=example,
            help = helpdict.get(funcname, '')
        ))
    
    return opt, required_args

def resolve_args(func, argv):
    parser, required_args = func_to_optionparser(func)
    options, args = parser.parse_args(argv)
    
    # Special case for stdin/stdout/stderr
    for pipe in ('stdin', 'stdout', 'stderr'):
        if pipe in required_args:
            required_args.remove(pipe)
            setattr(options, 'optfunc_use_%s' % pipe, True)
    
    # Do we have correct number af required args?
    if len(required_args) != len(args):
        if not hasattr(func, 'optfunc_notstrict'):
            parser._errors.append('Required %d arguments, got %d' % (
                len(required_args), len(args)
            ))
    
    # Ensure there are enough arguments even if some are missing
    args += [None] * (len(required_args) - len(args))
    for i, name in enumerate(required_args):
        setattr(options, name, args[i])
    
    return options.__dict__, parser._errors

def run(
        func, argv=None, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
    ):
    argv = argv or sys.argv[1:]
    include_func_name_in_errors = False
    
    # Handle multiple functions
    if isinstance(func, (tuple, list)):
        funcs = dict([
            (fn.__name__, fn) for fn in func
        ])
        try:
            func_name = argv.pop(0)
        except IndexError:
            func_name = None
        if func_name not in funcs:
            names = ["'%s'" % fn.__name__ for fn in func]
            s = ', '.join(names[:-1])
            if len(names) > 1:
                s += ' or %s' % names[-1]
            stderr.write("Unknown command: try %s\n" % s)
            return
        func = funcs[func_name]
        include_func_name_in_errors = True

    if inspect.isfunction(func):
        resolved, errors = resolve_args(func, argv)
    elif inspect.isclass(func):
        if hasattr(func, '__init__'):
            resolved, errors = resolve_args(func.__init__, argv)
        else:
            resolved, errors = {}, []
    else:
        raise TypeError('arg is not a Python function or class')
    
    # Special case for stdin/stdout/stderr
    for pipe in ('stdin', 'stdout', 'stderr'):
        if resolved.pop('optfunc_use_%s' % pipe, False):
            resolved[pipe] = locals()[pipe]
    
    if not errors:
        try:
            return func(**resolved)
        except Exception, e:
            if include_func_name_in_errors:
                stderr.write('%s: ' % func.__name__)
            stderr.write(str(e) + '\n')
    else:
        if include_func_name_in_errors:
            stderr.write('%s: ' % func.__name__)
        stderr.write("%s\n" % '\n'.join(errors))

def main(*args, **kwargs):
    prev_frame = inspect.stack()[-1][0]
    mod = inspect.getmodule(prev_frame)
    if mod is not None and mod.__name__ == '__main__':
        run(*args, **kwargs)
    return args[0] # So it won't break anything if used as a decorator

# Decorators
def notstrict(fn):
    fn.optfunc_notstrict = True
    return fn

def arghelp(name, help):
    def inner(fn):
        d = getattr(fn, 'optfunc_arghelp', {})
        d[name] = help
        setattr(fn, 'optfunc_arghelp', d)
        return fn
    return inner
