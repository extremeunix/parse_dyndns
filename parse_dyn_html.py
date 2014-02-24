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
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
