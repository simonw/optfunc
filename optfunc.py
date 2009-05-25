from optparse import OptionParser

class Switch(object):
    def __init__(self, shorthand, longhand, default=None):
        self.shorthand = shorthand
        self.longhand = longhand
        self.default = default

def run(func):
    # TODO: introspect function, build up command line args, execute it
    pass
