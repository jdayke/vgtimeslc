# Composite "Who is Jason Duval?" (VGTimes + LibertyCity): pre-mixed audio + single text track
$ErrorActionPreference = 'Continue'
$root = (Get-Location).Path
$w    = Join-Path $root 'Work\2026 11 05 Jason'
$out  = Join-Path $root 'Renders\2026 11 05'
New-Item -ItemType Directory -Force -Path $out | Out-Null
Get-ChildItem $out -Filter '*v001.mp4' -ErrorAction SilentlyContinue | Remove-Item -Force
$T = '25.65'
$fc = "[0:v]setsar=1,split[f1][f2];" +
      "[f2]scale=2356:1920,crop=1080:1920,gblur=sigma=28,colorchannelmixer=rr=0.42:gg=0.42:bb=0.42[bg];" +
      "[bg][f1]overlay=0:400[b0];[b0][1:v]overlay=0:0[b1];" +
      "[2:v]format=rgba,fade=t=in:st=17.0:d=0.5:alpha=1[lg];[b1][lg]overlay=0:0:shortest=1[b2];" +
      "color=c=white:s=1080x1920:r=30:d=${T},format=rgba,colorchannelmixer=aa=0.55[wh];" +
      "[b2][wh]overlay=0:0:enable='between(t,17.0,17.067)',fps=60,format=yuv420p[vout]"
$brands = @(@{b='vg'; n='VGTimes'; logo='Graphics\VG003.png'}, @{b='lc'; n='LibertyCity'; logo='Graphics\LC 002.png'})
$fail = 0
foreach ($x in $brands) {
  $o = Join-Path $out ('05 11 handoff ' + $x.n + ' Who Is Jason Duval v002.mp4')
  & ffmpeg -hide_banner -loglevel error -y -i (Join-Path $w 'fg.mp4') -i (Join-Path $w ('text_' + $x.b + '.mov')) `
    -loop 1 -framerate 30 -t $T -i (Join-Path $root $x.logo) -i (Join-Path $w 'mix.wav') `
    -filter_complex $fc -map '[vout]' -map '3:a' -t $T `
    -c:v h264_nvenc -preset p7 -tune hq -rc vbr -cq 17 -b:v 0 -profile:v high -pix_fmt yuv420p -r 60 -g 120 `
    -c:a aac -b:a 192k -ar 48000 -movflags +faststart $o
  Write-Output ($x.n + ' exit ' + $LASTEXITCODE)
  if ($LASTEXITCODE -ne 0) { $fail = 1 }
}
$vg = Join-Path $out '05 11 handoff VGTimes Who Is Jason Duval v002.mp4'
if (Test-Path $vg) { Start-Process explorer.exe -ArgumentList ('/select,"' + $vg + '"') }
exit $fail
