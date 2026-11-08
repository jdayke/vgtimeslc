# Render: GTA 6 Paris takeover (VGTimes + LibertyCity), 31.10.2026
$ErrorActionPreference = 'Continue'
$root   = (Get-Location).Path
$foot   = Join-Path $root 'Footage\2026 10 31'
$work   = Join-Path $root 'Work\2026 10 31 Paris v004'
$outDir = Join-Path $root 'Renders\2026 10 31'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$reel = Join-Path $foot 'Instagram_Fernando_Torres_DfFpLR6MsZl.mp4'
$beat = Join-Path $foot 'youtube_Nikilja_QNfyDI_SOD0.wav'
$start = '4.55'   # first frame with banners visible
$dur   = '26.2'   # to the end of the reel
$logoT = '15.05'  # beat drop = GTA VI logo poster enters frame

$brands = @(
  @{ Name='VGTimes';     Plate=(Join-Path $work 'plate_vg.png'); Logo=(Join-Path $root 'Graphics\VG003.png') },
  @{ Name='LibertyCity'; Plate=(Join-Path $work 'plate_lc.png'); Logo=(Join-Path $root 'Graphics\LC 002.png') }
)

$fail = 0
foreach ($b in $brands) {
  $out = Join-Path $outDir ('31 10 handoff ' + $b.Name + ' GTA 6 Paris v004.mp4')
  $fc = "[0:v]fps=60,scale=1080:1920:flags=lanczos,setsar=1[v];" +
        "[2:v]format=rgba[p];" +
        "[3:v]format=rgba,fade=t=in:st=${logoT}:d=0.5:alpha=1[l];" +
        "[v][p]overlay=0:0:shortest=1[a];" +
        "[a][l]overlay=0:0:shortest=1,format=yuv420p[vout];" +
        "[1:a]atrim=0:${dur},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:st=0:d=0.05,afade=t=out:st=25.7:d=0.5,loudnorm=I=-14:TP=-1.5:LRA=9[aout]"
  & ffmpeg -hide_banner -y `
    -ss $start -t $dur -i $reel `
    -t $dur -i $beat `
    -loop 1 -framerate 60 -t $dur -i $b.Plate `
    -loop 1 -framerate 60 -t $dur -i $b.Logo `
    -filter_complex $fc -map '[vout]' -map '[aout]' -t $dur `
    -c:v h264_nvenc -preset p7 -tune hq -rc vbr -cq 17 -b:v 0 -profile:v high -pix_fmt yuv420p -r 60 -g 120 `
    -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart $out
  if ($LASTEXITCODE -ne 0) { $fail = 1; Write-Output ('FAILED ' + $b.Name) } else { Write-Output ('OK ' + $out) }
}
Get-ChildItem $outDir | Select-Object Name, Length | Format-Table -AutoSize | Out-String | Write-Output
$vg = Join-Path $outDir '31 10 handoff VGTimes GTA 6 Paris v004.mp4'
if (Test-Path $vg) { Start-Process explorer.exe -ArgumentList ('/select,"' + $vg + '"') }
exit $fail
