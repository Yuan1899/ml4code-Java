import os
import sys
import shutil
import tarfile
import textwrap
import re

# (Naive) preprocess the .java files to match the VulDeePecker dataset format suitable to input into VulDeePecker replication tool
# Also perform some light code cleanup

counter = 0

file  = open("data.txt", "a")

for dirpath, dirs, files in os.walk("./Clean"):
	for filename in files:

		fname = os.path.join(dirpath,filename)
# 		print(fname)
		if fname.endswith('.java'): # and counter <1000:
			counter +=1
			# print(fname)
			if "Before" in fname:

				with open(fname, 'r') as f:
					code = f.read()
					if code == "":
						counter -=1
						break	
	
					code = textwrap.dedent(code)
					code = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", code)
					code = re.sub(re.compile("//.*?\n"),  "", code)
					code = re.sub(re.compile("import.*"), "", code)

					code = os.linesep.join([s.strip() for s in code.splitlines() if s])
					entry = "{} CVE-000.c cfunc 000 \n{}\n1\n---------------------------------\n".format(counter, code)
					file.write(entry)

			elif "After" in fname:

				with open(fname, 'r') as f:
					code = f.read()
					if code == "":
						counter -=1
						break	

					code = textwrap.dedent(code)
					code = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", code)
					code = re.sub(re.compile("//.*?\n"),  "", code)
					code = re.sub(re.compile("import.*"), "", code)

					code = os.linesep.join([s.strip() for s in code.splitlines() if s])
					entry = "{} CVE-000.c cfunc 000 \n{}\n0\n---------------------------------\n".format(counter, code)
					file.write(entry)

print("{} .java files with source code kept\n Done".format(counter))
