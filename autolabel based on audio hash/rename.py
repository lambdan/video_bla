import os
import shutil
import sys
import subprocess
import hashlib

HASHES_TXT = "hashes.txt"
renamed_file_extension = ".mkv" # include . !!! i recommend mkv as it can swallow anything
audio_extension = ".ac3" # include . !!! should be same as your properly labeled versions
output_folder = "Renamed/"
shouldrename = False # edit this to actually start renaming


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
		subprocess.call('ffmpeg -y -i "' + f + '" -c:a:0 copy temp' + audio_extension, shell=True, stdout=FNULL, stderr=subprocess.STDOUT) # .mka is matroska audio, can contain any audio format. c:a:0 incase there are multiple tracks
		current_hash = hash_file("temp" + audio_extension)
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

os.remove("temp" + audio_extension)