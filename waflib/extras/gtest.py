#! /usr/bin/env python
# encoding: utf-8
# author: Anton Feldmann


'''

When using this tool, the wscript will look like:

        def configure(conf):
                conf.load('compiler_cxx gtest')

        def build(bld):
                bld(source='main.cpp', target='app', use='GTEST')

Options are generated, in order to specify the location of tinyxml includes/libraries.


'''
import sys
import re
from waflib import Utils,Logs,Errors
from waflib.Configure import conf

GTEST_DIR=['/usr','/usr/local','/opt/local']
GTEST_CODE='''
#include <gtest/gtest.h>

TEST(MyTest, Test) {
   ASSERT_TRUE(true);
}

int main(int argc, char** argv) {
 ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
'''

def options(opt):
        opt.add_option('--gtest',
                       type='string',
                       default='',
                       dest='gtest_dir',
                       help='''path to GTest (/usr/local)''')
@conf
def __gtest_get_header_file(self,dir):
        try:
                return self.root.find_dir(dir).find_node('include/gtest/gtest.h')
        except:
                return None

@conf
def gtest_get_header(self,dir):
        val=self.check_cxx(fragment=GTEST_CODE,
                           includes=['%s/%s' % (dir, 'include')], 
                           execute=True, 
                           define_ret = True, 
                           mandatory=True)
        return val

@conf
def gtest_get_root(self,*k,**kw):
        root=k and k[0]or kw.get('path',None)

        if root and self.__gtest_get_root_file(root):
                return root
        for dir in GTEST_DIR:
                if self.__gtest_get_root_file(dir):
                        return dir

        if root:
                self.fatal('GTest not found in %s'%root)
        else:
                self.fatal('Gtest not found, use the --gtest argument')

@conf
def check_gtest(self,*k,**kw):
        if not self.env['CXX']:
                self.fatal('first load a c++ compiler')

        var=kw.get('uselib_store','GTESTLIB')
        self.start_msg('Checking GTtestLib')
        root = self.gtest_get_root(*k,**kw)
#        gtest_herader=self.gtest_get_header(root)

        self.env['INCLUDES_%s'%var]= '%s/%s' % (root, "include");

        if Logs.verbose:
                Logs.pprint('GREEN','        GTest include : %s'%self.env['INCLUDES_%s'%var])

