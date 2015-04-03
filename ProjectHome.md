**WARNING: Waf is moving to github.**

Waf is a Python-based framework for configuring, compiling and installing applications. Here are perhaps the most important features of Waf:

  * **Automatic build order**: the build order is computed from input and output files, among others
  * **Automatic dependencies**: tasks to execute are detected by hashing files and commands
  * **Performance**: tasks are executed in parallel automatically, the startup time is meant to be fast (separation between configuration and build)
  * **Flexibility**: new commands and tasks can be added very easily through subclassing, bottlenecks for specific builds can be eliminated through dynamic method replacement
  * **Extensibility**: though many programming languages and compilers are already supported by default, many others are available as extensions
  * **IDE support**: Eclipse, Visual Studio and Xcode project generators (waflib/extras/)
  * **Documentation**: the application is based on a robust model documented in [The Waf book](http://docs.waf.googlecode.com/git/book_17/single.html) and in the [API docs](http://docs.waf.googlecode.com/git/apidocs_17/index.html)
  * **Python compatibility**: cPython 2.5 to 3.4, Jython 2.5, IronPython, and Pypy

Waf is used in particular by [innovative companies](http://code.google.com/p/waf/wiki/ProjectsUsingWaf) such as [Avalanche studios](http://www.avalanchestudios.se). In the open-source world, Waf is used by a few projects such as [Samba](http://www.samba.org/). Learn more about Waf by reading [The Waf book](http://docs.waf.googlecode.com/git/book_17/single.html).

For researchers and build system writers, Waf is also a framework for creating [custom build systems](http://code.google.com/p/waf/source/browse/build_system_kit/) and [package distribution systems](http://code.google.com/p/waf/source/browse/playground/distnet/README.rst)
