#! /usr/bin/env python 
# -*- coding: utf-8 -*-

import os
import sys

for path in os.listdir("."):
    if path.endswith(".po"):
        os.system("msgfmt %s" % path)
        code = path.rsplit(".",1)[0]
        print code
        try:
            os.mkdir(code)
            os.mkdir (os.path.join(code, "LC_MESSAGES"))
        except:
            pass
        if sys.platform[0].lower() == "w":
            cp_bin = "copy"
        else:
            cp_bin = "cp"
        os.system("%s messages.mo %s%sLC_MESSAGES%ssicol.mo"  %
            (cp_bin, code, os.path.sep, os.path.sep ) )
        