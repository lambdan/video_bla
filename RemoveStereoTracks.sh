#!/bin/bash

# I use this to remove stereo tracks from files that have both a AC3 5.1 and a Stereo track, as I only need the 5.1 track
# Put the script in the same folder as mkv/mp4s, then run './RemoveStereoTracks.sh mkv delete' to remove them from MKV files and remove original files
# './RemoveStereoTracks.sh mp4' to remove from MP4 files, but keep original files

# WARNING
# CANCELLING THIS SCRIPT (CTRL C) CAN HAVE VERY BAD RESULTS
# IF YOU NEED TO CANCEL I RECOMMEND MOVING THE FILES TO ANOTHER FOLDER,
# THEN YOU CAN CANCEL AS IT CANT REMOVE THE FILES

if [ "$1" = "mp4" ]; then
	format="mp4"
elif [ "$1" = "mkv" ]; then
	format="mkv"
else
	echo "Usage: $0 <mkv/mp4> [delete]"
	echo "Will process all mkv/mp4 in current folder."
	echo "Adding delete after format will remove original file"
  	exit
fi

total=0

OS_NAME=$(uname -s)
OS_NAME=${OS_NAME:0:6}
if [[ "$OS_NAME" = "CYGWIN" ]]
then
    acstring="AC-3" # for some reason I get AC-3 on Windows from mkvmerge
else
    acstring="AC3"
fi


for f in *."$format"
do
	before=`du -m "$f" | cut -f1` # file size before

	# Find out which track is AC3
	# Change AC3 to AC-3 if on windows
	mkvmerge -i "$f" | grep "$acstring" | while read subline
	do
		tracknumber=`echo $subline | egrep -o "[0-9]{1,2}" | head -1`
		echo "$tracknumber" > /tmp/temptracknumber # write out to temp file
	done
	read -r -a tracknumber < /tmp/temptracknumber # read it back (bash is dumb, no global variables)

	mkvmerge -o "temp.$format" --audio-tracks "$tracknumber" "$f" # output new mkv, with only selected audio track

	if [ "$2" = "delete" ]; then
		rm "$f" # remove old file
	else
		mv "$f" "Original $f"
	fi

	mv "temp.$format" "$f" # move new file to old name

    after=`du -m "$f" | cut -f1` # space after
    saved=`expr $before - $after` # saved space 
    total=`expr $total + $saved` # total space saved
    echo "You saved $saved MB! (Total: $total MB)" 
    echo 
done