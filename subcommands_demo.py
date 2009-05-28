#!/usr/bin/env python
import optfunc

def one(arg):
    print "One: %s" % arg

def two(arg):
    print "Two: %s" % arg

def three(arg):
    print "Three: %s" % arg

if __name__ == '__main__':
    optfunc.run([one, two, three])
