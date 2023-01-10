#pip3 install pygtrie
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

# Create a trie with the words you want to match against
#trie =pytrie.SortedStringTrie()
#print(trie)

cat = lines[0]
paradigm = re.sub(r'\t', '', lines[1])

features_hash = {}

for line in lines[2::]:
	current_line = line.split("\t")
	#print(line)
	if(line == ""):
		continue
	current_form = current_line[0]
	forms = current_form.split("/")
	for form in forms:
		if(form == "-"):
			continue
		cform = re.sub(r'\*', '', form)
		#print(cform)
		features = current_line[1].split(" ")
		i=1
		#print(len(features))
		feature_value = ''
		while (i<len(features)):
			#print(i)
			f = features[i]
			if(re.match(r'num', features[i])):
				feature_value += '<s n="num:' + features[i+1] +'"/>'
				i = i + 1
			elif(re.match(r'parsarg', features[i])):
				suff = features[i+1]
				feature_value += '<s n="parsarg:' + features[i+1] +'"/>'
				i = i + 1
			else:
				i = i + 1
		#print(form)

		feature_value += '<s n="gen:any"/><s n="per:any"/>'
		feature_value += '<s n="case:o"/><s n="cm:0"/><s n="suffix:' + suff + '"/>'
		features_hash[cform] = feature_value

strings = list(features_hash.keys())
#print(strings)
max_match = os.path.commonprefix(strings)
rem = re.sub(max_match, '', paradigm)

out_content = '<paradef n="' + max_match + '/' + rem + '__n">\n'
for s in strings:
	out_content += '<e><p>\n<l>'
	left = re.sub(max_match, '', s)
	out_content += left
	out_content += '</l>\n'
	out_content += '<r>'+ rem + features_hash[s] + '</r>\n</e></p>\n'

out_content += '</paradef>\n'
#print(s)
print(out_content)
#print(max_match)
#print(max_match)
#print(features_hash)