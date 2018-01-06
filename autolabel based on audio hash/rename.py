import os
import shutil
import sys
import subprocess
import hashlib

HASHES_TXT = "hashes.txt"
input_extension = ".mkv"
renamed_file_extension = ".mkv" # include . !!! i recommend mkv as it can swallow anything
output_folder = "Renamed/"
length = 5 # must be same as in extract.bat

print "Settings:\n\tHashes txt = " + HASHES_TXT + "\n\tOutput Container = " + renamed_file_extension + "\n\tOutput Folder = " + output_folder + "\n\tAudio Length = " + str(length) + "\n"

if not os.path.isfile(HASHES_TXT):
	print HASHES_TXT + " not found. Cannot continue."
	raw_input("Press any key to exit...")
	sys.exit(1)

sr = raw_input("Do you want to Rename Now (Y), just test/dry-run (N) or exit (X)?: ")
if sr.lower() == "y":
	shouldrename = True
elif sr.lower() == "n":
	print "OK! I will NOT rename any files."
	shouldrename = False
else:
	sys.exit(1)

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

if not os.path.exists(output_folder): # we will move files we rename to avoid running through them again if the script would crash etc.
    os.makedirs(output_folder)

# read in hashes
old_names = []
old_hashes = []
with open(HASHES_TXT) as f:
	lines = f.readlines()
for l in lines:
	data = l.strip().split(" = ")
	old_names.append(data[0][:-4]) # name without .ext
	old_hashes.append(data[1])

names = []
hashes = []

#os.system("pause")

FNULL = open(os.devnull, 'w')

print "Hashing",

for f in os.listdir("."):
	if f.endswith(".mkv"):
		subprocess.call('ffmpeg -y -i "' + f + '" -t ' + str(length) + ' temp.wav', shell=True, stdout=FNULL, stderr=subprocess.STDOUT) # .mka is matroska audio, can contain any audio format. c:a:0 incase there are multiple tracks
		subprocess.call('ffmpeg -y -i temp.wav -c:a copy -t ' + str(length-1) + ' temp2.wav', shell=True, stdout=FNULL, stderr=subprocess.STDOUT) # .mka is matroska audio, can contain any audio format. c:a:0 incase there are multiple tracks
		current_hash = hash_file("temp2.wav")
		names.append(f)
		hashes.append(current_hash)
		print ".",

os.remove("temp.wav")
os.remove("temp2.wav")

print "done"
print "Checking for duplicate hashes",

dupes = {}
for i, h in enumerate(hashes):
	print ".",
	if hashes.count(h) > 1:
		dupes[names[i]] = h

no_matches = 0

if len(dupes) > 0:
	print "\nDuplicate found! Cannot continue."
	print "These files have the same hashes:"
	for n, h in dupes.items():
		print "\t" + n + " (" + h + ")"
	print "Go back to the extraction step, and edit the length in extract.bat to be longer (also change it in this script (rename.py))"
	print "If you still get the error even after doing that, there are probably two videos of the same episode"
	raw_input("Press any key to exit...")
	sys.exit(1)
else:
	print "done (none found)"
	for i, h in enumerate(hashes):
		old_name = names[i]
		try:
			new_name = old_names[old_hashes.index(h)] + renamed_file_extension
		except ValueError:
			no_matches += 1
			print "No match for " + old_name
			print "You can continue but you probably have to rename it manually"
			if no_matches > 4:
				print "Since you seem to be getting this error alot, maybe your length in extract.bat and rename.py aren't the same,"
				print "or maybe the audio was altered in the properly named videos?"
			raw_input("Press any key to continue...")
			continue

		if shouldrename == True:
			print "Renaming " + old_name + " --> " + new_name
			shutil.move(old_name, output_folder + new_name)
		else:
			print old_name + " == " + new_name

print "Done"
raw_input("Press any key to exit...")