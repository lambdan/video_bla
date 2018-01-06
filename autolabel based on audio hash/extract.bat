@echo off
set outputfolder=D:\Extracts\
set /a length=2
set match="*.mp4"

md "%outputfolder%"

for %%f in (%match%) do call echo Extracting %length% secs of audio from "%%f" into "%outputfolder%" && ffmpeg -i "%%f" -t %length% -loglevel error "%outputfolder%%%~nf.wav"

cd /d "%outputfolder%"
set /a "sniplength=%length%-1"

for %%f in (*.wav) do call echo Trimming 1 sec of audio from "%%f" && ffmpeg -i "%%f" -t %sniplength% -c:a copy -loglevel error temp.wav && del "%%f" && move temp.wav "%%f"