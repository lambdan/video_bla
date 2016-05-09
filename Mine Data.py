# Requires query-handbrake-log (https://github.com/donmelton/video_transcoding) and Mediainfo
# Usage: put 'Mine Data.py' in folder with logs and mkvs and run it. 
# Recommend piping it out to a .txt, i.e. `python Mine\ Data.py > output.txt`
# Example output: https://dl.dropboxusercontent.com/u/60071552/friends_output.txt

import os
from subprocess import check_output

print "filename" + "\t" "video length" + "\t" + "bitrate" + "\t" + "avg. transcode fps" + "\t" + "transcode time" + "\t" + "size(MB)"

for file in sorted(os.listdir('.')):
	if file.endswith(".log") and not file.startswith("."):

		# Bitrate
		for line in check_output(["query-handbrake-log","b", file]).split(' '):
			b = line
			break

		# Time took encoding
		for line in check_output(["query-handbrake-log","t", file]).split(' '):
			t = line
			break

		# Encoding speed
		for line in check_output(["query-handbrake-log","s", file]).split(' '):
			s = line
			break
		
		# Filesize of output
		# file[:-4] strips .log, making the file ending in .mkv (i.e. the video!)
		z = os.path.getsize(file[:-4]) >> 20 # >> 20 to get in MB: http://stackoverflow.com/a/6080504

		# Length of video using Mediainfo
		for line in check_output(["mediainfo", '--Inform=Video;%Duration/String3%', file[:-4]]).split('\n'):
			length = line[:-4] # strip .MMM milliseconds, they're irrelevant
			break

		# Print out, tab separated
		print file[:-4] + "\t" + length + "\t" + b + "\t" + s + "\t" + t + "\t" + str(z)