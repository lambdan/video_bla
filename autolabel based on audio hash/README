Compares audio track hashes. Useful if you ripped something and kept the audio unaltered, and now you wanna re-rip again but you don't want to re-identify the video files/episodes. You can hash the audio tracks of the properly labeled episodes, and then use it to find the same hash in the "unorganized" video files/episodes and rename appropriately.
Obviously requires untouched audio ("passthru"). Encoded/altered audio tracks won't have the same hash.

Only ran on Windows 10 with Python 2.7, but you can very easily run it on Linux/macOS. Just make a bash version of extract.bat (loop through all mkv files, and run `ffmpeg -i input.mkv -c:a:0 copy /path/to/output.ext`). The .py scripts should be cross platform already.

How to use:

1. Put extract.bat in the folder that has the properly labeled video files (.mkv), and edit the path in the script to better suit you (also make sure you change the audio extension if necessary). 
Then run the script. This will take a while, extracting the first audio track out of each video. 

2. Put hash.py in the folder with the audio track files (.ac3 etc), and pipe it's output to a text file, i.e. `hash.py > hashes.txt`. This will also take a while.

3. Put rename.py in the folder with the unorganized/unlabeled MKV files, along with the hashes.txt file you got from the 2nd step, and modify the lines at the top of the script to your taste. (Ideally you only need to change shouldrename = False to True)
I recommend running the script first with "shouldrename = False" to make sure it's doing it right. When you trust it, cancel the script, edit "shouldrename = False" to True, and then run again. It will then rename.

Q: Why not just extract audio into .mka container? It takes all formats!
A: True! And I tried! But the hashes weren't the same each time, so it cannot be used.
