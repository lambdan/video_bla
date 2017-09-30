import os
import sys
import subprocess

LABELED_TXT = "lengths of labeled.txt"
season = "S01"
shouldrename = False

# read in labeled lengths
LABELED = {}
with open(LABELED_TXT) as f:
	lines = f.readlines()
for l in lines:
	#print l.strip().split("=") # strip newline and split on =
	data = l.strip().split("=")
	LABELED[data[0]] = int(data[1])
# LABELED now contains labeled episodes and their length
#print LABELED

for f in os.listdir("."):
	if f.endswith(".mkv"):
		matches = 0
		newtitle = ""
		VID_LENGTH = (int(subprocess.check_output(["mediainfo", '--Inform=General;%Duration%', f]))/100)
		#print "Checking " + f + " with length " + str(VID_LENGTH)
		for title,length in LABELED.iteritems():
			if length == VID_LENGTH or length+1 == VID_LENGTH or length-1 == VID_LENGTH:
				if season in title:
					newtitle = newtitle + title
					matches += 1
		if matches == 0:
			print "!!! No matches: " + f
		elif matches == 1:
			print f + " ----> " + newtitle
			if shouldrename == True:
				os.rename(f, newtitle)
		elif matches > 1:
			print "*** Multiple matches: " + f + " (" + newtitle + ")"