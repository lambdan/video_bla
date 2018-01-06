import os
import sys
import subprocess
import hashlib

outputfile = "hashes.txt"

names = []
hashes = []

if os.path.isfile(outputfile):
	os.remove(outputfile)

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

for f in os.listdir("."):
	if f.endswith(".wav"):
		hashresult = hash_file(f)
		names.append(f)
		hashes.append(hashresult)
		print f + " = " + hashresult
		with open(outputfile, "a") as myfile:
			myfile.write(f + " = " + hashresult + "\n")

# Verify and see if there are dupes

dupes = {}
for i, h in enumerate(hashes):
	if hashes.count(h) > 1:
		dupes[names[i]] = h

if len(dupes) > 0:
	print "\nDuplicate found! These hashes cannot be used for renaming!"
	print "These files have the same hashes:"
	for n, h in dupes.items():
		print "\t" + n + " (" + h + ")"
	print "Go back to the extraction step, and edit the length in extract.bat to be longer (also change it in rename.py)"
	print "That should add more uniqueness."
	os.remove(outputfile)
else:
	print "All good! Copy hashes.txt to the folder with the unnamed files, along with rename.py"

raw_input("Press any key to exit...")
sys.exit(1)