import sys
import re
from argparse import ArgumentParser
import os

parser = ArgumentParser(description='This script will align Subtitle translation files\n\r'+
						"How to Run?\n" +
						"python3 " + sys.argv[0] + " -i=input.txt" 
						)
parser.add_argument("-i", "--input", dest="inputfile",
					help="provide input file name",required=True)
parser.add_argument("-s", "--skip", dest="skipfile",
					help="provide skip lines number of reference file")
parser.add_argument("-o", "--outdir", dest="outdir",
					help="provide output directory name")

args = parser.parse_args()

inputfile = args.inputfile
skipfile = args.skipfile
outdir = args.outdir


#open file using open file mode
fp1 = open(inputfile) # Open file on read mode -- input file
lines = fp1.read().split("\n") # Create a list containing all lines
fp1.close() # Close file

#open file using open file mode
fp2 = open("offset") # Open file on read mode -- input file
offset = fp2.read().split("\n") # Create a list containing all lines
fp2.close() # Close file

offset_hash = {}
for o in offset:
	if o == "":
		continue
	off = o.split(",")
	offset_hash[off[0]] = off[2]

#cat_list = offset_hash.keys()
#print(offset_hash)
#exit()
pdgm_file_names = []
for i in range(1, len(lines), 7):
	cur_line = lines[i].rstrip()
	if(cur_line == ""):
		continue
	pdgm_file_names.append(cur_line)
	if (not os.path.isfile(cur_line)):
		fpw = open("out/" + cur_line, "w", encoding="utf-8")
		fpw.write(cur_line+"\n")
		fpw.close()
	#print(cur_line)

#for p in pdgm_file_names:
	#open file using open file mode
#	if (not os.path.isfile(p)):
#		fpw = open("out/" + p, "w", encoding="utf-8")
#		fpw.close()

files = os.listdir()

paradigm_hash = {}
#cat_list = []
for file in files:
	#print(file)
	if file.endswith(".p"):
		f = open(file)
		first = f.readline().rstrip()
		#cat_list.append(first)
		second = f.readline().strip()
		with open(file) as f:
			arr =  list(x.rstrip() for x in f)
		#print(arr)
		paradigm_hash[first] = arr[1:]
#print(paradigm_hash)
cat_list = offset_hash.keys()
#for p in pdgm_file_names:
	#print(p)
for c in cat_list:
	try:
		cur_list = paradigm_hash[c]
		offset2 = int(offset_hash[c])
		print(offset2)
		#print(p, c, offset)
	except:
		cur_list = []
		offset = []
		next
	count = 0
	#print(c, cur_list)
	for d in range(1, len(cur_list), offset2):
		#print(count, offset2)
		root = cur_list[count ]
		print(root, cur_list)
		#print(root, p, c)
		#if(root == p):
		end_index = count + offset2
		if(count ==0):
			start_index = count
		else:
			start_index = count + 1
		pdgm_slots = "\n".join(cur_list[start_index:end_index])
		print("iam",pdgm_slots, start_index, end_index)
		count = count + offset2
		fpw2 = open("out/" + root, "a", encoding="utf-8")
		fpw2.write(pdgm_slots + "\n")
		fpw2.close()
			#else:
			#count = count + offset
	#fpw.close()
		#print(arr)
"""		offset = int(offset_hash[first])
		print(first, second, offset)
		count = 1
		for d in range(1, len(arr), int(offset)):
			#print(d)
			pdgm_slot = "\n".join(arr[count:offset])
			tmp = count
			count = count + int(offset) -1
			#print(arr[count])
			try:
				arr[count]
				fpw = open("out/" + arr[tmp], "a", encoding="utf-8")
				fpw.write(pdgm_slot)
				fpw.close()
			except:
				count = count

			#print(d)
#print(paradigm_hash.keys())

#pdgm_file_names = paradigm_hash.keys()"""



	