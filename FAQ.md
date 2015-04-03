

# Waf Users #

# Who is who #

The project members are visible on the [front page](http://code.google.com/p/waf/)

# wscripts maintainers and Waf developers #
## paths ##

Q: why does foo.cpp compile to `foo.cpp.<n>.o` where `<n>` is some number?
A: else the same files might be compiled in different contexts and overwritten

## variants ##
(see also: [Variants](Variants.md))

### on build ###
get environment by variant name:
```
bld.env_of_name(variant_name)
```

# The waf philosophy #

## Why does not waf do more error checking on user scripts? ##

The waf approach is to provide an extensible build framework in which
only a few restrictions are enforced. Checks for common errors are executed
when calling "waf -v -v"

If more error checking is needed right now, the waf core functions
may be wrapped to perform stricter error checking.

## Why is packaging of waf in distributions discouraged? ##

With most build systems developers need to spend a lot of time and
effort ensuring that their projects will build correctly with many versions
of the build tool they use. This is needed because the developers have
very little control over the age of the distribution that their
package is being built on, and requiring that all people who want to
build their project update to a specific version of the build system
can be a significant burden.

You might think that this problem can be solved by careful design of
the build systems APIs, but history has shown that even with careful
design it is difficult to create a build system that avoids these
problems. For example, the venerable 'autotools' package that is so
widely used by free software packages has never managed to stabilise
its API enough to solve this problem. Many projects use a autogen.sh
script to cope with autotools variants and many others are shipping massive
'configure' scripts (sometimes several MB in size) with their projects
to avoid relying on the version of autotools installed on a users
system being able to work with their project.

The waf script is designed to be small enough to include with your
project, which completely avoids these issues and allows you to take
advantage of the latest additions to waf without ever being concerned
that your users may hit a problem that only happens with an earlier
version of waf.

If waf is packaged with distributions then end users may inadvertently
end up using the distribution version rather than the version that you
have carefully tested with your project.

You do still need a copy of python installed of course, but we have
put a lot of effort into waf to ensure it works well with a wide range
of python versions.


# Common problems and solutions #

## The same files are always built ##

  1. Understanding why
> > The following command may provide a few ideas `./waf -v --zones=task`
  1. Generated files already exist in the source directory
> > If generated files exist in the source directory, the file signature will be incorrect. Two possibilities exist:
      * remove the generated file from the source directory and call `waf clean build`
      * update the file signature, for example `bld(rule='touch ${TGT}', target='foo.txt', update_outputs=True)`
  1. Several object files use the same name as output
> > This occurs if the same source files are used to produce different times the same target files. If the same task generators are declared by accident, remove the duplicates. Or, if the intent is to create several similar targets, use variants.
> > In the case of c/c++ applications the object file extension can be changed, for example:
```
bld.program(
  idx    = 55,
  source = 'test.c',
  target = 'test1')

bld.program(,
  idx    = 66,
  source = 'test.c',
  target = 'test2')
```
  1. The command-line changes
> > If the order of the source file change, the command-line will be different, causing the corresponding task to be executed (sometimes randomly).

## The files are not recompiled when the headers change ##

The include paths should contain the paths where the headers are located, relative to the current wscript file: `obj.includes = '. .. src'`

Waf does not look in folders such as `/usr/include` for performance reasons. To add a dependency on an external folder easily, you may:
**compute a checksum of the needed headers, and add the checksum as a command-line parameter such as `-Dexternal=84509734`** compute a checksum of the needed headers and set conf.env.CCDEPS, conf.env.CXXDEPS and perhaps conf.env.LINKDEPS
**use from waflib import preproc; c\_preproc.go\_absolute = True**

## Turning off file content hashing ##

Waf hashes the file contents to obtain the version of the files. This is required for the WAFCACHE to operate properly. In rare cases it is necessary to turn off file content hashing (projects with more than 10000 files), this can be performed by replacing the hash function like this:
```
from waflib import Utils
import stat
def h_file(filename):
   st = os.stat(filename)
   if stat.S_ISDIR(st): raise IOError, 'not a file'
   m = md5()
   m.update(st.st_mtime)
   m.update(st.st_size)
   return m.digest()
Utils.h_file = h_file
```

## How do I build static C binaries? ##

For gcc, set conf.env.SHLIB\_MARKER = '-Wl,-Bstatic' to link all libraries in static mode, and add '-static' to the linkflags to make a fully static binary.

# General questions #

## translations, intltool, gettext, msgfmt ##

See demos/intltool in the waf distribution

## distcheck ##

Waf provides a 'distcheck' (similar to the one found in autotools) since waf 1.2

## checkinstall ##

Turn off the libc tricks:
checkinstall --fstrans=no --nodoc ./waf install --destdir=test

## How do I ask waf to continue in spite of errors, attempt to perform all tasks and finally show all errors? ##

Use the -k option when invoking waf build

## are there any licensing issues with including waf in your project? ##

Waf is distributed under the new BSD license (see http://www.opensource.org/licenses/bsd-license.php).

The waf developers consider including the waf script in your project to meet the conditions for a source distribution of waf. This means that as long as your project
is compatible with the BSD license (which nearly everythinig is!) then you are fine
including the waf script in your project source tree.

## where does the Waf name come from? ##

The name 'Waf' was the shortest and easily typed name we could find at the time. There is no particular meaning.