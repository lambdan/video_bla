:: http://lambdan.se/130/encode_youtube
@echo off
setlocal enabledelayedexpansion

set preset=medium
set crf=20
set AudioBitrate=128
:: ultrafast < superfast < veryfast < faster < fast < medium < slow < slower < veryslow < placebo
:: the faster the encode is, the worse the compression is

:: crf ranges from 0 (lossless) to 51 (worst). 18-28 is a "subjectively sane range". 
:: "Consider 18 to be visually lossless or nearly so" -https://trac.ffmpeg.org/wiki/Encode/H.264

:: audio bitrate is in k

set version=1.1.2
title encode_youtube %version% by @djs__ http://lambdan.se - preset=%preset%, crf=%crf%, audio bitrate=%AudioBitrate%k

:: Full path input and output and escape spaces yadda yadda
set input="%~f1"
set output="%~d1%~p1%~n1_output_crf%crf%_%preset%_%AudioBitrate%k.mp4"

:: Check if we got a video to work with
if [%1] == [] goto novid 

echo Input video: %input%
::echo Output video: %output%

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
	ffmpeg -i %input% %trimcmd% -movflags faststart -vf "fps=30" -flags +cgop -x264opts keyint=15:no-scenecut=1 -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf %crf% -codec:a aac -strict -2 -b:a %AudioBitrate%k -r:a 48000 %output%
) else ( 
	ffmpeg -i %input%  %trimcmd% -movflags faststart -flags +cgop -x264opts keyint=30:no-scenecut=1 -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf %crf% -codec:a aac -strict -2 -b:a %AudioBitrate%k -r:a 48000 %output%
)
title Encode Done
pause
exit

:upscaleto720p
if %framerate% == 30 (
	ffmpeg -i %input%  %trimcmd% -movflags faststart -c:v libx264 -flags +cgop -aspect %aspect% -vf "scale=%width%:720 , fps=30" -x264opts keyint=15:no-scenecut=1 -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf %crf% -codec:a aac -strict -2 -b:a %AudioBitrate%k -r:a 48000 %output%
) else (
	ffmpeg -i %input%  %trimcmd% -movflags faststart -c:v libx264 -flags +cgop -aspect %aspect% -vf scale=%width%:720 -x264opts keyint=30:no-scenecut=1 -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf %crf% -codec:a aac -strict -2 -b:a %AudioBitrate%k -r:a 48000 %output%
)
title Encode Done
pause
exit

:novid
echo You need to drag n drop a video onto this .bat
pause
exit
