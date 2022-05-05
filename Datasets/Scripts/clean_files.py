import os
import sys
import shutil
import tarfile

counter = 0

# Clean out any CVE-xxx folders that do not have source code included

print("Extracting original set of files")

for dirpath, dirs, files in os.walk("./Data"):	
	code = 0
	for filename in files:

		fname = os.path.join(dirpath,filename)
		# print(fname)
		if fname.endswith('.gz'):
			counter+=1
			code = 1
			# print(counter)
			
			tar = tarfile.open(fname, "r:gz")

			# print(dirpath)
			new_path = dirpath.split(os.sep)
			new_dir = "./Extracted/{}".format(dirpath.split(os.sep)[2])
			tar.extractall(path=new_dir)
			tar.close()
			# os.remove(fname)

			break
	
print("{} folders with source code kept".format(counter))
print("-----------------------------------------")
print("Organizing the .java source code files")


counter = 0

# Clean out everything that is not a .java file

for dirpath, dirs, files in os.walk("./Extracted"):
	for filename in files:

		fname = os.path.join(dirpath,filename)
# 		print(fname)
		if fname.endswith('.java'):
			counter +=1
			if "before" in fname:

				old_path = dirpath.split(os.sep)
				new_dir = "{}/{}/{}/{}/Before/".format(old_path[0], "Clean", old_path[2], old_path[3])
				new_path = "{}/{}".format(new_dir, filename)

				if not os.path.exists(new_dir):

					os.makedirs(new_dir)
				shutil.copy(fname, new_path)


			elif "after" in fname:

				old_path = dirpath.split(os.sep)
				new_dir = "{}/{}/{}/{}/After/".format(old_path[0], "Clean", old_path[2], old_path[3])
				new_path = "{}/{}".format(new_dir, filename)

				if not os.path.exists(new_dir):

					os.makedirs(new_dir)
				shutil.copy(fname, new_path)

print("{} .java files with source code kept\n Done".format(counter))
