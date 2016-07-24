#!/usr/bin/env python

import urllib, time

response = urllib.urlopen("http://www.omdbapi.com/?t=Braveheart&plot=full&r=json").read()
print response
print
time.sleep(1)

movie = 'silence of the lambs'
response = urllib.urlopen("http://www.omdbapi.com/?t=%s&plot=full&r=json" % urllib.quote(movie)).read()
print 'searching for %s' % movie
print response
print
time.sleep(1)

movie = 'el lado oscuro del corazon'
response = urllib.urlopen("http://www.omdbapi.com/?t=%s&plot=full&r=json" % urllib.quote(movie)).read()
print 'searching for %s' % movie
print response
print
time.sleep(1)

movie = 'jason bourne'
response = urllib.urlopen("http://www.omdbapi.com/?t=%s&plot=full&r=json" % urllib.quote(movie)).read()
print 'searching for %s' % movie
print response
print
time.sleep(1)

movie = 'whichilocotli'
response = urllib.urlopen("http://www.omdbapi.com/?t=%s&plot=full&r=json" % urllib.quote(movie)).read()
print 'searching for %s' % movie
print response
print
time.sleep(1)

movie = 'die hard'
response = urllib.urlopen("http://www.omdbapi.com/?t=%s&plot=full&r=json" % urllib.quote(movie)).read()
print 'searching for %s' % movie
print response
print
time.sleep(1)

movie = 'die hard with a vengence'
response = urllib.urlopen("http://www.omdbapi.com/?t=%s&plot=full&r=json" % urllib.quote(movie)).read()
print 'searching for %s' % movie
print response
print
time.sleep(1)

movie = 'inception'
response = urllib.urlopen("http://www.omdbapi.com/?t=%s&plot=full&r=json" % urllib.quote(movie)).read()
print 'searching for %s' % movie
print response
print
