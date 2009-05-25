from optparse import OptionParser

class Var(object):
    def __init__(self, shorthand, longhand, default=None):
        self.shorthand = shorthand
        self.longhand = longhand
        self.default = default
    
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
