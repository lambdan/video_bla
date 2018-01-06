_Compares audio track hashes to automatically rename TV Episodes to what you previously named them._

![Script Running](https://raw.githubusercontent.com/lambdan/video_bla/master/autolabel%20based%20on%20audio%20hash/images/ordering.PNG)

Useful if you've previously ripped TV Shows/Episodes with [MakeMKV][makemkv] and properly labeled them, then transcoded the video but kept the audio in the original format/passed it through, removed the MakeMKV originals, and now you want to re-rip them again but don't want to manually identify and rename the episodes again.

[makemkv]: https://www.makemkv.com/

__If you altered the audio in any way this won't work, because the hashes won't be the same:__
- If you made DTS into AC3 or AC3 Stereo in AAC, or anything like that, you cannot use this.
- Even a scratch on your disc can cause the audio to be very slightly altered, thus making it impossible to use this script.
- ...maybe in the future I am smarter and can figure out a way to make it work even if the audio has been altered

## Concept

- Extract the first couple of seconds of audio from the files that are already labeled, into WAV files
- Hash (sha1) those audio files and store the filenames and hashes
- Do the same for the unlabeled files
- Compare hashes, and if they match, rename the unlabeled video to what the renamed video was called, because their audio tracks are identical!

## Requirements

- Python (2.7)
- ffmpeg (accessible from path)

Only ran on Windows 10 with Python 2.7, but you can very easily run it on Linux/macOS. Just make a bash version of extract.bat, or manually do the commands. The .py scripts should be cross platform already.

## How to use

1. Put `extract.bat` in the folder that has the properly labeled video files. Edit the top lines in the script to change output path where the WAV files appear, length of audio to extract (2 worked for me and should be the shortest possible<sup><a href="#2secs">Why?</a></sup>), and which files to match (defaults to all mp4 files `*.mp4`.
Then run the batch script.

2. Put `hash.py` in the folder with the WAV files you just got and run it. If it tells you there are duplicate hashes, you need to go back a step and increase the audio length.

3. Put `rename.py` in the folder with the unorganized/unlabeled MKV files, along with the `hashes.txt` file you got from the 2nd step, and modify the lines at the top of the script to your taste if necessary (if you changed audio length in `extract.py`, you need to change length here as well)

When you run `rename.py` it will ask you if you want to start renaming or just test/dry-run. I recommend testing/dry-running first to see that it's working properly. After that, let it rename.

Tested with my _That '70s Show PAL DVDs_ and it worked perfectly.

<a name="2secs"></a>__Why 2 seconds is shortest length we can use:__ Because sometimes when you extract audio from a video the length won't be exactly the same, it will vary by a few milliseconds depending on interleaves and keyframe intervals etc. If we try to compare hashes on two _seemingly_ identical audio extractions that came from two different video files, the hash will differ because the length is different. However, if we then extract a section of audio from these audio extractions the results are always the same (for some reason), and then we can hash them and get identical values. I guess you can mess around with milliseconds, but whatever. 2 seconds is already very fast, and honestly, even 30 seconds doesn't take long.

## History

2018-01-06
- Literally atleast 1000x faster (just hash a few seconds (2 secs by default) instead of the whole audio track)
- Python scripts much more user friendly
- No need to change audio format/extension (I use WAV now)
- Check and stop for duplicate hashes
- Warn and pause for unmatched videos

2017-12-15	
- Initial Version

---------------------------

![Early test](https://raw.githubusercontent.com/lambdan/video_bla/master/autolabel%20based%20on%20audio%20hash/images/hashes.PNG)
<figcaption>Early test I did that shows the hashes are identical after extracting audio from the audio extractions from the videos</figcaption>