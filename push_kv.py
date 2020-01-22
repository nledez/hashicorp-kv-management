#!/usr/bin/env python3

import argparse
import consul
import hvac
import sys
import yaml

VAULT_KV_MOUNT = 'kv'

update = False
consul_to_create_or_update = {}
vault_to_create_or_update = {}

parser = argparse.ArgumentParser(description='Import Consul & Vault keys from YAML file')
parser.add_argument('--filename', action='append', help='YAML file to load')
parser.add_argument('--update', dest='update', action='store_true', help='Update key needed')

args = parser.parse_args()

c = consul.Consul()
h = hvac.Client()

def load_yaml(filename):
    stream = open(filename, 'r')
    data = yaml.load(stream, Loader=yaml.BaseLoader)

    consul_to_create_or_update = {}
    vault_to_create_or_update = {}

    print('Check Consul keys:')
    for k, v in data.get(VAULT_KV_MOUNT, {}).items():
        current_raw_value = c.kv.get(k)
        if current_raw_value[1] is None:
            current_value = None
        else:
            current_value = current_raw_value[1]['Value'].decode()

        if current_value is None:
            print('{} => is missing'.format(k))
            consul_to_create_or_update[k] = v
        elif current_value != v:
            print('{}: {} != {}'.format(k, current_value, v))
            consul_to_create_or_update[k] = v

    print('Check Vault keys:')
    for k, v in data.get('vault', {}).items():
        try:
            current_raw_value = h.secrets.kv.v1.read_secret(
                mount_point=VAULT_KV_MOUNT,
                path=k,
            )
            current_value = current_raw_value['data']
        except(hvac.exceptions.InvalidPath):
            current_value = None

        if current_value is None:
            print('{} => is missing'.format(k))
            vault_to_create_or_update[k] = v
        elif current_value != v:
            print('{}: {} != {}'.format(k, current_value, v))
            vault_to_create_or_update[k] = v

    return (consul_to_create_or_update, vault_to_create_or_update)

for filename in args.filename:
    (new_consul, new_vault) = load_yaml(filename)
    consul_to_create_or_update = {**consul_to_create_or_update, **new_consul}
    vault_to_create_or_update = {**vault_to_create_or_update, **new_vault}

if len(consul_to_create_or_update) == 0 and vault_to_create_or_update == 0:
    print('Everything is OK. Exit now')
    sys.exit(0)

if args.update:
    print('\nDo update:')
    for k, v in consul_to_create_or_update.items():
        print('{}: {}'.format(k, v))
        c.kv.put(k, v)
    for k, v in vault_to_create_or_update.items():
        print('{}: {}'.format(k, v))
        h.secrets.kv.v1.create_or_update_secret(
            mount_point=VAULT_KV_MOUNT,
            path=k,
            secret=v,
        )
else:
    print('\nRun in dry mode, add "--update" parameter if you want update keys')
