#!/usr/bin/env python

import urllib
import re
import webbrowser

# Idea is taken from the following article:
# http://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video

RE_STR = r'href=\"\/watch\?v=(.{11})'
SEARCH_FMT = 'http://www.youtube.com/results?search_query=%s'
VIDEO_FMT = 'http://www.youtube.com/watch?v=%s'

search = urllib.quote('inception movie trailer')
content = urllib.urlopen(SEARCH_FMT % search)
search_results = re.findall(RE_STR, content.read())
webbrowser.open(VIDEO_FMT % search_results[0])
