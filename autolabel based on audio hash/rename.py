import os
import shutil
import sys
import subprocess
import hashlib

HASHES_TXT = "hashes.txt"
renamed_file_extension = ".mkv" # include . !!! i recommend mkv as it can swallow anything
output_folder = "Renamed/"
length = 2 # must be same as in extract.bat

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
HASHES = {}
with open(HASHES_TXT) as f:
	lines = f.readlines()
for l in lines:
	data = l.strip().split(" = ")
	HASHES[data[0][:-4]] = data[1] # [:-4] to remove .ext from title
#print HASHES

#os.system("pause")

FNULL = open(os.devnull, 'w')

for f in os.listdir("."):
	if f.endswith(".mkv"):
		subprocess.call('ffmpeg -y -i "' + f + '" -t ' + str(length) + ' temp.wav', shell=True, stdout=FNULL, stderr=subprocess.STDOUT) # .mka is matroska audio, can contain any audio format. c:a:0 incase there are multiple tracks
		subprocess.call('ffmpeg -y -i temp.wav -c:a copy -t ' + str(length-1) + ' temp2.wav', shell=True, stdout=FNULL, stderr=subprocess.STDOUT) # .mka is matroska audio, can contain any audio format. c:a:0 incase there are multiple tracks
		current_hash = hash_file("temp2.wav")
		found_match = False
		for title,stored_hash in HASHES.iteritems():
			if current_hash == stored_hash:
				found_match = True
				#os.system("pause")
				if shouldrename == True:
					print "Renaming " + f + " --> " + title + renamed_file_extension
					shutil.move(f, output_folder + title + renamed_file_extension)
				else:
					print f + " == " + title
					#print f + " (" + current_hash + ")" + " == " + title + " (" + stored_hash + ")"
				continue
		if found_match is False:
			print "No match for " + f
			raw_input("Press any key to continue...")

os.remove("temp.wav")
os.remove("temp2.wav")

print "Done"
raw_input("Press any key to exit...")