$ErrorActionPreference = 'Stop'
$auditRoot = 'F:\OpenScience\audits\bio-clip-seq-ago-clip-mirna-targets\reaudit3-opt10-20260928'
$hashFile = Join-Path $auditRoot 'artifact-hashes.sha256'
$entries = Get-ChildItem -LiteralPath $auditRoot -Recurse -File |
    Where-Object { $_.FullName -ne $hashFile } |
    Sort-Object { $_.FullName.Substring($auditRoot.Length + 1) }
$lines = foreach ($entry in $entries) {
    $relative = $entry.FullName.Substring($auditRoot.Length + 1).Replace('\', '/')
    $digest = (Get-FileHash -LiteralPath $entry.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "$digest  $relative"
}
[System.IO.File]::WriteAllLines($hashFile, $lines, [System.Text.UTF8Encoding]::new($false))
