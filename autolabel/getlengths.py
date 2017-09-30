import os
import sys
import subprocess

for f in os.listdir("."):
	if f.endswith(".mkv"):
		VID_LENGTH = (int(subprocess.check_output(["mediainfo", '--Inform=General;%Duration%', f]))/100)
		print f + "=" + str(VID_LENGTH)