#!/usr/bin/env python
# Copyright 2012 Cyrus Dasadia [cyrus -a-t- extremeunix.com]
#
# How it works:
# 1. Login to DynDNS, open the zone
# 2. Save the page on local machine
# 3. python parse_dyndns_html.py -f <your_zone.html> 
# 4. Enjoy!
# 
# Known issues:
# This script does not detect web-redirects (webhops). 
#
## The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from bs4 import BeautifulSoup
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',help="DynDNS HTML page of the zone",dest="zonefile",required=True)
    
    options = parser.parse_args()
    zonefile = options.zonefile
    try:
        soup = BeautifulSoup(open(zonefile))
    except:
        print "Cannot open: %s" % zonefile
        sys.exit(1)

    #All your RRs are belong to us!    
    t = soup.find('fieldset')

    #Each record is within a table row
    for tr in t.findAll('tr'):
        rr = ''  
        #Get each column of a resource record
        for td in tr.findAll('td'):
            if td.findAll('input'):
                for input in td.findAll('input'):
                    # We will skip the checkbox which allows you to delete record
                    if input.has_key('type') and input['type'] == 'checkbox':
                        pass
                    else:
                         rr += ","+ input['value'].strip()
            else:
                rr += "," + td.string.strip()
        #Get rid of first comma and print the resource record
        print "%s" % rr[1:].encode('ascii', 'ignore')


if __name__ == '__main__':
    main()
