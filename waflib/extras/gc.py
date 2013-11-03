#! /usr/bin/env python
# encoding: utf-8
# author: Anton Feldmann


'''

When using this tool, the wscript will look like:

        def configure(conf):
                conf.load('compiler_cxx boehmgc')

        def build(bld):
                bld(source='main.cpp', target='app', use='BOEHMGC')

Options are generated, in order to specify the location of tinyxml includes/libraries.


'''
import sys
import re
from waflib import Utils,Logs,Errors
from waflib.Configure import conf

GC_DIR=['/usr','/usr/local','/opt/local']
GC_VERSION_CODE='''
#include <iostream>
#include <gc.h>
int main() { std::cout << GC_VERSION_MAJOR << \
                          GC_VERSION_MINOR << \
                          GC_ALPHA_VERSION << std::endl;
'''

def options(opt):
        opt.add_option('--boehm gc',
                       type='string',
                       default='',
                       dest='gc_dir',
                       help='''path to Boehm GC (/usr/local)''')


@conf
def __gc_get_version_file(self,dir):
        try:
                return self.root.find_dir(dir).find_node('include/gc.h')
        except:
                return None
@conf
def gc_get_version(self,dir):
        val=self.check_cxx(fragment=GC_VERSION_CODE,
                           includes=['%s/%s' % (dir, 'include')], 
                           execute=True, 
                           define_ret = True, 
                           mandatory=True)
        return val

@conf
def gc_get_root(self,*k,**kw):
        root=k and k[0]or kw.get('path',None)

        if root and self.__gc_get_version_file(root):
                return root
        for dir in GC_DIR:
                if self.__gc_get_version_file(dir):
                        return dir

        if root:
                self.fatal('Boehm GC not found in %s'%root)
        else:
                self.fatal('Boehm GC not found, use the --tinyxml argument')

@conf
def check_tinyxml(self,*k,**kw):
        if not self.env.CXX:
                self.fatal('first load a c++ compiler')

        var=kw.get('uselib_store','BOEHMGC')
        self.start_msg('Checking Boehm GC')
        root = self.tinyxml_get_root(*k,**kw);
        self.env.GC_VERSION=self.gc_get_version(root)

        self.env['INCLUDES_%s'%var]= '%s/%s' % (root, "include");
        self.env['LIB_%s'%var] = "gc"
        self.env['LIBPATH_%s'%var] = '%s/%s' % (root, "lib")

        self.end_msg(self.env.GC)
        if Logs.verbose:
                Logs.pprint('GREEN','    BoehnGC include : %s'%self.env['INCLUDES_%s'%var])
                Logs.pprint('GREEN','    BoehmGC lib     : %s'%self.env['LIB_%s'%var])
                Logs.pprint('GREEN','    BoehmGC libpath : %s'%self.env['LIBPATH_%s'%var])

