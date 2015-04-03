# General recommendations #

  * Make as little code as possible (unlike autotools, it is not necessary to have a script in each folder)
  * Look carefully at the demos provided with the Waf source code
  * Use the `uselib` features

# C/C++ specific #

  * Remove object files (files with extension `.o`) from the source directory
    1. they may cause build errors or unnecessary rebuilds
    1. there is a risk to add them to the source control
  * Avoid static libraries:
    1. copy pasting binary objects wastes space
    1. flag order is tricky to get right
    1. use bld.path.ant\_glob to match files across several folders
  * Move the `#ifdef` conditions to the configuration settings
    1. try to replace complicated structures such as `#if PROGRAM_VERSION(2, 4, 2)` by `#if VERSION_1`, where the defines are set in a config.h file
    1. errors should occur at configuration time, not at build time