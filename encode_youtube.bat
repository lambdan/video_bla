:: http://lambdan.se/130/encode_youtube
@echo off
setlocal enabledelayedexpansion

set version=1.1.1
title encode_youtube %version% by @djs__ http://lambdan.se

set preset=medium
:: ultrafast < superfast < veryfast < faster < fast < medium < slow < slower < veryslow < placebo
:: the faster the encode is, the worse the compression is
set crf=18
:: Ranges from 0 (lossless) to 51 (worst). 18-28 is a "subjectively sane range". 
:: "Consider 18 to be visually lossless or nearly so" -https://trac.ffmpeg.org/wiki/Encode/H.264

:: Full path input and output and escape spaces yadda yadda
set input="%~f1"
set output="%~d1%~p1%~n1_output.mp4"

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
	ffmpeg -i %input% %trimcmd% -vf "fps=30" -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf %crf% -b:a 384k %output%
) else ( 
	ffmpeg -i %input%  %trimcmd% -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf %crf% -b:a 384k %output%
)
title Encode Done
pause
exit

:upscaleto720p
if %framerate% == 30 (
	ffmpeg -i %input%  %trimcmd% -c:v libx264 -aspect %aspect% -vf "scale=%width%:720 , fps=30" -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf %crf% -b:a 384k %output%
) else (
	ffmpeg -i %input%  %trimcmd% -c:v libx264 -aspect %aspect% -vf scale=%width%:720 -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset %preset% -crf %crf% -b:a 384k %output%
)
title Encode Done
pause
exit

:novid
echo You need to drag n drop a video onto this .bat
pause
exit
