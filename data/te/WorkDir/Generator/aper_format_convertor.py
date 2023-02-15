#pip3 install pygtrie
#new dev commit
from argparse import ArgumentParser
import sys
import re
from collections import OrderedDict
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

meta_paradigm_flag = 0
if(re.search(r'\?', paradigm)):
	meta_paradigm_flag = 1
	paradigm = re.sub(r'\?', r'[i]', paradigm)

#features_hash = {}
features_hash =  	OrderedDict()
sdef = '<sdefs>\n'
sdef = '<sdef n="root:' + paradigm + '" c="'+paradigm+'"/>\n'
sdef += '<sdef n="lcat:' + cat +'" c="'+cat+'" />\n'
sdef += '<sdef n="gen:any" c="any"/>\n'
sdef += '<sdef n="per:any" c="any"/>\n'
sdef += '<sdef n="case:o" c="o"/>\n'
sdef += '<sdef n="case:d" c="d"/>\n'
sdef += '<sdef n="cm:0" c="0"/>\n'
sdef += '<sdef n="cm:obl" c="obl"/>\n'

line_no = 1
for line in lines[2::]:
	line = re.sub(r'  ', ' ', line)
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
		if(re.search(r'#', form)):
			case_flag = 1
			cform = re.sub(r'#', '', form)
		else:
			case_flag = 0
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
		#feature_value = '\n<!--pcdatalineno=' + str(line_no) + '-->\n'
		feature_value = '<s n="root:' + paradigm + '"/><s n="lcat:' + cat +'"/>'
		feature_value += '<s n="gen:any"/>'
		case = 'o'
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
			elif(re.search(r'case', features[i])):
				case = features[i+1]
				i = i + 1
			else:
				#case = 'o'
				i = i + 1
		#print(form)
		feature_value += '<s n="case:' + case +'"/><s n="cm:' + suff + '"/><s n="suffix:' + suff + '"/>'
		sdef += '<sdef n="cm:' + suff +'" c="'+suff+'" />\n<sdef n="num:' + number +'" c="'+number+'" />\n<sdef n="suffix:' + suff + '" c="'+suff+'"/>\n'
		cform = cform + "____line_no____" + str(line_no)
		if(lr_flag == 1):
			if(cform in features_hash):
				cur_val = features_hash[cform]
				features_hash[cform] = cur_val + "	" + feature_value
			else:
				features_hash[cform] = feature_value
		else:
			if(cform in features_hash):
				cur_val = features_hash[cform]
				features_hash[cform] = cur_val + "	" + feature_value + 'LR_FLAG'
			else:
				features_hash[cform] = feature_value + 'LR_FLAG'
	line_no = line_no + 1

strings = list(features_hash.keys())
#print(strings)
max_match = os.path.commonprefix(strings)
#print("Iam",max_match)

rem = re.sub(max_match, '', paradigm)
rem_orig = rem

out_content = '<?xml version="1.0"?>\n<dictionary>\n<alphabet>abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ</alphabet>\n'
#out_content = sdef #+ '</sdefs>'
sdef_fp.write(sdef)
#out_content += '<pardefs>'
out_content = '<pardef n="' + max_match + '/' + rem_orig + '__n">\n'

if(meta_paradigm_flag == 1):
	rem = re.sub(r'\[[a-z]\]', '<prm/>', rem)

dict_content = ''

for s in strings:
	val = features_hash[s]

	num = re.sub(r".*____line_no____([0-9]+)", r'\1', s)
	s = re.sub(r'____line_no.*$', '', s)
	left = re.sub(max_match, '', s)
	if(meta_paradigm_flag == 1):
		left = re.sub(r'\[[a-z]\]', '<prm/>', left)	
	
	for v in val.split("	"):
		out_content +='\n<!--pcdata line number='+ num +'-->\n'
		out_content += '<e><p><l>'
	
		out_content += left
		out_content += '</l>'
		if(re.search(r'LR_FLAG', v)):
			v =  re.sub(r'LR_FLAG', '', v)
			out_content += '<r e="LR">'+ rem + v + '</r></p></e>\n'
		else:
			out_content += '<r>'+ rem + v + '</r></p></e>\n'

#dict_content += '<section id="main" type="standard">\n'
dict_root = re.sub(r'____.*$', '', strings[0])
dict_content += '<e lm="' + dict_root + '">'
if(meta_paradigm_flag == 1):
	max_match = re.sub(r'\[[a-z]\]', '<prm/>', max_match)
	dict_content += '<i>' + max_match + '</i><par n="' + max_match + '/' + rem_orig + '__n"/ prm="i" ></e>\n'
else:
	dict_content += '<i>' + max_match + '</i><par n="' + max_match + '/' + rem_orig + '__n"/></e>\n'
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
