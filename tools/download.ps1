# Загрузчик оригиналов для шортсов VGTimes / LibertyCity
# Берёт ссылки из links.txt (по одной на строку) и скачивает их в Footage\<сегодняшняя дата>.
# При первом запуске сам ставит yt-dlp через winget, если его нет.

$ErrorActionPreference = 'Stop'
$root    = Split-Path -Parent $PSScriptRoot          # J:\Claude\VGTimes and LibertyCity
$links   = Join-Path $PSScriptRoot 'links.txt'
$outDir  = Join-Path $root ('Footage\' + (Get-Date -Format 'yyyy MM dd'))
$ffmpegDir = 'C:\ffmpeg\bin'

# 1. yt-dlp
$ytdlp = Get-Command yt-dlp -ErrorAction SilentlyContinue
if (-not $ytdlp) {
    Write-Host 'yt-dlp не найден, ставлю через winget...' -ForegroundColor Yellow
    winget install --id yt-dlp.yt-dlp -e --accept-source-agreements --accept-package-agreements
    $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
    $ytdlp = Get-Command yt-dlp -ErrorAction Stop
} else {
    Write-Host 'Обновляю yt-dlp...' -ForegroundColor DarkGray
    try { & yt-dlp -U | Out-Null } catch { }   # если ставился через winget, обновится командой winget upgrade
}

# 2. ffmpeg (нужен для склейки видео+звук и конвертации в wav)
$ffArgs = @()
if (Test-Path (Join-Path $ffmpegDir 'ffmpeg.exe')) { $ffArgs = @('--ffmpeg-location', $ffmpegDir) }
elseif (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host 'ffmpeg не найден, ставлю через winget...' -ForegroundColor Yellow
    winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
}

# 3. Ссылки
if (-not (Test-Path $links)) { throw "Нет файла $links" }
$urls = Get-Content $links | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith('#') }
if (-not $urls) { Write-Host 'В links.txt нет ссылок.'; exit }
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$common = @(
    '--no-playlist', '--restrict-filenames',
    '--write-info-json',                     # метаданные: автор, дата, ссылка — для кредита
    '-o', (Join-Path $outDir '%(extractor)s_%(uploader)s_%(id)s.%(ext)s')
) + $ffArgs

# Если Instagram/TikTok/X просят вход — раскомментируйте строку ниже (браузер, где вы залогинены).
# Firefox работает надёжнее, чем Chrome.
# $common += @('--cookies-from-browser', 'firefox')

$failed = @()
foreach ($u in $urls) {
    Write-Host "`n=== $u" -ForegroundColor Cyan
    try {
        if ($u -match 'music\.youtube|#audio$') {
            # только звук: оригинал + wav для монтажа
            & yt-dlp @common -f 'ba' -x --audio-format wav --keep-video $u.Replace('#audio','')
        } else {
            # лучшее видео + лучший звук, склейка в mp4
            & yt-dlp @common -f 'bv*+ba/b' --merge-output-format mp4 $u
        }
        if ($LASTEXITCODE -ne 0) { $failed += $u }
    } catch { $failed += $u }
}

Write-Host "`nГотово. Папка: $outDir" -ForegroundColor Green
if ($failed) {
    Write-Host 'Не скачались:' -ForegroundColor Red
    $failed | ForEach-Object { Write-Host "  $_" }
    Write-Host 'Для Instagram/TikTok/X обычно помогает --cookies-from-browser (см. комментарий в скрипте).'
}
Invoke-Item $outDir
Read-Host 'Enter — закрыть'
