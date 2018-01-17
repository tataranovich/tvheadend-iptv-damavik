#!/bin/sh
# -*- coding: utf-8 -*-
# Copyright (c) 2014  Andrey Tataranovich <tataranovich@gmail.com>
# License: GPL-3
# Website: https://github.com/tataranovich/tvheadend-iptv-damavik

RUN_PREFIX="$(dirname $0)"
TVGUIDE_URL='http://help.telecom.by/_files/TelecomTV/TelecomTVepg/xmltv.xml'
TVGUIDE_LOCAL="$HOME/xmltv.xml"

if [ -f "$TVGUIDE_LOCAL" ]; then
    MTIME_OLD=$(stat -c %Y "$TVGUIDE_LOCAL")
else
    MTIME_OLD=0
fi

if [ "$1" = "--force" ]; then
    MTIME_OLD=0
fi

wget -q -N "$TVGUIDE_URL" -O "$TVGUIDE_LOCAL"
MTIME_NEW=$(stat -c %Y "$TVGUIDE_LOCAL")
if [ "x$MTIME_OLD" != "x$MTIME_NEW" ]; then
    # File was changed on the server, we need to import it
    cat "$TVGUIDE_LOCAL" | socat - UNIX-CONNECT:/home/hts/.hts/tvheadend/epggrab/xmltv.sock
fi
