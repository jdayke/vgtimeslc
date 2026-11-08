$ErrorActionPreference = 'Continue'
$w = Join-Path (Get-Location).Path 'Work\2026 11 06 Lucia'
$py = 'D:\VGTimes\Shorts\.transcription-venv\Scripts\python.exe'
$out = Join-Path $w 'voices\EN_Ava_lucia_hook_v2.mp3'
for ($i = 1; $i -le 5; $i++) {
  $env:PYTHONPATH = 'D:\VGTimes\Shorts\.tools\edge_tts_latest'
  & $py -m edge_tts --voice 'en-US-AvaNeural' --rate=+7% --text 'GTA 6 second main character just got out of prison.' --write-media $out
  if ((Test-Path $out) -and ((Get-Item $out).Length -gt 1000)) { Write-Output "ok try $i"; break }
  Write-Output "fail try $i"; Start-Sleep -Seconds 5
}
& ffprobe -v error -show_entries format=duration -of csv=p=0 $out
& ffmpeg -hide_banner -i $out -af silencedetect=n=-40dB:d=0.1 -f null - 2>&1 | Select-String silence_
$env:PYTHONPATH = ''
& $py (Join-Path (Get-Location).Path 'Tools\jobs\done\words2.py') $out
