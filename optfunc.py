from optparse import OptionParser

class Var(object):
    def __init__(self, short=None, long=None, default=None, help=None):
        self.short = short
        self.long = long
        self.default = default
        self.help = help
    
    def convert(self, data):
        return data

class String(Var):
    def convert(self, data):
        return str(data)

class Bool(Var):
    def convert(self, data):
        return data.strip() not in ('0', '', 'false', 'False')

def run(func):
    # TODO: introspect function, build up command line args, execute it
    pass
