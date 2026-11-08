$ErrorActionPreference = 'Continue'
$w = Join-Path (Get-Location).Path 'Work\2026 11 06 Lucia'
New-Item -ItemType Directory -Force -Path (Join-Path $w 'voices') | Out-Null
$py = 'D:\VGTimes\Shorts\.transcription-venv\Scripts\python.exe'
$env:PYTHONPATH = 'D:\VGTimes\Shorts\.tools\edge_tts_latest'
function Say($args2, $out) {
  for ($i = 1; $i -le 5; $i++) {
    & $py -m edge_tts --voice 'en-US-AvaNeural' @args2 --write-media $out
    if ((Test-Path $out) -and ((Get-Item $out).Length -gt 1000)) { Write-Output "ok $out try $i"; return }
    Write-Output "fail try $i"; Start-Sleep -Seconds 5
  }
}
$main = Join-Path $w 'voices\EN_Ava_lucia.mp3'
$q = Join-Path $w 'voices\EN_Ava_lucia_question.mp3'
Say @('--file', (Join-Path $w 'vo_lucia_en.txt')) $main
Say @('--text', 'Lucia or Jason... who is more dangerous?') $q
foreach ($f in @($main, $q)) {
  Write-Output "=== $f"
  & ffprobe -v error -show_entries format=duration -of csv=p=0 $f
  & ffmpeg -hide_banner -i $f -af silencedetect=n=-40dB:d=0.15 -f null - 2>&1 | Select-String silence_end
}
