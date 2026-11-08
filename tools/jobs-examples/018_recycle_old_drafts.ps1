$ErrorActionPreference = 'Continue'
Add-Type -AssemblyName Microsoft.VisualBasic
foreach ($n in @('LC Who Is Jason Duval','LC Who Is Jason Duval v2','LC Who Is Jason Duval v3')) {
  $p = Join-Path 'J:\CapCut\CapCut Drafts' $n
  if (Test-Path $p) { [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory($p, 'OnlyErrorDialogs', 'SendToRecycleBin'); Write-Output "recycled $n" }
}
