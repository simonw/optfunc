#!/usr/bin/env python
# Depends on geocoders from http://github.com/simonw/geocoders being on the 
# python path.
import geocoders
import optfunc
import os

# We use notstrict because we want to be able to trigger the list_geocoders
# option without being forced to provide the normally mandatory 's' argument
@optfunc.notstrict
@optfunc.arghelp('list_geocoders', 'list available geocoders and exit')
def geocode(s, api_key='', geocoder='google', list_geocoders=False):
    "Usage: %prog <location string> --api-key <api-key>" 
    available = [
        f.replace('.py', '')
        for f in os.listdir(os.path.dirname(geocoders.__file__))
        if f.endswith('.py') and not f.startswith('_') and f != 'utils.py'
    ]
    if list_geocoders:
        print 'Available geocoders: %s' % (', '.join(available))
        return
    
    assert geocoder in available, '"%s" is not a known geocoder' % geocoder
    assert s, 'Enter a string to geocode'
    
    mod = __import__('geocoders.%s' % geocoder, {}, {}, ['geocoders'])
    
    name, (lat, lon) =  mod.geocoder(api_key)(s)
    print '%s\t%s\t%s' % (name, lat, lon)

optfunc.main(geocode)
