#!/bin/sh
# -*- coding: utf-8 -*-
# Copyright (c) 2014  Andrey Tataranovich <tataranovich@gmail.com>
# License: GPL-3
# Website: https://github.com/tataranovich/tvheadend-iptv-damavik

RUN_PREFIX="$(dirname $0)"
M3U_URL="http://help.telecom.by/_files/TelecomTV/TelecomTVpacket/TVPACKET2.m3u"
M3U_LOCAL="$HOME/TVPACKET2.m3u"

if [ -f "$M3U_LOCAL" ]; then
    MTIME_OLD=$(stat -c %Y "$M3U_LOCAL")
else
    MTIME_OLD=0
fi

wget -q -N "$M3U_URL" -O "$M3U_LOCAL"
MTIME_NEW=$(stat -c %Y "$M3U_LOCAL")
if [ "x$MTIME_OLD" != "x$MTIME_NEW" ]; then
    # File was changed on the server, we need to import it
    echo "Playlist changed, importing..."
    sudo /etc/init.d/tvheadend stop
    rm -fr ~/.hts/tvheadend/channels/ ~/.hts/tvheadend/iptvservices/
    "$RUN_PREFIX/tvheadend.py" "$M3U_LOCAL" "$RUN_PREFIX/tvguide.json" ~/.hts/tvheadend/
    sudo /etc/init.d/tvheadend start
fi
