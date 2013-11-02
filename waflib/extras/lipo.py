#! /usr/bin/env python
# encoding: utf-8
# Anton Feldmann 2013 (New BSD License)

import os,sys

from waflib import TaskGen, Task, Utils
from waflib.Configure import conf
from waflib.Task import always_run
from waflib.TaskGen import extension, feature, after, before, before_method
from waflib.Utils import threading

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
 
def _lipo_lib(ctx, lib_name):
    ctx(rule='lipo -create ${SRC} -output ${TGT}',
        shell = True,
        target = 'lib%s-%s.a' % (lib_name, ctx.target),
        source = ['build/ios_%s_%s/lib%s.a' % (x, ctx.target, lib_name) for x in ARCHS]
    )

def _lipo_thin_lib(ctx, lib_name):
    ctx(rule='lipo -thin ${ARCH} ${SRC} -output ${TGT}',
        shell = True,
        target = 'lib%s-%s.a' % (lib_name, ctx.target),
        source = ['build/ios_%s_%s/lib%s.a' % (x, ctx.target, lib_name) for x in ARCHS]
    )

def _lipo_remove_lib(ctx, lib_name):
    ctx(rule='lipo -remove ${ARCH} ${SRC} -output ${TGT}',
        shell = True,
        target = 'lib%s-%s.a' % (lib_name, ctx.target),
        source = ['build/ios_%s_%s/lib%s.a' % (x, ctx.target, lib_name) for x in ARCHS]
    )
