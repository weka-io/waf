#!/usr/bin/env python
# encoding: utf-8
# Christoph Koke, 2013

"""
Writes the c and cpp compile commands into build/compile_commands.json
see http://clang.llvm.org/docs/JSONCompilationDatabase.html

Usage:

    def configure(conf):
        conf.load('compiler_cxx')
        ...
        conf.load('clang_compilation_database')
"""

import json
from waflib import Logs, TaskGen
from waflib.Tools import c, cxx

@TaskGen.feature('*')
@TaskGen.after_method('process_use')
def collect_compilation_db_tasks(self):
	"Add a compilation database entry for compiled tasks"
	try:
		clang_db = self.bld.clang_compilation_database_tasks
	except AttributeError:
		clang_db = self.bld.clang_compilation_database_tasks = []
		self.bld.add_post_fun(write_compilation_database)

	for task in getattr(self, 'compiled_tasks', []):
		if isinstance(task, (c.c, cxx.cxx)):
			clang_db.append(task)

def write_compilation_database(ctx):
	"Write the clang compilation database as json"
	database_file = ctx.bldnode.make_node('compile_commands.json')
	Logs.info("Store compile comands in %s" % database_file.path_from(ctx.path))
	clang_db = dict((x["file"], x) for x in json.load(database_file))
	for task in getattr(ctx, 'clang_compilation_database_tasks', []):
		try:
			cmd = task.last_cmd
		except AttributeError:
			continue
		filename = task.inputs[0].abspath()
		entry = {
			"directory" : getattr(task, 'cwd', ctx.variant_dir),
			"command"   : " ".join(cmd),
			"file"	  : filename,
		}
		clang_db[filename] = entry
	database_file.write(json.dumps(clang_db.values(), indent=2))

