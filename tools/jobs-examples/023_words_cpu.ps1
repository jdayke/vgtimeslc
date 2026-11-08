$py = 'D:\VGTimes\Shorts\.transcription-venv\Scripts\python.exe'
& $py -m pip list 2>$null | Select-String -Pattern "whisper|torch|ctranslate"
& $py (Join-Path (Get-Location).Path 'Tools\jobs\done\words.py')
