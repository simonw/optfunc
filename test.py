import unittest
import optfunc
from StringIO import StringIO

class TestOptFunc(unittest.TestCase):
    def test_three_positional_args(self):
        
        has_run = [False]
        def func(one, two, three):
            has_run[0] = True
        
        # Should only have the -h help option
        parser, required_args = optfunc.func_to_optionparser(func)
        self.assertEqual(len(parser.option_list), 1)
        self.assertEqual(str(parser.option_list[0]), '-h/--help')
        
        # Should have three required args
        self.assertEqual(required_args, ['one', 'two', 'three'])
        
        # Running it with the wrong number of arguments should cause an error
        for argv in (
            ['one'],
            ['one', 'two'],
            ['one', 'two', 'three', 'four'],
        ):
            e = StringIO()
            optfunc.run(func, argv, stderr=e)
            self.assert_('Required 3 arguments' in e.getvalue(), e.getvalue())
            self.assertEqual(has_run[0], False)
        
        # Running it with the right number of arguments should be fine
        e = StringIO()
        optfunc.run(func, ['one', 'two', 'three'], stderr=e)
        self.assertEqual(e.getvalue(), '')
        self.assertEqual(has_run[0], True)
    
    def test_one_arg_one_option(self):
        
        has_run = [False]
        def func(one, option=''):
            has_run[0] = (one, option)
        
        # Should have -o option as well as -h option
        parser, required_args = optfunc.func_to_optionparser(func)
        self.assertEqual(len(parser.option_list), 2)
        strs = [str(o) for o in parser.option_list]
        self.assert_('-h/--help' in strs)
        self.assert_('-o/--option' in strs)
        
        # Should have one required arg
        self.assertEqual(required_args, ['one'])
        
        # Should execute
        self.assert_(not has_run[0])
        optfunc.run(func, ['the-required', '-o', 'the-option'])
        self.assert_(has_run[0])
        self.assertEqual(has_run[0], ('the-required', 'the-option'))
        
        # Option should be optional
        has_run[0] = False
        optfunc.run(func, ['required2'])
        self.assert_(has_run[0])
        self.assertEqual(has_run[0], ('required2', ''))
    
    def test_options_are_correctly_named(self):
        def func1(one, option='', verbose=False):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(func1)
        strs = [str(o) for o in parser.option_list]
        self.assertEqual(strs, ['-h/--help', '-o/--option', '-v/--verbose'])
    
    def test_option_with_hyphens(self):
        def func2(option_with_hyphens=True):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(func2)
        strs = [str(o) for o in parser.option_list]
        self.assertEqual(strs, ['-h/--help', '-o/--option-with-hyphens'])
    
    def test_options_with_same_inital_use_next_letter(self):
        def func1(one, version='', verbose=False):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(func1)
        strs = [str(o) for o in parser.option_list]
        self.assertEqual(strs, ['-h/--help', '-v/--version', '-e/--verbose'])

        def func2(one, host=''):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(func2)
        strs = [str(o) for o in parser.option_list]
        self.assertEqual(strs, ['-h/--help', '-o/--host'])
    
    def test_short_option_can_be_named_explicitly(self):
        def func1(one, option='', q_verbose=False):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(func1)
        strs = [str(o) for o in parser.option_list]
        self.assertEqual(strs, ['-h/--help', '-o/--option', '-q/--verbose'])

        e = StringIO()
        optfunc.run(func1, ['one', '-q'], stderr=e)
        self.assertEqual(e.getvalue().strip(), '')
    
    def test_notstrict(self):
        "@notstrict tells optfunc to tolerate missing required arguments"
        def strict_func(one):
            pass
        
        e = StringIO()
        optfunc.run(strict_func, [], stderr=e)
        self.assertEqual(e.getvalue().strip(), 'Required 1 arguments, got 0')
        
        @optfunc.notstrict
        def notstrict_func(one):
            pass
        
        e = StringIO()
        optfunc.run(notstrict_func, [], stderr=e)
        self.assertEqual(e.getvalue().strip(), '')
    
    def test_arghelp(self):
        "@arghelp('foo', 'help about foo') sets help text for parameters"
        @optfunc.arghelp('foo', 'help about foo')
        def foo(foo = False):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(foo)
        opt = parser.option_list[1]
        self.assertEqual(str(opt), '-f/--foo')
        self.assertEqual(opt.help, 'help about foo')
    
    def test_multiple_invalid_subcommand(self):
        "With multiple subcommands, invalid first arg should raise an error"
        def one(arg):
            pass
        def two(arg):
            pass
        def three(arg):
            pass
        
        # Invalid first argument should raise an error
        e = StringIO()
        optfunc.run([one, two], ['three'], stderr=e)
        self.assertEqual(
            e.getvalue().strip(), "Unknown command: try 'one' or 'two'"
        )
        e = StringIO()
        optfunc.run([one, two, three], ['four'], stderr=e)
        self.assertEqual(
            e.getvalue().strip(),
            "Unknown command: try 'one', 'two' or 'three'"
        )
        
        # No argument at all should raise an error
        e = StringIO()
        optfunc.run([one, two, three], [], stderr=e)
        self.assertEqual(
            e.getvalue().strip(),
            "Unknown command: try 'one', 'two' or 'three'"
        )
    
    def test_multiple_valid_subcommand_invalid_argument(self):
        "Subcommands with invalid arguments should report as such"
        def one(arg):
            executed.append(('one', arg))
        
        def two(arg):
            executed.append(('two', arg))

        e = StringIO()
        executed = []
        optfunc.run([one, two], ['one'], stderr=e)
        self.assertEqual(
            e.getvalue().strip(), 'one: Required 1 arguments, got 0'
        )
    
    def test_multiple_valid_subcommand_valid_argument(self):
        "Subcommands with valid arguments should execute as expected"
        def one(arg):
            executed.append(('one', arg))
        
        def two(arg):
            executed.append(('two', arg))

        e = StringIO()
        executed = []
        optfunc.run([one, two], ['two', 'arg!'], stderr=e)
        self.assertEqual(e.getvalue().strip(), '')
        self.assertEqual(executed, [('two', 'arg!')])

    def test_run_class(self):
        class Class:
            def __init__(self, one, option=''):
                self.has_run = [(one, option)]
        
        class NoInitClass:
            pass

        # Should execute
        e = StringIO()
        c = optfunc.run(Class, ['the-required', '-o', 'the-option'], stderr=e)
        self.assertEqual(e.getvalue().strip(), '')
        self.assert_(c.has_run[0])
        self.assertEqual(c.has_run[0], ('the-required', 'the-option'))
        
        # Option should be optional
        c = None
        e = StringIO()
        c = optfunc.run(Class, ['required2'], stderr=e)
        self.assertEqual(e.getvalue().strip(), '')
        self.assert_(c.has_run[0])
        self.assertEqual(c.has_run[0], ('required2', ''))

        # Classes without init should work too
        c = None
        e = StringIO()
        c = optfunc.run(NoInitClass, [], stderr=e)
        self.assert_(c)
        self.assertEqual(e.getvalue().strip(), '')
    
    def test_stdin_special_argument(self):
        consumed = []
        def func(stdin):
            consumed.append(stdin.read())
        
        class FakeStdin(object):
            def read(self):
                return "hello"
        
        optfunc.run(func, stdin=FakeStdin())
        self.assertEqual(consumed, ['hello'])
    
if __name__ == '__main__':
    unittest.main()
