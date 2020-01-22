#!/usr/bin/env python3

import consul
import yaml

from pprint import pprint

c = consul.Consul()

stream = open('dev.yaml', 'r')
data = yaml.load(stream, Loader=yaml.BaseLoader)

need_to_create_or_update = {}

for k, v in data['kv'].items():
    current_raw_value = c.kv.get(k)
    if current_raw_value[1] is None:
        current_value = None
    else:
        current_value = current_raw_value[1]['Value'].decode()

    if current_value is None:
        print('{} => is missing'.format(k))
        need_to_create_or_update[k] = v
    elif current_value != v:
        print('{}: {} != {}'.format(k, current_value, v))
        need_to_create_or_update[k] = v
