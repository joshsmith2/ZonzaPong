#coding=utf-8
'''
Created on 4 nov. 2012

@author: Sora
'''
import os


DEBUG = True

SOCKET_IO_PORT = 8080

SOCKET_IO_REMOTE_ADDR = "0.0.0.0"

TORNADIO_LOGGING_LEVEL = "debug" if DEBUG else "info"

DOCUMENT_ROOT = os.path.dirname(os.path.abspath(__file__))

RESOURCES_ROOT = DOCUMENT_ROOT + "/resources"

