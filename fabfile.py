'''
Created on 2 juin 2012

@author: Sora
'''
from fabric.api import local, run, sudo, env
from fabric.contrib import django
import os
import sys


# needed to push youfood.settings onto the path.
sys.path.append(os.path.abspath('.'))

# default env configuration
env.python = 'python'
env.project_name = 'pyMapperServer'
env.deploy_user = 'apache'
env.deploy_group = 'commons'
# default to current working directory
env.project_path = os.path.dirname(__file__)
env.hosts = ['localhost']
env.apache = 'httpd'
# django integration for access to settings, etc.
django.project(env.project_name)


def tornadio(ip="127.0.0.1", port=None, logging=None):
    from pongserver import settings as pong_settings
    if port is None:
        port = pong_settings.SOCKET_IO_PORT
    if logging is None:
        logging = pong_settings.TORNADIO_LOGGING_LEVEL or 'ERROR'
    local("{python} tornadio.py {port} --logging={log_level}".format(python=env.python, port=port, log_level=logging))
