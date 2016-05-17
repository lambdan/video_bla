# i use this to extract the Bright, Kauffman & Crane logo out of every Friends episode...
# tested/used on windows 10. probably works on unix/os x but change the FRIENDS_DIR and folder separator on line 43

import os
import subprocess
from subprocess import check_output
import sys
from PIL import Image

def get_main_color(file): # http://stackoverflow.com/a/2271013
    img = Image.open(file)
    colors = img.getcolors(1234567) #put a higher value if there are many colors in your image
    max_occurence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
        return most_present
    except TypeError:
        raise Exception("Too many colors in the image")

FRIENDS_DIR = "W:\RAW\TV\Friends (BR)"
TEMP_FILE = 'bkr_temp.jpg'
WHITE_LEVEL = 190 # over 190 should be white enough (blame s01e09), most are around 240-250

#check a single episode to see what its white level is (get the screenshot using mpc-hc or something)
#DOMINANT_COLOR = get_main_color("friends s01e09.mkv_snapshot_22.39_[2016.05.17_16.11.59].jpg")
#print DOMINANT_COLOR
#sys.exit(1)

if os.path.exists(TEMP_FILE):
	print "Removing old temp file: " + TEMP_FILE
	os.remove(TEMP_FILE)

for file in os.listdir(FRIENDS_DIR):
	if file.endswith('.mkv'):

		if os.path.exists(file + ".jpg"): # see if logo already exists for this episode
			print "Skipping: " + file + " (already exists)"
			continue

		print "Finding Bright, Kauffman, Crane logo for " + file
		VID_PATH = FRIENDS_DIR + "\\" + file

		# get video length, as we wanna start at the end
		VID_LENGTH = (int(check_output(["mediainfo", '--Inform=General;%Duration%', VID_PATH]))/1000) # divide with 1000 to get secs
		ORIG_VID_LENGTH = VID_LENGTH

		found_still = False
		DECREASE_VALUE = 2 # we start by checking every 2 seconds, if we cant find it after 30 seconds we go to 1 second

		while found_still is False:
			if (ORIG_VID_LENGTH-VID_LENGTH>15):
				if DECREASE_VALUE is 1:
					print ""
					print "Could not find logo for: " + file
					print "It probably has a very faded white (see s01e09 and s06e05)"
					print "Exiting..."
					sys.exit(1)
				else:
					DECREASE_VALUE = 1

			# screenshot the video using ffmpeg
			subprocess.call(['ffmpeg', '-ss', str(VID_LENGTH), '-i', VID_PATH, '-vframes', str(1), '-q:v', str(2), TEMP_FILE])

			# if ffmpeg tries to screenshot a non existent time it wont output any file
			if not os.path.exists(TEMP_FILE):
				# so if ffmpeg didn't output anything, check 1 sec earlier
				VID_LENGTH -= DECREASE_VALUE
				continue

			DOMINANT_COLOR = get_main_color(TEMP_FILE)
			for c in DOMINANT_COLOR:
				if c>WHITE_LEVEL: 
					found_still = True
				else:
					found_still = False
					os.remove(TEMP_FILE) # remove old
					VID_LENGTH -= DECREASE_VALUE # decrease seconds to check earlier
					break
		
		print str(file) + ": " + str(DOMINANT_COLOR) + " at time " + str(VID_LENGTH)

		# rename temp file to input mkv but add .jpg
		os.rename(TEMP_FILE, file + ".jpg")

		