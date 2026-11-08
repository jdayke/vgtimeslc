# Voice samples for "Who is Jason Duval?" (EN x3, RU x2) via local edge-tts
$ErrorActionPreference = 'Continue'
$root = (Get-Location).Path
$work = Join-Path $root 'Work\2026 11 05 Jason'
$out  = Join-Path $work 'voices'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$py = 'D:\VGTimes\Shorts\.transcription-venv\Scripts\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }
$env:PYTHONPATH = 'D:\VGTimes\Shorts\.tools\edge_tts_latest'
$en = Join-Path $work 'vo_en.txt'
$ru = Join-Path $work 'vo_ru.txt'
$jobs = @(
  @('EN_1_Christopher', 'en-US-ChristopherNeural', $en, '+0%'),
  @('EN_2_Andrew',      'en-US-AndrewNeural',      $en, '+0%'),
  @('EN_3_Guy',         'en-US-GuyNeural',         $en, '+0%'),
  @('RU_1_Dmitry',      'ru-RU-DmitryNeural',      $ru, '+0%'),
  @('RU_2_AndrewMulti', 'en-US-AndrewMultilingualNeural', $ru, '+0%')
)
foreach ($j in $jobs) {
  $mp3 = Join-Path $out ($j[0] + '.mp3')
  & $py -m edge_tts --voice $j[1] --rate $j[3] --file $j[2] --write-media $mp3
  if (Test-Path $mp3) {
    $d = & ffprobe -v error -show_entries format=duration -of csv=p=0 $mp3
    Write-Output ('OK ' + $j[0] + ' ' + $d + 's')
  } else { Write-Output ('FAILED ' + $j[0]) }
}
Start-Process explorer.exe -ArgumentList ('"' + $out + '"')
