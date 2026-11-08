# Music candidates, Kevin MacLeod (incompetech.com), CC BY 4.0 - credit required
$ErrorActionPreference = 'Continue'
$dst = Join-Path (Get-Location).Path 'Work\2026 11 05 Jason\music'
New-Item -ItemType Directory -Force -Path $dst | Out-Null
$tracks = @('Hitman', 'Cipher', 'Volatile Reaction')
foreach ($t in $tracks) {
  $u = 'https://incompetech.com/music/royalty-free/mp3-royaltyfree/' + [uri]::EscapeDataString($t) + '.mp3'
  $f = Join-Path $dst ($t + '.mp3')
  & curl.exe -L --fail --retry 3 -s -S -o $f $u
  if ($LASTEXITCODE -eq 0 -and (Test-Path $f)) {
    $d = & ffprobe -v error -show_entries format=duration -of csv=p=0 $f
    Write-Output ('OK ' + $t + ' ' + $d + 's')
  } else { Write-Output ('FAILED ' + $t + ' ' + $u) }
}
