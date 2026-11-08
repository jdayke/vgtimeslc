$py = 'D:\VGTimes\Shorts\.transcription-venv\Scripts\python.exe'
$env:HF_HUB_DISABLE_SYMLINKS_WARNING = '1'
& $py (Join-Path (Get-Location).Path 'Tools\jobs\done\words_ru.py') (Join-Path (Get-Location).Path 'Work\2026 11 05 Jason\voices\RU_team_take1.wav')
