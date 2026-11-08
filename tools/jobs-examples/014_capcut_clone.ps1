# Clone user's working CapCut project "VGT" as "LC Who Is Jason Duval B" (content replaced afterwards)
$ErrorActionPreference = 'Continue'
$src = 'J:\CapCut\CapCut Drafts\VGT'
$dst = 'J:\CapCut\CapCut Drafts\LC Who Is Jason Duval B'
if (Test-Path $dst) { Write-Output 'exists'; exit 1 }
& robocopy $src $dst /E /NFL /NDL /NJH /NJS /R:1 /W:1 /XD Resources | Out-Null
Remove-Item (Join-Path $dst 'draft_cover.jpg') -ErrorAction SilentlyContinue
Remove-Item (Join-Path $dst 'Timelines\AD6D6398-17A1-4fdf-8D1D-07825317E530\draft_cover.jpg') -ErrorAction SilentlyContinue
Get-ChildItem $dst -Recurse -File | Select-Object @{n='f';e={$_.FullName.Substring($dst.Length+1)}}, Length | Format-Table -AutoSize | Out-String -Width 200 | Write-Output
exit 0
