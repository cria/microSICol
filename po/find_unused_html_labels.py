#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys, os
import re
from update_potfile_in import get_file_list

search_dirs = ["html"]
exclude_dirs = [".svn"]
extensions = ["html"]

python_file = "../py/modules/labels.py"
python_regexp = re.compile(r"""^\s*['"](.*?)['"]\s*:""", re.MULTILINE | re.UNICODE)
html_regexp = re.compile(r"""\%\(([a-zA-Z0-9_]*?)\)s""", re.MULTILINE | re.UNICODE)

def main(*argv):
    if "all" in argv:
        mode = "all"
    else:
        mode = "normal"
    file_list = get_file_list(search_dirs, exclude_dirs, extensions, sep= os.path.sep, append_nl = False)
    python_labels_text = open(python_file, "rt").read().decode("utf-8")
    python_labels = {}
    out = ''

    for match in python_regexp.finditer(python_labels_text):
        label = match.groups()[0]
        line_number = python_labels_text.count("\n", 0, match.start()) + 1
        if not python_labels.has_key (label):
            python_labels[label] = []
        python_labels[label].append("Python Labels: %d - %s" % (line_number, label))
    
    html_labels = {}
    
    for html_file in file_list:
        file_content = open(os.path.join("..", html_file), "rt").read().decode("utf-8")
            
        for match in html_regexp.finditer(file_content):
            label = match.groups()[0]
            line_number = file_content.count("\n", 0, match.start()) + 1
            if not html_labels.has_key (label):
                html_labels[label] = []
            html_labels[label].append("\t%s:%d" % (html_file, line_number))
    
    if not "reverse" in argv:
        for label in sorted(python_labels.keys()):
            if mode == "all" or (mode=="normal" and not html_labels.has_key(label)) or len(python_labels[label]) > 1:
                if len(python_labels[label]) > 1:
                    out += "DUPLICATE LABEL on python side:"
                for l in python_labels[label]:
                    out += l
                if html_labels.has_key(label):
                    for l in html_labels[label]:
                        out += l
                out += '\n'
    else:
        for label in sorted(html_labels.keys()):
            if mode == "all" or not python_labels.has_key(label):
                out += "%s:" % label
                if python_labels.has_key(label):
                    for l in python_labels[label]:
                        out += l
                for l in html_labels[label]:
                    out += l
            out += '\n'

    arq = file("output.txt", 'wb')
    arq.write(out)
    arq.close()

if __name__ == "__main__":
    if "help" in sys.argv:
        print """\
        find_unused_html_labels [all] [reverse]
        Use this script to find out labels in py/modules/labels.py which are
        not used in the html templates under html/*html
        
        all: list all labels, even if they are used in the html templates
        
        reverse: list exitng html labels wich do not have a counterpart 
                 in the labels.py file
        """
        sys.exit(0)
    main(*sys.argv)
