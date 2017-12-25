@echo off
for %%f in (*.mkv) do call ffmpeg -i "%%f" -c:a:0 copy "D:\Untranscoded\That 70s Show PAL\AC3\%%~nf.ac3"