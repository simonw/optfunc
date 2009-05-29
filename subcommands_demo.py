#!/usr/bin/env python
import optfunc

def one(arg):
    print "One: %s" % arg

def two(arg):
    print "Two: %s" % arg

def three(arg):
    print "Three: %s" % arg

optfunc.main([one, two, three])
