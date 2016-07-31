@echo off
setlocal enabledelayedexpansion

set version=1.1
title encode_youtube %version% by @djs__ http://lambdan.se
:: Script I use to encode gameplay (usually speedruns) for YouTube
:: Output is originalfilename_output.mp4, in the same folder as original file
:: Requires ffmpeg (either in path or just put ffmpeg.exe next to this .bat)

:: Inspired by https://github.com/donmelton/video_transcoding and anri-chan
:: Encodes follow YouTube Guidelines: https://support.google.com/youtube/answer/1722171?hl=en

set preset=medium
:: ultrafast < superfast < veryfast < faster < fast < medium < slow < slower < veryslow < placebo
:: the faster the encode is, the worse the compression is

:: We need a video to work with
if "%1."=="." goto novid 

echo Input video: "%1"

set trim=n
echo Do you want to trim the video? [ y / (n) ]
set /p trim=">>> "
if /I "%trim%" == "y" (
	echo Use HH:MM:SS
	set /p vidstart=Video start: 
	set /p vidend=Video end: 
	set trimcmd=-async 1 -ss !vidstart! -to !vidend!
) else (
	set trimcmd= 
)

set def=SD
echo Is this video SD (less than 720p) or HD? [ (SD) / HD ]
set /p def=">>> " 
:: For SD we need to ask for aspect ratio, as its probably 720x480 source
if /I "%def%" == "SD" (
	set def=SD
	goto askaspect
) else (
	goto askfps
)

:askaspect
set ar=4:3
echo 4:3 or 16:9 game? [ (4:3) / 16:9 ]
set /p ar=">>> " 
if "%ar%" == "4:3" (
	set width=960
	set aspect=4:3
	goto askfps
) else (
	set width=1280
	set aspect=16:9
	goto askfps
)

:askfps
set framerate=60
echo 30 or 60 fps game? [ 30 / (60) ] 
set /p framerate=">>> "
title Encoding...
if /I "%def%" == "HD" (
	set def=HD
	goto encodehd
) else (
	goto upscaleto720p
)

:encodehd
if %framerate% == 30 (
	ffmpeg -i "%1" %trimcmd% -vf "fps=30" -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf 18 -b:a 384k  "%~n1_output.mp4"
) else ( 
	ffmpeg -i "%1" %trimcmd% -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf 18 -b:a 384k  "%~n1_output.mp4"
)
title Encode Done
pause
exit

:upscaleto720p
if %framerate% == 30 (
	ffmpeg -i "%1" %trimcmd% -c:v libx264 -aspect %aspect% -vf "scale=%width%:720 , fps=30" -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf 18 -b:a 384k "%~n1_output.mp4"
) else (
	ffmpeg -i "%1" %trimcmd% -c:v libx264 -aspect %aspect% -vf scale=%width%:720 -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf 18 -b:a 384k  "%~n1_output.mp4"
)
title Encode Done
pause
exit

:novid
echo You need to drag n drop a video onto this .bat
pause
exit
