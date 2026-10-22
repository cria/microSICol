#!/usr/bin/env python
#-*- coding: utf-8 -*-
#This script is used to compress tinyMCE source code
import re #regexp module
import os #operational system module
js_files = ['editor_plugin_src.js']
for js_file in js_files:
  f = open(js_file,'r')
  f2 = open(js_file.replace("_src",""),'w')
  linhas = f.readlines()
  #1st level of compression - remove /* multi-line comments */
  wholefile = "\n".join(linhas)
  remove_inds = []
  start_index = 0
  count = 0
  last_letter = ''
  init_multicomment = False
  for letter in wholefile:
    if last_letter == '/' and letter == '*' and not init_multicomment:
      init_multicomment = True
      start_index = count-1
    if letter == '/' and last_letter == '*' and init_multicomment:
      init_multicomment = False
      remove_inds.append((start_index,count+1))
    last_letter = letter
    count += 1
  diff = 0
  for ind in remove_inds:
    wholefile = wholefile[:ind[0]-diff]+wholefile[ind[1]-diff:]
    diff += ind[1]-ind[0]
  linhas = wholefile.split("\n")
  #2nd level of compression
  newlinhas = []
  is_string = re.compile(r"\"(.*?)\"|'(.*?)'| in ",re.MULTILINE | re.DOTALL) #avoid getting lines with "a in b"
  #Remove extra spaces and commentaries such as '//....'
  for linha in linhas:
      linha = linha.strip()
      linha = re.sub(r"//[^'\"]*$",'',linha) #if commentary is not found, return string as is
      linha = re.sub(r"/[*](.*?)[*]/",'',linha) #remove /* content */
      #Further compression 
      #Conditions:
      # - when a line has no strings whatsoever
      # - don't remove spaces if code like "function a","new Array","else if","var ua","case 'x'","return true","new TinyMCE","a in b" appears
      newline = ''
      if not is_string.search(linha):
          linha = re.sub(r"//.*$",'',linha) #we are sure not to get strings like "http://" etc.
          linha = re.sub("(?<!var|lse|ase|urn|new|ion)\s",'',linha) #look-behind works with fixed-width patterns
      if linha.find("//") != -1: #Avoid commenting what shouldn't
          newline = '\n'
      if linha.find("else") == len(linha)-4:
          newline = '\n'
      if linha.find("return") == len(linha)-6:
          newline = '\n'
      if linha.find("new") == len(linha)-3:
          newline = '\n'
      if linha.find("var") == len(linha)-3:
          newline = '\n'
      if linha.find("case") == len(linha)-4:
          newline = '\n'
      if linha.find("function") == len(linha)-8:
          newline = '\n'
      if linha: #ignore empty lines
          newlinhas.append(linha + newline) 
  #Save compressed tinyMCE file
  f2.writelines(newlinhas)
  #Close files
  f.close();
  f2.close();
  #Warn user that process has ended
  fsize = os.path.getsize(f.name)
  f2size = os.path.getsize(f2.name)
  print("-------------------------------------")
  print("Status ["+js_file.replace("_src","")+"]")
  print("Compressed File = ",f2size," bytes")
  print("Source File = ",fsize," bytes")
  print("New size is %.2f%% of original size." % ((float(f2size)/float(fsize))*100.0))
print("-------------------------------------")
raw_input('Press Enter to quit...')
