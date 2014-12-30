# -*- coding: utf-8 -*-
# Copyright (c) 2014  Andrey Tataranovich <tataranovich@gmail.com>
# License: GPL-3
# Website: https://github.com/tataranovich/tvheadend-iptv-damavik

import json


class ChannelNameTransform:
    def __init__(self, config_file):
        handle = open(config_file, 'r')
        self.transform = json.load(handle)
        handle.close()

    def replace(self, channel_name):
        if channel_name in self.transform:
            return self.transform[channel_name]