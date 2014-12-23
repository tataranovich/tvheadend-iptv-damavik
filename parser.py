#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Track():
    def __init__(self, length, title, path):
        self.length = length
        self.title = title
        self.path = path 


def parse_m3u_file(infile):
    m3u = open(infile, 'r')
    # TODO: Hardcoded utf-8-sig decoder can misbehave with other M3U files
    line = m3u.readline().decode('utf-8-sig')
    if not line.startswith('#EXTM3U'):
        return None

    playlist = []
    entry = Track(None, None, None)

    for line in m3u:
        line = line.strip()
        if line.startswith('#EXTINF:'):
            length, title = line.split('#EXTINF:')[1].split(',', 1)
            entry = Track(length.strip(), title.strip(), None)
        elif len(line) != 0:
            entry.path = line.strip()
            playlist.append(entry)
            entry = Track(None, None, None)
    m3u.close()

    return playlist
