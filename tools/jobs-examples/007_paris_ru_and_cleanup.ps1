# 1) Old versions v001-v003 -> Recycle Bin (recoverable)
# 2) Render LibertyCity RU v004
$ErrorActionPreference = 'Continue'
$root   = (Get-Location).Path
$outDir = Join-Path $root 'Renders\2026 10 31'
Add-Type -AssemblyName Microsoft.VisualBasic
Get-ChildItem $outDir -File | Where-Object { $_.Name -match ' v00[123]\.mp4$' } | ForEach-Object {
  [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($_.FullName, 'OnlyErrorDialogs', 'SendToRecycleBin')
  Write-Output ('recycled ' + $_.Name)
}

$foot  = Join-Path $root 'Footage\2026 10 31'
$reel  = Join-Path $foot 'Instagram_Fernando_Torres_DfFpLR6MsZl.mp4'
$beat  = Join-Path $foot 'youtube_Nikilja_QNfyDI_SOD0.wav'
$plate = Join-Path $root 'Work\2026 10 31 Paris v004\plate_lc_ru.png'
$logo  = Join-Path $root 'Graphics\LC 002.png'
$out   = Join-Path $outDir '31 10 handoff LibertyCity RU GTA 6 Paris v004.mp4'
$start = '4.55'; $dur = '26.2'; $logoT = '15.05'

$fc = "[0:v]fps=60,scale=1080:1920:flags=lanczos,setsar=1[v];" +
      "[2:v]format=rgba[p];" +
      "[3:v]format=rgba,fade=t=in:st=${logoT}:d=0.5:alpha=1[l];" +
      "[v][p]overlay=0:0:shortest=1[a];" +
      "[a][l]overlay=0:0:shortest=1,format=yuv420p[vout];" +
      "[1:a]atrim=0:${dur},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:st=0:d=0.05,afade=t=out:st=25.7:d=0.5,loudnorm=I=-14:TP=-1.5:LRA=9[aout]"
& ffmpeg -hide_banner -y `
  -ss $start -t $dur -i $reel `
  -t $dur -i $beat `
  -loop 1 -framerate 60 -t $dur -i $plate `
  -loop 1 -framerate 60 -t $dur -i $logo `
  -filter_complex $fc -map '[vout]' -map '[aout]' -t $dur `
  -c:v h264_nvenc -preset p7 -tune hq -rc vbr -cq 17 -b:v 0 -profile:v high -pix_fmt yuv420p -r 60 -g 120 `
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart $out
$code = $LASTEXITCODE
Get-ChildItem $outDir | Select-Object Name, Length | Format-Table -AutoSize | Out-String | Write-Output
if (Test-Path $out) { Start-Process explorer.exe -ArgumentList ('/select,"' + $out + '"') }
exit $code
