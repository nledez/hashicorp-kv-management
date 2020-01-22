#!/usr/bin/env python3

import argparse
import consul
import sys
import yaml

update = False
need_to_create_or_update = {}

parser = argparse.ArgumentParser(description='Import Consul & Vault keys from YAML file')
parser.add_argument('--filename', action='append', help='YAML file to load')
parser.add_argument('--update', dest='update', action='store_true', help='Update key needed')

args = parser.parse_args()

c = consul.Consul()

def load_yaml(filename):
    stream = open(filename, 'r')
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

    return need_to_create_or_update

print('Check keys:')
for filename in args.filename:
    new_dict = load_yaml(filename)
    need_to_create_or_update = {**need_to_create_or_update, **new_dict}

if len(need_to_create_or_update) == 0:
    print('Everything is OK. Exit now')
    sys.exit(0)

if args.update:
    print('\nDo update:')
    for k, v in need_to_create_or_update.items():
        print('{}: {}'.format(k, v))
        c.kv.put(k, v)
else:
    print('\nRun in dry mode, add "--update" parameter if you want update keys')
