# TranscodeVideos.py - transcode a bunch of videos and move or remove the originals
# (I used it for converting all my various .AVI files to x264 & AAC .MP4 files)
# https://github.com/lambdan/video_bla/blob/master/TranscodeVideos.py

import os
import subprocess
import sys
import shutil
import random
import time

# Configuration ##################

pathstxt = 'winpaths.txt' # path to txt file with all absolute paths to the avi files (or mpg etc). 
# you can use `ls -d -1 $PWD/**/*.avi` to get a list of fullpaths to avi files
donetxt = 'done.txt' # txt file with files we have done

mode = "move" # 'move' or 'remove' original files
movepath = './delete/' # originals will be moved here, end with a / !!!

# you should also change the transcode command in the transcode function below to suit your needs

# ################################

def transcode(inputfile, outputfile):
	print "\nTranscoding " + inputfile
	try:
		# transcode command
		subprocess.call(['ruby', os.path.abspath("C:/Ruby22-x64/bin/transcode-video"), '--audio-width', 'all=surround', '--no-log', '--small', '--mp4', inputfile, '--output', outputfile])
	except:
		error("Transcode failed",inputfile)

def verify(inputfile, outputfile):
	# verifies transcodes by comparing duration of original video and new video
	print "\nVerifying... ",

	try:
		originalLength = int(subprocess.check_output(['mediainfo', '--Inform=General;%Duration%', inputfile]))
	except: # original file probably contained an illegal character
		error("Illegal char or not good path",inputfile)
		addToDone(inputfile)
		return False
	
	# if the new output is corrupt, mediainfo wont return a length
	try:
		newLength = int(subprocess.check_output(['mediainfo', '--Inform=General;%Duration%', outputfile]))
	except: # corrupt
		newLength = 0

	diffLength = abs(originalLength - newLength)
	if diffLength > 5000: # 5 seconds in difference
		print "bad"
		return False
	else:
		print "ok!"
		return True

def moveOriginal(inputfile):
	# moves or removes original files
	if mode == "move":
		filename = os.path.basename(inputfile)
		dest = movepath + filename 
		if os.path.isfile(dest): # maybe file with identical name already exists
			i = 0
			while os.path.isfile(dest): # increase i until the new filename doesnt exist
				name, ext = os.path.splitext(filename)
				dest = movepath + name + "_" + str(i) + ext #suffix with _i
				i += 1	
		print "\nMoving original file...",
		shutil.move(inputfile, os.path.abspath(dest))
		print " ok!"
	elif mode == "remove" or "delete":
		print "\nRemoving original file...",
		os.remove(inputfile)
		print " ok!"
	else:
		print "Unsupported mode: " + mode
		sys.exit(1)


def addToDone(path):
	# adds the original files path to a txt so we can keep track of which we have done
	with open(donetxt, "a") as myfile:
		myfile.write(path)
	print "\nAdded to " + donetxt

def error(reason, path):
	# writes out error messages to a txt
	if not os.path.isfile('errors.txt'): # create file if not exist
		open('errors.txt', 'w').close()
		with open('errors.txt', "a") as myfile:
			myfile.write("These files have been skipped. You need to do these manually.\n\n")
	with open('errors.txt', "a") as myfile:
		myfile.write(reason + ": " + path + "\n")
	print "\nERROR: " + reason + ": " + path

# make sure we have all files we need to run
if not os.path.isfile(pathstxt):
	print 'Textfile "' + pathstxt + '" with paths to files to be processed not found. Please create one.'
	raw_input("Press the <ENTER> key to continue...")
	sys.exit(1)
if not os.path.isfile(donetxt):
	print 'Creating ' + donetxt
	open(donetxt, 'w').close()
if not os.path.isdir(movepath):
	print 'Creating ' + movepath + ' folder'
	os.makedirs(movepath)

x = 0 # this will be how many we have done
num_lines = sum(1 for line in open(pathstxt)) # count how many lines (files) we have to do 

with open(pathstxt) as f:
	for filepath in f:
		x += 1

		# check if we have already done this file
		donefiles = open(donetxt, 'r')
		donelist = donefiles.readlines()
		donefiles.close()
		found = False
		for line in donelist:
			if filepath in line:
				found = True
				#print "Already done: " + filepath[:-1]
				continue

		# we have not transcoded this video
		if found == False:
			if os.name == "nt":
				# set title of cmd window in windows to show how many files we've done
				os.system("title (" + str(x) + "/" + str(num_lines) + ") Converting: " + filepath[:-1])
				#TODO: do the same in unix

			# set up input and output filepaths
			inputfile = r"" + os.path.abspath(filepath[:-1]) + ""
			outputfile =  r"" + os.path.abspath(filepath[:-4] + 'mp4') + ""

			transcode(inputfile, outputfile)

			if verify(inputfile, outputfile): # good transcode on the first try, all good
				moveOriginal(inputfile)
				addToDone(filepath)
			else: # length differs by more than 5 seconds, or output is corrupt
				try:
					os.remove(outputfile)
				except: # file doesnt exist or original file had illegal character
					continue
				print "\nLength differs by more than 5 seconds, trying to make a new transcode"
				transcode(inputfile, outputfile)
				if verify(inputfile, outputfile): # succeeded now
					moveOriginal(inputfile)
					addToDone(filepath)
				else:
					os.remove(outputfile)
					error("Length kept on differing", filepath)
					addToDone(filepath)

			# give user some time to stop me
			print "\nSleeping 3 seconds"
			print "Hit CTRL C now to stop script"
			time.sleep(3)