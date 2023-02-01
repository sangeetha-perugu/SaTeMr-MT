from argparse import ArgumentParser
import sys
import re

aper_fp = open("template.txt", "w") # Open file on appen mode -- sdef file

arr = ['sdef.txt', 'pardef.txt', 'dict.txt']

out_lines =[]
for a in arr:
	fp1 = open(a)
	lines = fp1.read()#.split("\n") # Create a list containing all lines
	out_lines.append(lines)
	fp1.close() # Close file


template_fp = '<?xml version="1.0"?>'
template_fp += '<dictionary>'
template_fp += '<alphabet>abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ</alphabet>'
template_fp += '<sdefs>'
template_fp += out_lines[0]
template_fp += '</sdefs>'
template_fp += '<pardefs>'
template_fp += out_lines[1]
template_fp += '</pardefs>'

template_fp += '<section id="main" type="standard">'
template_fp += out_lines[2]
template_fp += '</section>'
template_fp += '</dictionary>'

print(template_fp)
aper_fp.write(template_fp)
aper_fp.close()

