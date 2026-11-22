# Watchdog for the Claude runner: starts runner.ps1, restarts it if it dies or its status file goes stale (hang).
# Errors with timestamps: Tools\jobs\_runner_error.log
$ErrorActionPreference = 'Continue'
$tools  = $PSScriptRoot
$root   = Split-Path -Parent $tools
$jobs   = Join-Path $tools 'jobs'
$status = Join-Path $jobs '_runner_status.txt'
$elog   = Join-Path $jobs '_runner_error.log'
$errf   = Join-Path $jobs '_runner_stderr.tmp'
$stale  = 90
$wm = New-Object System.Threading.Mutex($false, ('Local\ClaudeWatchdog_' + ($root -replace '[^A-Za-z0-9]', '_')))
$own = $false
try { $own = $wm.WaitOne(0) } catch [System.Threading.AbandonedMutexException] { $own = $true }
if (-not $own) { Write-Host 'Watchdog already running for this project - closing.' -ForegroundColor Yellow; Start-Sleep -Seconds 3; exit 0 }
try {
  Add-Type -Namespace W -Name C -MemberDefinition '[DllImport("kernel32.dll")] public static extern System.IntPtr GetStdHandle(int h); [DllImport("kernel32.dll")] public static extern bool GetConsoleMode(System.IntPtr h, out uint m); [DllImport("kernel32.dll")] public static extern bool SetConsoleMode(System.IntPtr h, uint m);'
  $hIn = [W.C]::GetStdHandle(-10); $m = 0
  if ([W.C]::GetConsoleMode($hIn, [ref]$m)) { [W.C]::SetConsoleMode($hIn, (($m -band (-bnot 0x40)) -bor 0x80)) | Out-Null }
} catch { }
function Log($t) { try { Add-Content -Path $elog -Value ((Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ' ' + $t) } catch { } }
function Flush-Err { try { if (Test-Path $errf) { $e = (Get-Content $errf -Raw); if ($e -and $e.Trim()) { Log ('stderr: ' + $e.Trim()) }; Remove-Item $errf -Force } } catch { } }
while ($true) {
  try {
    Log 'start runner'
    $p = Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',('"' + (Join-Path $tools 'runner.ps1') + '"')) -WorkingDirectory $root -NoNewWindow -PassThru -RedirectStandardError $errf
    Start-Sleep -Seconds 15
    while (-not $p.HasExited) {
      Start-Sleep -Seconds 15
      $age = 0
      try { $age = ((Get-Date) - (Get-Item $status -ErrorAction Stop).LastWriteTime).TotalSeconds } catch { $age = 9999 }
      if ($age -gt $stale) {
        Log ('HANG: status not updated for ' + [int]$age + 's - restarting runner')
        & taskkill.exe /T /F /PID $p.Id | Out-Null
        break
      }
    }
    try { if ($p.HasExited) { Log ('runner exited, code ' + $p.ExitCode) } } catch { }
    Flush-Err
  } catch { Log ('watchdog error: ' + $_) }
  Write-Host 'Runner stopped - restarting in 5 s' -ForegroundColor Red
  Start-Sleep -Seconds 5
}
