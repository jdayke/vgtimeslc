# Claude job runner v2 for the VGTimes / LibertyCity project folder.
# Jobs (.ps1 / .py) dropped into Tools\jobs\ run one by one, working dir = project folder.
# Log: Tools\jobs\done\<job>.log.  Kill switch: create Tools\jobs\_kill (any content).
# Each job is killed automatically after 20 minutes.
$ErrorActionPreference = 'Continue'
$tools  = $PSScriptRoot
$root   = Split-Path -Parent $tools
$jobs   = Join-Path $tools 'jobs'
$done   = Join-Path $jobs 'done'
$status = Join-Path $jobs '_runner_status.txt'
$kill   = Join-Path $jobs '_kill'
$limit  = 1200
New-Item -ItemType Directory -Force -Path $jobs, $done | Out-Null
$env:Path = 'C:\ffmpeg\bin;' + [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')
$Host.UI.RawUI.WindowTitle = 'Claude runner v2 - ' + $root
Write-Host ('Runner v2 started. Project folder: ' + $root) -ForegroundColor Green
if (Test-Path $kill) { Remove-Item $kill -Force }

while ($true) {
    ('alive v2 ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')) | Set-Content -Encoding UTF8 $status
    $next = Get-ChildItem $jobs -File | Where-Object { $_.Extension -eq '.ps1' -or $_.Extension -eq '.py' } | Sort-Object Name | Select-Object -First 1
    if (-not $next) { if (Test-Path $kill) { Remove-Item $kill -Force }; Start-Sleep -Seconds 2; continue }

    $name = $next.BaseName
    $work = Join-Path $done $next.Name
    $log  = Join-Path $done ($name + '.log')
    $olog = Join-Path $done ($name + '.out.tmp')
    $elog = Join-Path $done ($name + '.err.tmp')
    Move-Item $next.FullName $work -Force
    Write-Host ''
    Write-Host ('>>> ' + $next.Name + '  ' + (Get-Date -Format 'HH:mm:ss')) -ForegroundColor Cyan
    ('running ' + $name + ' ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')) | Set-Content -Encoding UTF8 $status

    if ($work.EndsWith('.py')) { $exe = 'python'; $al = @('"' + $work + '"') }
    else { $exe = 'powershell.exe'; $al = @('-NoProfile','-ExecutionPolicy','Bypass','-File','"' + $work + '"') }
    $start = Get-Date
    $p = Start-Process -FilePath $exe -ArgumentList $al -WorkingDirectory $root -NoNewWindow -PassThru -RedirectStandardOutput $olog -RedirectStandardError $elog
    $reason = ''
    while (-not $p.HasExited) {
        Start-Sleep -Milliseconds 500
        $el = ((Get-Date) - $start).TotalSeconds
        ('running ' + $name + ' ' + [int]$el + 's ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')) | Set-Content -Encoding UTF8 $status
        if (Test-Path $kill) { $reason = 'KILLED by _kill'; Remove-Item $kill -Force }
        elseif ($el -gt $limit) { $reason = 'KILLED by timeout' }
        if ($reason) { & taskkill.exe /T /F /PID $p.Id | Out-Null; break }
    }
    $p.WaitForExit(5000) | Out-Null
    $code = 1
    if (-not $reason) { $code = $p.ExitCode }
    $sec = [int]((Get-Date) - $start).TotalSeconds
    $txt = ''
    if (Test-Path $olog) { $txt += (Get-Content $olog -Raw); Remove-Item $olog }
    if (Test-Path $elog) { $e = Get-Content $elog -Raw; if ($e) { $txt += "`r`n--- stderr (last 4000 chars) ---`r`n" + $e.Substring([math]::Max(0, $e.Length - 4000)) }; Remove-Item $elog }
    $txt += "`r`n" + $reason + "`r`n=== EXIT " + $code + ' | ' + $sec + 's | ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + "`r`n"
    [IO.File]::WriteAllText($log, $txt, (New-Object System.Text.UTF8Encoding($false)))
    if ($code -eq 0) { $c = 'Green' } else { $c = 'Red' }
    Write-Host ('<<< ' + $name + ' exit ' + $code + ', ' + $sec + 's ' + $reason) -ForegroundColor $c
}
