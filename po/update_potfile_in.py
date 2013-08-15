#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys, os

search_dirs = ["py", "js"]
exclude_dirs = [".svn", "external"]
extensions = ["py", "js", "pyw"]
output_file = "POTFILES.in"

def get_file_list(search_dirs = search_dirs, exclude_dirs = exclude_dirs, extensions = extensions, sep = '/', append_nl = True):
    file_list = []
    for search_dir in search_dirs:
        for root, dirs, files in os.walk(os.path.join("..", search_dir)):
            for exclude_dir in exclude_dirs:
                if exclude_dir in dirs:
                    dirs.remove(exclude_dir)
            for file in files:
                if file.split(".")[-1] in extensions:
                    name = root.split(os.path.sep)
                    # "/" is used for intltool-update - regardless
                    #of the system
                    name = sep.join (name[1:] + [file])
                    if append_nl:
                        file_list.append(name + "\n")
                    else:
                        file_list.append(name)
    return file_list
def main(*argv):
    file_list = get_file_list()
    of = open (output_file, "wt")
    of.writelines(file_list)
    of.close()
  
if __name__ == "__main__":
    main (*sys.argv)
