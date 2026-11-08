$ErrorActionPreference = 'Continue'
$root = (Get-Location).Path
$out  = Join-Path $root 'Footage\2026 10 31'
New-Item -ItemType Directory -Force -Path $out | Out-Null

if (-not (Get-Command yt-dlp -ErrorAction SilentlyContinue)) {
    Write-Output 'yt-dlp not found -> winget install'
    winget install --id yt-dlp.yt-dlp -e --accept-source-agreements --accept-package-agreements --disable-interactivity
    $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User') + ';C:\ffmpeg\bin'
}
Write-Output ('yt-dlp: ' + (& yt-dlp --version))
Write-Output ('ffmpeg: ' + ((& ffmpeg -version | Select-Object -First 1)))

$common = @('--no-playlist','--restrict-filenames','--write-info-json','--ffmpeg-location','C:\ffmpeg\bin',
            '-o', (Join-Path $out '%(extractor)s_%(uploader)s_%(id)s.%(ext)s'))

Write-Output "`n=== Instagram reel"
& yt-dlp @common -f 'bv*+ba/b' --merge-output-format mp4 'https://www.instagram.com/reels/DfFpLR6MsZl/'
$ig = $LASTEXITCODE

Write-Output "`n=== YouTube track (audio)"
& yt-dlp @common -f 'ba' -x --audio-format wav --keep-video 'https://www.youtube.com/watch?v=QNfyDI_SOD0'
$yt = $LASTEXITCODE

Write-Output "`nIG exit=$ig YT exit=$yt"
Get-ChildItem $out | Select-Object Name, Length | Format-Table -AutoSize | Out-String | Write-Output
if ($ig -ne 0 -or $yt -ne 0) { exit 1 }
