# Introduction #

Waf already supports quite a number of tools (gcc, g++, java, python, intltool etc. etc.) that compile software. If you happen to use a tool that waf does not support yet this page describes how to add that support. Once you have written the code please file an issue in our [Issue tracker](http://code.google.com/p/waf/issues/list) and attach the patch, or send it to the [development mailing list](http://groups.google.com/group/waf-users)

# Waf tool definition #

A Waf tool is a file located in the `wafadmin/Tools` folder. It is used to extend the Waf behavior in the following areas:
  1. detect project settings (when running `waf configure`)
  1. provide additional configuration helpers (detecting libraries)
  1. provide code for building files (define how to compile c++ code)

The Waf tools contain python code in no particular order, except for the function `detect(conf)`. It is executed during the configuration, when the code `conf.check_tool('tool_name')` is called

# Writing Waf tools #

## 1. Detecting the project settings ##

The body of the function `detect(conf)` is used to detect the configuration:
  * the `conf` object is an instance of `Configure.Configuration`
  * the attribute `conf.env` holds the configuration variables: `print conf.env['CXX']`
  * `conf.env` can be modified to store the project configuration, for example `conf.env['CXX'] = 'g++'`
  * the conf object has various methods (find\_program, check\_library) to help configuring the project
  * `detect(conf)` does not return any special value

## 2. Extending the Configuration class ##

The `conf` object can be extended by **attaching** new methods to it (`conf.hook`). The methods usually throw `ConfigurationError` if something fails.

The purpose is to extend the configuration routines and to limit the amount of `import` to write.

Here is a quick example (the module `checks.py` provides several useful examples):
```
def check_dummy(self):
    return True
def detect(conf):
    "attach the checks to the conf object"
    conf.hook(check_dummy)
    # now use the hook attached to the conf instance
    result = conf.check_dummy()
```

## 3. Defining new compilation rules ##

Waf separates the high-level interfaces (declaring programs, shared libraries) from the low-level tasks (compile this file and add the results to the files to link). The user script almost never access the low-level apis, but this is needed for defining new kinds of file processing.

The elements needed for defining new compilation rules are the following (they are not all needed):
  * Defining new Tasks
  * Extending the class task\_gen
  * Adding file extensions

### a. Defining new Tasks ###

Waf decomposes the file transformations into units of change. These units are called `tasks`, they can be linked to other tasks, and they can be run in parallel or one by one (depending on the constraints).

The `Task` objects can be created in three ways:
  * Using `Tass.simple_task_type`
  * Using `Task.task_type_from_func`
  * using the `Task` constructor

The most popular way is to use the `simple_task_type`:
```
Task.simple_task_type('task_name', '${COMPILER} ${SRC} > ${TGT}', color='BLUE', prio=40)
```
The variables such as `${COMPILER`} represent environment variables, while the `SRC` and `TGT` are special variables representing the input and output files

Another optional way is to define your own 'builder' function, then call `task_type_from_func`:
```
Task.task_type_from_func('task_name', builder_func, color='CYAN', prio=120)
```

### b. Extending the class task\_gen ###
The classes instantiated when calling `bld.create_obj` are instances of `Object.py::task_gen`. That class provides settings for calling methods (adding, removing, changing methods is possible), and for declaring the order in which to call the code.

The core of the `task_gen` class is the method `apply` which takes the methods to execute, performs a topological sort on them, and calls them one by one (code execution in parallel would even be possible).

Here is how to declare a new method on task\_gen:
  * use the following imports `from Object import after, before, taskgen, feature`
  * write a function with a unique parameter: `def function(self):`
  * add the decorator `@taskgen` to attach a function to the task\_gen class
  * use the decorators `@after('apply_core')` or `@before('apply_core')` to set the order
  * use the decorator `@feature('name')` to declare the feature it belongs to. Features like cc, cxx, are used to add groups of methods upon execution

The new methods may perform the following operations:
  * modify the state of the `task_gen` instance (change attributes)
  * create `task` instances
  * modify the environment instance
  * add or remove methods, even if the method sorting has been performed

As an example:
```
from Object import taskgen, after, before, feature
@taskgen
@after('apply_core')
@before('install_target')
@feature('cc')
def special_install(self):
   if not getattr(self, "special", None): return
   print "disabling the regular installation"
   self.inst_var = 0
```

### c. Adding file extensions ###

The class `task_gen` usually executes the method `apply_core` which is used to process the source files (the "source" attribute).

The source files are transformed one by one into `Node` objects and are added to a temporary list. The list is then processed using a mapping `file_extension -> method`

Here is how to declare a new extension that process files of extension ".coin" into ".cpp" files:
```
from Object import extension

@taskgen
@extension('.coin')
def coin_file(self, node):
    out_source = node.change_ext('.cpp')

    tsk = self.create_task('task_name')
    tsk.set_inputs(node)
    tsk.set_outputs(out_source)

    # the out file is to be processed as a cpp file
    self.allnodes.append(out_source)
```

## 4. Implementation details ##

Instead of adding types, subtypes, and extensions through inheritance on task\_gen (msvc.py), the following scheme is now used:
  1. until a task generator is posted (asked to create the tasks), nothing happens
  1. when posted, the table of features are used to add groups of methods
  1. the methods inserted are reordered with the ordering constraints (topological sort)
  1. the methods are then called one by one for creating the tasks

Here are a few examples, they only represent the ideas, not the actual code:
  * if a task\_generator has an attribute "cpp", the methods "apply\_defines" and "apply\_core" are added to the list of methods to execute
  * if it has an attribute "shlib", the method "create\_shlib" is added
  * if msvc is to be used (env['MSVC']==True), the "create\_shlib" method is replaced by "create\_shlib\_msvc"

Using such meta-data adds enough abstraction without impacting performance (calling fewer methods) or flexibility (the methods can be added manually, or inheritance is still possible).