#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import os, re
import update_potfile_in

# The regexp bellow will match strings marked for translation with " _(<string>) "  
#in the source code. It works for either python or javascript syntax,
#and has provisions for python multiline strings with the triple quote syntax.
#  IT WON´T WORK for the C style quote concatatenation over multiple lines

regexp = re.compile(r"""_\s*\(\s*(?:"(?=[^\"])|'(?=[^\'])|['"]{3})(.*?)(?:"(?=[^\"])|'(?=[^\'])|['"]{3})\s*\)""", re.UNICODE | re.MULTILINE |re.DOTALL)

def main():
    labels = {}
    file_list = update_potfile_in.get_file_list(sep = os.path.sep, append_nl = False)
    count = 0

    for file_name in file_list:
        file_content = open(os.path.join("..", file_name), "rt").read().decode("utf-8")
        
        for  match in regexp.finditer(file_content):
            #Verify if this line is comented out:
            if file_name.endswith("py"):
                comment = "#" in file_content[file_content.rfind("\n", 0 , match.start()) : match.start()]
            else: 
                comment = False
            if comment:
                continue
            label = match.groups()[0]
            line_number = file_content.count("\n", 0, match.start()) + 1
            if not labels.has_key(label):
                labels[label] = []
            labels[label].append("%s:%d\t\t_(\"%s\")" % (file_name, line_number, label))

    for label in sorted(labels.keys()):
        count += 1
        if len(labels[label]) > 1:
            for l in labels[label]:
                print l
            print
    print "Unique Count: %i" % count

if __name__ == "__main__":
    main()
