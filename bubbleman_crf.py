import subprocess

raw_video = "bubbleman_720p_lossless.avi"
presets = ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow", "placebo"]

for preset in presets:
	crf = 0
	while crf <= 51:
		output = preset + "-crf" + str(crf) + ".mp4"
		subprocess.call(['ffmpeg', '-n', '-i', raw_video, '-preset', preset, '-ac', '1', '-g', '1', '-crf', str(crf), output])
		crf += 1