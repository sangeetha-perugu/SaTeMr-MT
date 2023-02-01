#pip3 install pygtrie
#new dev commit
from argparse import ArgumentParser
import sys
import re
#	import pytrie
import os.path



parser = ArgumentParser(description='This script will generate apertium dict format \n\r'+
						"How to Run?\n" +
						"python3 " + sys.argv[0] + " -i=noun.p" + " -o=apertium.dict"
						)
parser.add_argument("-i", "--input", dest="inputfile",
                    help="provide paradigm file name",required=True)
#parser.add_argument("-o", "--output", dest="outfile",
#                    help="provide output file name like apertium.dict",required=False)

args = parser.parse_args()

inputfile = args.inputfile
#outfile = args.outfile

#if outfile is None:
#	outfile = 'out.txt'

#open file using open file mode
fp1 = open(inputfile) # Open file on read mode -- input file
lines = fp1.read().split("\n") # Create a list containing all lines
fp1.close() # Close file

#open file using open file mode
sdef_fp = open("sdef.txt", "a") # Open file on appen mode -- sdef file
paradef_fp = open("pardef.txt", "a") # Open file on appen mode -- pardef file
dict_fp = open("dict.txt", "a") # Open file on appen mode -- pardef file


# Create a trie with the words you want to match against
#trie =pytrie.SortedStringTrie()
#print(trie)

cat = lines[0].strip()
paradigm = re.sub(r'[\t ]+', '', lines[1]).strip()

features_hash = {}
sdef = '<sdefs>\n'
sdef = '<sdef n="root:' + paradigm + '" c="'+paradigm+'"/>\n'
sdef += '<sdef n="lcat:' + cat +'" c="'+cat+'" />\n'
sdef += '<sdef n="gen:any" c="any"/>\n'
sdef += '<sdef n="per:any" c="any"/>\n'
sdef += '<sdef n="case:o" c="o"/>\n'
sdef += '<sdef n="cm:0" c="0"/>\n'

for line in lines[2::]:
	current_line = line.split("\t")
	#print(line)
	if(line == ""):
		continue
	current_form = current_line[0]
	forms = current_form.split("/")
	for form in forms:
		form = form.strip()
		#print("1",form)
		if(form == "-" or form == ""):
			continue
		if(re.search(r'\*', form)):
			lr_flag = 1
			cform = re.sub(r'\*', '', form)
		else:
			cform = form
			lr_flag = 0
		#print("2",cform)
		features = current_line[1].split(" ")
		i=1
		#print(len(features))
		feature_value = '<s n="root:' + paradigm + '"/><s n="lcat:' + cat +'"/>'
		feature_value += '<s n="gen:any"/>'

		while (i<len(features)):
			#print(i)
			f = features[i]
			if(re.search(r'num', features[i])):
				if(re.search(r'eka',features[i+1])):
					number = 'sg'
				else:
					number = 'pl'
				feature_value += '<s n="num:' + number +'"/><s n="per:any"/>'
				i = i + 1
			elif(re.search(r'parsarg', features[i])):
				suff = features[i+1]
				#feature_value += '<s n="parsarg:' + features[i+1] +'"/>'
				i = i + 1
			else:
				i = i + 1
		#print(form)

		feature_value += '<s n="case:o"/><s n="cm:0"/><s n="suffix:' + suff + '"/>'
		sdef += '<sdef n="num:' + number +'" c="'+number+'" />\n<sdef n="suffix:' + suff + '" c="'+suff+'"/>\n'
		if(lr_flag == 1):
			features_hash[cform] = feature_value
		else:
			features_hash[cform] = feature_value + 'LR_FLAG'

strings = list(features_hash.keys())
#print(strings)
max_match = os.path.commonprefix(strings)
rem = re.sub(max_match, '', paradigm)

out_content = '<?xml version="1.0"?>\n<dictionary>\n<alphabet>abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ</alphabet>\n'
#out_content = sdef #+ '</sdefs>'
sdef_fp.write(sdef)
#out_content += '<pardefs>'
out_content = '<pardef n="' + max_match + '/' + rem + '__n">\n'

dict_content = ''

for s in strings:
	out_content += '<e><p>\n<l>'
	left = re.sub(max_match, '', s)
	out_content += left
	out_content += '</l>\n'
	if(re.search(r'LR_FLAG', features_hash[s])):
		val = features_hash[s]
		val =  re.sub(r'LR_FLAG', '', val)
		out_content += '<r e="LR">'+ rem + val + '</r>\n</p></e>\n'
	else:
		out_content += '<r>'+ rem + features_hash[s] + '</r>\n</p></e>\n'

#dict_content += '<section id="main" type="standard">\n'
dict_content += '<e lm="' + strings[0] + '">'
dict_content += '<i>' + max_match + '</i><par n="' + max_match + '/' + rem + '__n"/></e>'
#dict_content + ='</section>\n'

out_content += '</pardef>\n'
#out_content += '</pardefs>\n'
#out_content += dict_content
paradef_fp.write(out_content)
dict_fp.write(dict_content)
#out_content += '</dictionary>\n'
#print(s)
print(out_content)
#print(max_match)
#print(max_match)
#print(features_hash)
