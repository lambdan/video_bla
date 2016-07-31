@echo off

if "%1."=="." goto novid

echo Input video: %1

set def=SD
echo Is this video SD (less than 720p) or HD? [ (SD) / HD ]
set /p def=">>> " 

if "%def%" == "SD" (
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
if "%def%" == "HD" (
	goto encodehd
) else (
	goto upscaleto720p
)

:encodehd
if %framerate% == "30" (
	ffmpeg -i %1 -vf "fps=30" -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset medium -crf 1 -x264opts vbv-maxrate=8000:vbv-bufsize=4000:keyint=600:min-keyint=60:crf-max=25:qpmax=34 %1output.mp4
) else ( 
	ffmpeg -i %1 -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset medium -crf 1 -x264opts vbv-maxrate=12000:vbv-bufsize=6000:keyint=600:min-keyint=60:crf-max=25:qpmax=34 %1output.mp4
)
exit

:upscaleto720p
if %framerate% == "30" (
	ffmpeg -i %1 -c:v libx264 -aspect %aspect% -vf "scale=%width%:720,fps=30" -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset medium -crf 1 -x264opts vbv-maxrate=5000:vbv-bufsize=2500:keyint=600:min-keyint=60:crf-max=25:qpmax=34 %1output.mp4
) else (
	ffmpeg -i %1 -c:v libx264 -aspect %aspect% -vf scale=%width%:720 -bf 2 -pix_fmt yuv420p -vprofile high -level 4.1 -preset medium -crf 1 -x264opts vbv-maxrate=7500:vbv-bufsize=3750:keyint=600:min-keyint=60:crf-max=25:qpmax=34 %1output.mp4
)
exit

:novid
echo You need to drag n drop a video onto this .bat
pause
exit