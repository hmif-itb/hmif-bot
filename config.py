import os
import sys


config = dict()
config_keys = ['secret', 'access_token', 'private_group', 'pass_code']

if ('--dev' in sys.argv):
    with open('.env', 'r') as envfile:
        envs = envfile.read()
        for env in envs.split('\n'):
            keypair = env.split('=')
            config[keypair[0]] = keypair[1]
    for key in config_keys:
        if (key not in config):
            raise Exception('{} not found in .env'.format(key))
else:
    for key in config_keys:
        config[key] = os.environ[key]
