# Download official GTA VI media kit (video clips + screenshots) from rockstargames.com/VI/media
$ErrorActionPreference = 'Continue'
$dst = Join-Path (Get-Location).Path 'Footage\2026 11 05\rockstar_media'
New-Item -ItemType Directory -Force -Path $dst | Out-Null
$zips = @(
  'https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Videos.zip',
  'https://media-rockstargames-com.akamaized.net/VI/downloads/screenshots/GTAVI_Screenshots.zip'
)
foreach ($u in $zips) {
  $name = Split-Path $u -Leaf
  $zip  = Join-Path $dst $name
  Write-Output ('=== ' + $name)
  & curl.exe -L --fail --retry 3 -s -S -o $zip $u
  if ($LASTEXITCODE -ne 0) { Write-Output ('download failed ' + $name); continue }
  Write-Output ('size MB: ' + [math]::Round((Get-Item $zip).Length / 1MB, 1))
  $out = Join-Path $dst ([IO.Path]::GetFileNameWithoutExtension($name))
  Expand-Archive -Path $zip -DestinationPath $out -Force
  Remove-Item $zip
}
Get-ChildItem $dst -Recurse -File | Select-Object @{n='File';e={$_.FullName.Substring($dst.Length+1)}}, @{n='MB';e={[math]::Round($_.Length/1MB,1)}} | Format-Table -AutoSize | Out-String -Width 300 | Write-Output
