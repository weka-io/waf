#! /usr/bin/env python
# encoding: utf-8
# author: Anton Feldmann

'''

When using this tool, the wscript will look like:

        def configure(conf):
                conf.load('compiler_cxx loki')

        def build(bld):
                bld(source='main.cpp', target='app', use='LOKI')

Options are generated, in order to specify the location of loki includes/libraries.


'''
import sys
import re
from waflib import Utils,Logs,Errors
from waflib.Configure import conf

LOKI_DIR=['/usr','/usr/local','/opt/local']

def options(opt):
        opt.add_option('--libloki',
                       type='string',
                       default='',
                       dest='loki_dir',
                       help='''path to libLoki (/usr/local)''')

def configure(conf):
    conf.check_cxx(lib = 'somelib', use = 'LOKI')
