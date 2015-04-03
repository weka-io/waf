THE CONTENTS ON THIS PAGE ARE OBSOLETE

#summary Various code snippets for common use cases.

# Introduction #

It often happens that people have similar goals and needs when writing build scripts for Waf. And so it happens they write similar code. This page is intended to list some common examples of code which might be interesting for others and maybe re-used.


# Snippets #

### Retrieve latest change Subversion revision in current directory ###

Author: eht16 (Enrico Tröger)

Description: The following function reads the output of **svn info** and retrieves the revision number from the **Last Changed Rev** field in its output. The revision number is returned as a string object or '-1' if an error occurred.

Code:
```
import subprocess

def conf_get_svn_rev():
    try:
        p = subprocess.Popen(['svn', 'info', '--non-interactive'], stdout=subprocess.PIPE, \
                stderr=subprocess.STDOUT, close_fds=False, env={'LANG' : 'C'})
        stdout = p.communicate()[0]

        if p.returncode == 0:
            lines = stdout.splitlines(True)
            for line in lines:
                if line.startswith('Last Changed Rev'):
                    key, value = line.split(': ', 1)
                    return value.strip()
        return '-1'
    except:
        return '-1'
```

### Install post action ###

(author: dkovalkov)
```
def shutdown():
    if Options.commands['install']:
        # Your actions
        pass
```

### Disable install ###

(author: dkovalkov)
```
def build(bld):
    obj = bld(features='cxx cprogram')
    ...
    obj.install_path = None
```
For 1.6, you can also do it this way:
```
def build(bld):
    bld.program(install_path=None)
```

### Disable color output ###

(author: dkovalkov)
```
import Logs
Logs.colors_lst['USE'] = False
```
(.. or set NOCOLOR in the shell environment)

### Get the relative path from the caller wscript to the main wscript ###
```
def get_top_level(bld):
	'''
	Get the relative path from the caller wscript to main wscript.
	'''
        import traceback, os
	stack = traceback.extract_stack(limit=2)
	caller = os.path.dirname(stack[0][0])
	root = bld.srcnode.abspath()
	root_to_caller = caller[len(root):].strip(os.path.sep)
	caller_to_root = ''
	for entry in root_to_caller.split(os.path.sep):
		caller_to_root += '..' + os.path.sep

	caller_to_root = caller_to_root.rstrip(os.path.sep)

	return caller_to_root
```

### Run LINT on all source files ###

see playground/lint/