# Kevin MacLeod tracks (CC BY 4.0) via YouTube - incompetech.com is unreachable from this PC
$ErrorActionPreference = 'Continue'
$dst = Join-Path (Get-Location).Path 'Work\2026 11 05 Jason\music'
New-Item -ItemType Directory -Force -Path $dst | Out-Null
$q = @(
  @('Hitman', 'https://www.youtube.com/watch?v=zvPYgXf79LY'),
  @('Cipher', 'ytsearch1:Kevin MacLeod Cipher'),
  @('Volatile_Reaction', 'ytsearch1:Kevin MacLeod Volatile Reaction')
)
foreach ($t in $q) {
  & yt-dlp --no-playlist -f 'ba' -x --audio-format wav --ffmpeg-location 'C:\ffmpeg\bin' --print-to-file '%(title)s | %(uploader)s | %(webpage_url)s | %(duration)s' (Join-Path $dst ($t[0] + '.source.txt')) -o (Join-Path $dst ($t[0] + '.%(ext)s')) $t[1]
  if (Test-Path (Join-Path $dst ($t[0] + '.wav'))) { Write-Output ('OK ' + $t[0] + ' :: ' + (Get-Content (Join-Path $dst ($t[0] + '.source.txt')))) } else { Write-Output ('FAILED ' + $t[0]) }
}
