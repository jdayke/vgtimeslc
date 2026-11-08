# Composite "Who is Jason Duval?" VGTimes + LibertyCity on PC (NVENC)
$ErrorActionPreference = 'Continue'
$root = (Get-Location).Path
$w    = Join-Path $root 'Work\2026 11 05 Jason'
$out  = Join-Path $root 'Renders\2026 11 05'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$T = '25.65'
$vo  = Join-Path $w 'voices\EN_2_Andrew.mp3'
$mus = Join-Path $w 'music\Hitman.wav'
$brands = @(@{b='vg'; n='VGTimes'; logo='Graphics\VG003.png'}, @{b='lc'; n='LibertyCity'; logo='Graphics\LC 002.png'})
Push-Location $w
foreach ($x in $brands) {
  $args = @('-hide_banner','-y','-i','fg.mp4','-i',$vo,'-ss','34.94','-t',$T,'-i',$mus)
  for ($i=0; $i -lt 9; $i++)  { $args += @('-loop','1','-framerate','60','-t',$T,'-i',('png\plate_' + $x.b + '_' + $i.ToString('00') + '.png')) }
  for ($i=0; $i -lt 12; $i++) { $args += @('-loop','1','-framerate','60','-t',$T,'-i',('png\sub_' + $i.ToString('00') + '.png')) }
  $args += @('-loop','1','-framerate','60','-t',$T,'-i',(Join-Path $root $x.logo))
  $args += @('-filter_complex_script',('fc_' + $x.b + '.txt'),'-map','[vout]','-map','[aout]','-t',$T,
             '-c:v','h264_nvenc','-preset','p7','-tune','hq','-rc','vbr','-cq','17','-b:v','0','-profile:v','high','-pix_fmt','yuv420p','-r','60','-g','120',
             '-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',
             (Join-Path $out ('05 11 handoff ' + $x.n + ' Who Is Jason Duval v001.mp4')))
  & ffmpeg @args
  Write-Output ($x.n + ' exit ' + $LASTEXITCODE)
}
Pop-Location
$vg = Join-Path $out '05 11 handoff VGTimes Who Is Jason Duval v001.mp4'
if (Test-Path $vg) { Start-Process explorer.exe -ArgumentList ('/select,"' + $vg + '"') }
