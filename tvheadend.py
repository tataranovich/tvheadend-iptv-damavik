#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014  Andrey Tataranovich <tataranovich@gmail.com>
# License: GPL-3
# Website: https://github.com/tataranovich/tvheadend-iptv-damavik

import sys
import os
import os.path
import json
import parser
import re
import tvguide

reload(sys)
sys.setdefaultencoding('utf8')

def write_json(filename, obj):
    json_file = open(filename, 'w')
    json_file.write(json.dumps(obj, ensure_ascii=False, indent=4))
    json_file.close()


def configure_tvheadend(playlist, xmltv_match_file, outdir):
    i = 0
    xmltv_channel_names = tvguide.ChannelNameTransform(xmltv_match_file)
    for entry in playlist:
        i += 1
        title = entry.title
        if 'tvg-name=' in entry.length:
            title = re.search(r'tvg-name="([^"]+)"', entry.length).group(1)
        if not xmltv_channel_names.replace(unicode(title)) is None:
            title = xmltv_channel_names.replace(unicode(title))
        channel = {'name': title, 'channel_number': i}
        write_json(os.path.join(outdir, 'channels', str(i)), channel)
        group, port = entry.path.split('udp://@')[1].split(':', 1)
        iptv_service = {'pmt': 0, 'pcr': 0, 'stype': 1, 'port': port, 'group': group, 'interface': 'eth2',
                        'channelname': title, 'mapped': 1, 'disabled': 0}
        write_json(os.path.join(outdir, 'iptvservices', 'iptv_' + str(i)), iptv_service)


def show_usage():
    print 'Usage: tvheadend.py <M3Ufile> <xmltv-match.json> <OutputDir>'


def main():
    if len(sys.argv) < 4:
        show_usage()
        sys.exit(1)

    m3ufile = sys.argv[1]
    xmltv_match = sys.argv[2]
    outdir = sys.argv[3]

    if not os.path.isfile(m3ufile):
        print >> sys.stderr, '[Error] Specified M3U file not found: %s' % m3ufile
        sys.exit(1)
    if not os.path.isfile(xmltv_match):
        print >> sys.stderr, '[Error] Specified XMLTV match file not found: %s' % xmltv_match
        sys.exit(1)
    if not os.path.isdir(outdir):
        print >> sys.stderr, '[Error] Specified output directory not found: %s' % outdir
        sys.exit(1)
    else:
        try:
            os.mkdir(os.path.join(outdir, 'channels'))
            os.mkdir(os.path.join(outdir, 'iptvservices'))
        except OSError:
            print >> sys.stderr, 'Unable to create tvheadend directory structure'
            sys.exit(1)

    configure_tvheadend(parser.parse_m3u_file(m3ufile), xmltv_match, outdir)

if __name__ == '__main__':
    main()
