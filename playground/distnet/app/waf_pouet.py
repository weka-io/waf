# module exported and used for configuring the package pouet

import os

def options(opt):
	# project-specific options go here
	pass

def configure(conf):
	conf.env.append_value('DEFINES_pouet', 'pouet=1')
	conf.env.append_value('INCLUDES_pouet', os.path.dirname(os.path.abspath(__file__)))

def build(bld):
	# project-specific build targets go here
	pass

