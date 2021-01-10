#!/usr/bin/env python3

import argparse
import consul
import sys
import yaml

from pprint import pprint

consul_keys = []
consul_values = {}

parser = argparse.ArgumentParser(description='Extract Consul keys')
parser.add_argument('--input', help='YAML file with keys to extract')
parser.add_argument('--output', help='File to output keys extrated')
parser.add_argument('--key', help='Key to put in Consul (value is needed)')
parser.add_argument('--value', help='Value to put in Consul (key is needed)')

args = parser.parse_args()

if args.input == None or args.output == None:
    parser.print_help()
    exit(1)

c = consul.Consul()


def get_keys_to_load(filename):
    stream = open(filename, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)

    if data:
        return data.get('kv', {})
    else:
        return {}


def get_consul_keys(consul_keys):
    print('Extract Consul keys:')
    consul_values = {}

    for k in consul_keys:
        print(k)
        current_raw_value = c.kv.get(k)
        if current_raw_value[1] is None:
            current_value = None
        else:
            current_value = current_raw_value[1]['Value'].decode()
        consul_values[k] = current_value

    return consul_values


def write_consul_keys_to_file(filename, data):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


if args.key != None or args.value != None:
    if args.key != None and args.value != None:
        print('Update with {}={}'.format(args.key, args.value))
        c.kv.put(args.key, args.value)
    else:
        parser.print_help()
        print('')
        print('Need to define --key and --value together')
        exit(1)


consul_keys = get_keys_to_load(args.input)
consul_values['kv'] = get_consul_keys(consul_keys)
# pprint(consul_values)
write_consul_keys_to_file(args.output, consul_values)
