$ErrorActionPreference = 'Stop'

$audit = 'F:\OpenScience\audits\bio-atac-seq-allele-specific-accessibility\reaudit-opt10-20260928'
$candidate = 'F:\OpenScience\wt\opt10-atac-asa\skills\bio-atac-seq-allele-specific-accessibility'
$worktree = 'F:\OpenScience\wt\opt10-atac-asa'
$provider = 'F:\optimizing-agent-science-skills\external\GPTomics__bioSkills'
$providerCommit = 'd91ed3d563019e649dc854c56ccd62551359488a'
$expectedCandidate = '4310ddfa1d9ed178f033ad42e77e0772ddadd3c4905dd1e9bcef8b6289a24103'
$expectedBlobs = [ordered]@{
    'atac-seq/allele-specific-accessibility/SKILL.md' = 'e0941c7bde0a2e4540e6f1b962575bfcfa77254a'
    'atac-seq/allele-specific-accessibility/usage-guide.md' = 'f3e7ccbebed3654a2efa24b5a62b58e43719c0cc'
    'atac-seq/allele-specific-accessibility/examples/wasp_ase_pipeline.sh' = 'e8920f67859dede6e3f9b49793047a7a153e91da'
}

$files = @(Get-ChildItem -LiteralPath $candidate -Recurse -File)
$records = [string[]]@(foreach ($file in $files) {
    $relative = $file.FullName.Substring($candidate.Length + 1).Replace('\', '/')
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash.ToLowerInvariant()
    "$relative`t$($file.Length)`t$hash"
})
[Array]::Sort($records, [StringComparer]::Ordinal)
$manifest = [string]::Join("`n", $records)
$manifestBytes = [Text.Encoding]::UTF8.GetBytes($manifest)
$sha = [Security.Cryptography.SHA256]::HashData($manifestBytes)
$candidateHash = [Convert]::ToHexString($sha).ToLowerInvariant()
if ($candidateHash -ne $expectedCandidate) { throw "candidate identity mismatch: $candidateHash" }

$head = (git -C $provider rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $head -ne $providerCommit) { throw 'provider commit mismatch' }
if (@(git -C $provider status --porcelain).Count -ne 0) { throw 'provider checkout is dirty' }
foreach ($item in $expectedBlobs.GetEnumerator()) {
    $actual = (git -C $provider rev-parse "$providerCommit`:$($item.Key)").Trim()
    if ($LASTEXITCODE -ne 0 -or $actual -ne $item.Value) { throw "provider blob mismatch: $($item.Key)" }
}

$skill = Get-Content -Raw -LiteralPath (Join-Path $candidate 'SKILL.md')
$methods = Get-Content -Raw -LiteralPath (Join-Path $candidate 'references\method-selection-and-failures.md')
$provenance = Get-Content -Raw -LiteralPath (Join-Path $candidate 'references\provenance.md')
$combined = $skill + $methods
foreach ($forbidden in @('1.5-3x', 'above 70%', 'p < 1e-5')) {
    if ($combined.Contains($forbidden)) { throw "unsupported fixed claim remains: $forbidden" }
}
foreach ($required in @('method-selection routes only', 'no executable QuASAR', 'no executable MatrixEQTL', 'study-specific FDR or permutation')) {
    if (-not $combined.Contains($required)) { throw "required bounded claim missing: $required" }
}
foreach ($blob in $expectedBlobs.Values) {
    if (-not $provenance.Contains($blob)) { throw "candidate provenance omits blob: $blob" }
}
if (-not $provenance.Contains('may reflect its newline normalization')) { throw 'newline-normalization caveat missing' }

$status = @(git -C $worktree status --short)
$lines = @(
    "run_utc=$([DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ'))"
    "candidate_sha256=$candidateHash"
    "candidate_file_count=$($files.Count)"
    "candidate_manifest_bytes=$($manifestBytes.Length)"
    "worktree_head=$((git -C $worktree rev-parse HEAD).Trim())"
    "worktree_status=$([string]::Join(';', $status))"
    "provider_commit=$head"
)
foreach ($item in $expectedBlobs.GetEnumerator()) { $lines += "provider_blob_$($item.Key)=$($item.Value)" }
$lines += @(
    'provider_checkout_clean=PASS'
    'canonical_blob_identity=PASS'
    'candidate_content_identity=PASS'
    'unsupported_fixed_claims_absent=PASS'
    'matrixeqtl_quasar_external_only=PASS'
    'study_specific_multiplicity_language=PASS'
    'checkout_hash_normalization_caveat=PASS'
)
New-Item -ItemType Directory -Force -Path (Join-Path $audit 'evidence') | Out-Null
[IO.File]::WriteAllLines((Join-Path $audit 'evidence\static.txt'), $lines)
$lines
