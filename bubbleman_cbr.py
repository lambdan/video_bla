import subprocess

raw_video = "bubbleman_720p_lossless.avi"
presets = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]

for preset in presets:
	bitrate = 100
	while bitrate <= 5000:
		bitratek = str(bitrate) + "k"
		output = preset + "-" + bitratek + ".mp4"
		subprocess.call(['ffmpeg', '-n', '-i', raw_video, '-preset', preset, '-ac', '1', '-g', '1', '-b:v', bitratek, '-minrate', bitratek, '-maxrate', bitratek, '-bufsize', bitratek, output])
		bitrate += 100