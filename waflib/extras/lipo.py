#! /usr/bin/env python
# encoding: utf-8
# Anton Feldmann 2013 (New BSD License)

import os,sys

from waflib import TaskGen, Task, Utils
from waflib.Configure import conf
from waflib.Task import always_run
from waflib.TaskGen import extension, feature, after, before, before_method
from waflib.Utils import threading

LIPO_COMMAND='lipo -create ${SRC} -output ${TGT}'

def options(ctx):
        ctx.add_option('-lo',
		       '--lipo-options', 
		       dest='lipo_option',
		       action='store', 
		       default='', 
		       help='space separated list of flags to pass to lipo')

def configure(conf):
    conf.find_program('lipo', var='LIPO')
    if conf.options.lipo_option:
        conf.env.LIPOOPT = conf.options.lipo_option
 
