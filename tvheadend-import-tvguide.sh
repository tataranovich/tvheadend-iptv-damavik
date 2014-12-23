#!/bin/sh
# -*- coding: utf-8 -*-
# Copyright (c) 2014  Andrey Tataranovich <tataranovich@gmail.com>
# License: GPL-3
# Website: https://github.com/tataranovich/tvheadend-iptv-damavik

TVGUIDE_URL='http://www.vipiko.tv/get?cur-xtv-tgz'
TVGUIDE_LOCAL="$HOME/vipiko.tv.tgz"

if [ -f "$TVGUIDE_LOCAL" ]; then
    MTIME_OLD=$(stat -c %Y "$TVGUIDE_LOCAL")
else
    MTIME_OLD=0
fi

wget -q -N "$TVGUIDE_URL" -O "$TVGUIDE_LOCAL"
MTIME_NEW=$(stat -c %Y "$TVGUIDE_LOCAL")
if [ "x$MTIME_OLD" != "x$MTIME_NEW" ]; then
    # File was changed on the server, we need to import it
    tar -xzOf "$TVGUIDE_LOCAL" | nc -U /home/hts/.hts/tvheadend/epggrab/xmltv.sock
fi