$ErrorActionPreference = 'Continue'
$w = Join-Path (Get-Location).Path 'Work\2026 11 05 Jason'
$py = 'D:\VGTimes\Shorts\.transcription-venv\Scripts\python.exe'
$env:PYTHONPATH = 'D:\VGTimes\Shorts\.tools\edge_tts_latest'
$out = Join-Path $w 'voices\EN_2_Andrew_question.mp3'
for ($i = 1; $i -le 5; $i++) {
  & $py -m edge_tts --voice 'en-US-AndrewNeural' --text 'Jason or Lucia... who is really in charge?' --write-media $out
  if ((Test-Path $out) -and ((Get-Item $out).Length -gt 1000)) { Write-Output "ok try $i"; break }
  Write-Output "fail try $i"; Start-Sleep -Seconds 5
}
& ffprobe -v error -show_entries format=duration -of csv=p=0 $out
& ffmpeg -hide_banner -i $out -af silencedetect=n=-40dB:d=0.15 -f null - 2>&1 | Select-String silence
