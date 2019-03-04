import os
import sys


config = dict()

if ('--dev' in sys.argv):
    with open('.env', 'r') as envfile:
        envs = envfile.read()
        for env in envs.split('\n'):
            keypair = env.split('=')
            config[keypair[0]] = keypair[1]
    if ('secret' not in config):
        raise 'Channel secret not found in .env'
    if ('access_token' not in config):
        raise 'Channel access token not found in .env'
else:
    config['secret'] = os.environ['secret']
    config['access_token'] = os.environ['access_token']
