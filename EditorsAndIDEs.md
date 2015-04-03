# Editors #

It is recommended to include a header in wscript files
```
#! /usr/bin/env python
# encoding: utf-8
```

## Vim ##

Sometimes the developers will omit it, making it difficult to read in text editors. Here is a line to add to the ~/vimrc file:
```
au BufNewFile,BufRead wscript* set filetype=python
```

The build outputs can be parsed by vim to scroll to the errors. Use the following to build with waf:
```
:set makeprg=waf
```

## Emacs ##

In emacs put this into yout .emacs file:
```
(setq auto-mode-alist (cons '("wscript" . python-mode) auto-mode-alist))
```