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
        opt.add_option('--loki',
                       type='string',
                       default='',
                       dest='loki_dir',
                       help='''path to loki (/usr/local)''')

@conf
def __loki_get_file(self,dir):
        try:
                return self.root.find_dir(dir).find_node('include/loki/LokiTypeInfo.h')
        except:
                return None

@conf
def loki_get_root(self,*k,**kw):
        root=k and k[0]or kw.get('path',None)

	for dir in LOKI_DIR:
                if self.__loki_get_file(dir):
                        return dir

	self.fatal('TinyXML not found in %s'%root)

@conf
def check_loki(self,*k,**kw):
        if not self.env['CXX']:
                self.fatal('first load a c++ compiler')

        var=kw.get('uselib_store','LOKI')
        self.start_msg('Checking loki')
        root = self.loki_get_root(*k,**kw);

        self.env['INCLUDES_%s'%var]= '%s/%s' % (root, "include");
        self.env['LIB_%s'%var] = "loki"
        self.env['LIBPATH_%s'%var] = '%s/%s' % (root, "lib")

        self.end_msg('checked Loki')
        if Logs.verbose:
                Logs.pprint('GREEN','    Loki include : %s'%self.env['INCLUDES_%s'%var])
                Logs.pprint('GREEN','    Loki lib     : %s'%self.env['LIB_%s'%var])
                Logs.pprint('GREEN','    Loki libpath : %s'%self.env['LIBPATH_%s'%var])
