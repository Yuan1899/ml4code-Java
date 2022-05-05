import os
import sys
import shutil
import textwrap
import re
import javalang
import random
import string
import numpy as np
import csv
from datetime import datetime

counter = 0

# JavaClass: receives a `path` of a Java file, extracts the code,
# converts the code from Allman to K&R, extracts the methods,
# and creates a list of JavaMethod objects.
class JavaClass:
	def __init__(self, path):
		self.src = JavaClass._extract_code(path)
		self.src = JavaClass._allman_to_knr(self.src)
		self.methods = JavaClass.chunker(self.src)
		self.method_names = [method.name for method in self.methods]

	# __iter__: iterate through the methods in the JavaClass.
	def __iter__(self):
		return iter(self.methods)

	# _extract_code: receives a `path` to a Java file, removes all comments,
	# and returns the contents of the file sans comments.
	@staticmethod
	def _extract_code(path):
		with open(path, 'r') as content_file:
			contents = content_file.read()
			contents = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", contents)
			contents = re.sub(re.compile("//.*?\n"),  "", contents)
			return contents

	# tokens: A getter that returns a 1-dimensional space-delimited
	# string of tokens for the whole source file.
	def tokens(self):
		tokens = javalang.tokenizer.tokenize(self.src)
		return [" ".join(token.value for token in tokens)][0]

	# find_occurences: Returns a list of all occurrences of
	# a character `ch` in a string `s`.
	@staticmethod
	def find_occurrences(s, ch):
		return [i for i, letter in enumerate(s) if letter == ch]

	# _allman_to_knr: Converts a string `contents` from the style of
	# allman to K&R. This is required for `chunker` to work correctly.
	@staticmethod
	def _allman_to_knr(contents):
		s, contents = [], contents.split("\n")
		line = 0
		while line < len(contents):
			if contents[line].strip() == "{":
				s[-1] = s[-1].rstrip() + " {"
			else:
				s.append(contents[line])
			line += 1
		return "\n".join(s)

	# chunker: Extracts the methods from `contents` and returns
	# a list of `JavaMethod` objects.
	@staticmethod
	def chunker(contents):
		r_brace = JavaClass.find_occurrences(contents, "}")
		l_brace = JavaClass.find_occurrences(contents, "{")
		tokens = javalang.tokenizer.tokenize(contents)
		guide, chunks = "", []
		_blocks = ["enum", "finally", "catch", "do", "else", "for",
				   "if", "try", "while", "switch", "synchronized"]

		for token in tokens:
			if token.value in ["{", "}"]:
				guide += token.value

		while len(guide) > 0:
			i = guide.find("}")
			l, r = l_brace[i - 1], r_brace[0]
			l_brace.remove(l)
			r_brace.remove(r)

			ln = contents[0:l].rfind("\n")
			chunk = contents[ln:r + 1]
			if len(chunk.split()) > 1:
				if chunk.split()[0] in ["public", "private", "protected"] and "class" not in chunk.split()[1]:
					chunks.append(JavaMethod(chunk))
			guide = guide.replace("{}", "", 1)
		return chunks


# JavaMethod: receives a `chunk`, which is the method string.
class JavaMethod:
	def __init__(self, chunk):
		self.method = chunk
		self.name = chunk[:chunk.find("(")].split()[-1]

	# tokens: a getter that returns a 1-dimensional space-delimited
	# string of tokens for the method.
	def tokens(self):
		tokens = javalang.tokenizer.tokenize(self.method)
		return [" ".join(token.value for token in tokens)][0]

	# __str__: String representation for a method.
	def __str__(self):
		return self.method

	# __iter__: Iterator for the tokens of each method.
	def __iter__(self):
		tokens = javalang.tokenizer.tokenize(self.method)
		return iter([tok.value for tok in tokens])


file  = open("data_method.txt", "a")

for dirpath, dirs, files in os.walk("./Clean"):
	for filename in files:
		fname = os.path.join(dirpath,filename)

		if "Before" in fname:		

			if fname.endswith('.java'): #and counter <1000:
				fname_sibling = fname
				fname_sibling = re.sub(re.compile("Before"), "After", fname_sibling)	
				print("Name:    " + fname)
				print("Sibling: " + fname_sibling)	

				try:
					j = JavaClass(fname)
					j_sibling = JavaClass(fname_sibling)
					
					for method in j.methods:
						same = 0
						counter +=1
						for method_sibling in j_sibling.methods:
							code = str(method)
							code_sibling = str(method_sibling)

							if code == code_sibling:
								same = 1

							code = textwrap.dedent(code)
							code = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", code)
							code = re.sub(re.compile("//.*?\n"),  "", code)

							code = os.linesep.join([s.strip() for s in code.splitlines() if s])

							focus = method.tokens().split("(", 1)

						if same == 0:
							# there is no exact matching method, this means it was vulnerable and changed
							entry = "{} CVE-000.c cfunc 000 \n{}\n1\n---------------------------------".format(counter, code)
						else:
							entry = "{} CVE-000.c cfunc 000 \n{}\n0\n---------------------------------".format(counter, code)
						file.write(entry)
				except:
					pass

print("{} .java files with source code kept\n Done".format(counter))
