#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os, os.path
import json
import parser
import re

def configureTvheadend(playlist, outdir):
    id = 0
    for entry in playlist:
        id = id + 1
        title = entry.title
        if 'tvg-name=' in entry.length:
            title = re.search(r'tvg-name="([^"]+)"', entry.length).group(1)
        channel = open(outdir + '/channels/' + str(id), 'w')
        channel.write(json.dumps({'name': title, 'channel_number': id}, ensure_ascii = False, indent = 4, separators = (',', ': ')))
        channel.close()
        service = open(outdir + '/iptvservices/iptv_' + str(id), 'w')
        group, port = entry.path.split('udp://@')[1].split(':', 1)
        service.write(json.dumps({'pmt':0, 'stype': 1, 'pcr': 0, 'port': port, 'group': group, 'interface': 'eth2', 'channelname': title, 'mapped': 1, 'disabled': 0}, ensure_ascii = False, indent = 4, separators = (',', ': ')))
        service.close()

def showUsage():
    print 'tvheadend.py <M3Ufile> <OutputDir>'

def main():
    m3ufile = sys.argv[1]
    outdir = sys.argv[2]

    if len(sys.argv) < 3:
        showUsage()
        sys.exit(1)
        
    if not os.path.isdir(outdir):
        print 'Specified output directory not exists: %s' % outdir
        sys.exit(1)
    else:
        os.mkdir(outdir + '/channels')
        os.mkdir(outdir + '/iptvservices')

    configureTvheadend(parser.parseM3U(m3ufile), outdir)

if __name__ == '__main__':
    main()
