$ErrorActionPreference = 'Continue'
$root = (Get-Location).Path
$w = Join-Path $root 'Work\2026 11 05 Jason'
$py = 'D:\VGTimes\Shorts\.transcription-venv\Scripts\python.exe'
$env:PYTHONPATH = 'D:\VGTimes\Shorts\.tools\edge_tts_latest'
$out = Join-Path $w 'voices\EN_2_Andrew_v2.mp3'
& $py -m edge_tts --voice 'en-US-AndrewNeural' --file (Join-Path $w 'vo_en_v2.txt') --write-media $out
& ffprobe -v error -show_entries format=duration -of csv=p=0 $out
$b = 'J:\CapCut\CapCut Drafts\LC Who Is Jason Duval B'
if (Test-Path $b) {
  Add-Type -AssemblyName Microsoft.VisualBasic
  [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($b, 'OnlyErrorDialogs', 'SendToRecycleBin')
  Write-Output 'B recycled'
}
