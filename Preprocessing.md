# C/C++ Dependencies in waf #

The module ccroot.py contains the base class for all c/c++ programs/libraries/objects:
  * add the include paths
  * add the defines
  * create the tasks (c/c++ or other that produce c source)
  * add the library flags
  * add extra object files

Source files are not analyzed until all c/c++ tasks are created. To infer the dependencies on the c/c++ source files, scanner classes are used. The roles of the scanner classes are:
  * to find the files on which the sources depend
  * create a signature of a c/c++ task in a consistent manner to know if it needs to be run

The scanners can currently operate on two modes:
  * scan raw `#include` lines in the source
  * preprocess the source files when they change (default behaviour)

# System includes #

To scan the files in reasonable time, waf does not look for includes on the system like /usr/include, this means that for a block like this, the "foo.h" include will be ignored if the macro is not defined within the project:
```
#if MY_EVIL_MACRO(5, 6, 234)
  #include "foo.h"
#endif
```
To make the project more modular and maintainable, it is recommended to put all platform-specific test that lead to include changes into a configuration header (config.h), and to use simple configuration defines:
```
#ifdef IS_WIN32
  #include "foo.h"
#endif
```

# Strict quotes #

With the following:
```
import preproc
preproc.strict_quotes=1
```
only includes using double quotes will be used:
```
#include "foo.h" /* will be considered */
#include <bar.h> /* will be ignored */
```

The strict behaviour is disabled (0) by default.

# Configuration header : config.h #

A script similar to this one:
```
VERSION='0.0.1'
APPNAME='cc_test'

srcdir = '.'
blddir = 'build'

def set_options(opt):
        pass

def configure(conf):
        conf.check_tool('gcc')

        conf.define('HELLO', None)
        conf.define('NAME', 'ita')
        conf.define('ANOTHER', 1)
        conf.write_config_header('config.h')

def build(bld):
        obj = bld.create_obj('cc', 'program')
        obj.source = 'main.c'
        obj.target = 'test'
        obj.includes = '.'
```


will produce a configuration header named `config.h` in the build dir `build` with the following content upon `waf configure`:
```
/* configuration created by waf */
#ifndef _CONFIG_H_WAF
#define _CONFIG_H_WAF

#define HELLO
#define ANOTHER 1
#define NAME "ita"

#endif /* _CONFIG_H_WAF */
```

The defines are stored on `conf.define`, to write several configuration headers, it may be necessary to reset the values:
```
conf.define('foo')
conf.write_config_header('config1.h')

conf.defines = {}
conf.define('bar')
conf.write_config_header('config2.h')
```