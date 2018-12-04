#!/bin/sh
# -*- coding: utf-8 -*-
# Copyright (c) 2014  Andrey Tataranovich <tataranovich@gmail.com>
# License: GPL-3
# Website: https://github.com/tataranovich/tvheadend-iptv-damavik

RUN_PREFIX="$(dirname $0)"
M3U_URL="http://help.telecom.by/_files/TelecomTV/TelecomTVpacket/TVPACKET3.m3u"
M3U_LOCAL="$HOME/TVPACKET3.m3u"

if [ -f "$M3U_LOCAL" ]; then
    MTIME_OLD=$(stat -c %Y "$M3U_LOCAL")
    cp -a "$M3U_LOCAL" "${M3U_LOCAL}.tmp"
else
    MTIME_OLD=0
    touch "${M3U_LOCAL}.tmp"
fi

wget -q -N "$M3U_URL" -O "${M3U_LOCAL}.tmp"

M3U_SIZE=$(stat -c %s "${M3U_LOCAL}.tmp")
if [ $M3U_SIZE -le 256 ]; then
    echo "Error: M3U file size is too small (${M3U_SIZE} bytes)" >&2
    rm "${M3U_LOCAL}.tmp"
    exit 1
else
    mv "${M3U_LOCAL}.tmp" "${M3U_LOCAL}"
fi

MTIME_NEW=$(stat -c %Y "$M3U_LOCAL")

if [ "x$MTIME_OLD" != "x$MTIME_NEW" ]; then
    # File was changed on the server, we need to import it
    echo "Playlist changed, importing..."
    sudo /etc/init.d/tvheadend stop
    # Cleanup old channel/epg configuration
    rm -fr ~/.hts/tvheadend/channels/ ~/.hts/tvheadend/iptvservices/
    rm -fr ~/.hts/tvheadend/epggrab/xmltv/channels/ ~/.hts/tvheadend/epgdb.v2 ~/.hts/tvheadend/imagecache/meta/
    "$RUN_PREFIX/tvheadend.py" "$M3U_LOCAL" "$RUN_PREFIX/tvguide.json" ~/.hts/tvheadend/
    sudo /etc/init.d/tvheadend start
    echo "Forcing EPG import..."
    "$RUN_PREFIX/tvheadend-import-tvguide.sh" --force
    for i in htpc-pi htpc-wetek htpc-brix
    do
        ssh -T root@${i}.home.tataranovich.com >/dev/null || echo "Failed to restart PVR on ${i}.home.tataranovich.com"
    done
fi
