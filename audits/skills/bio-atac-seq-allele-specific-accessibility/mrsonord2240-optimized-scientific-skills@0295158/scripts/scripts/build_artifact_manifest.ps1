$ErrorActionPreference = 'Stop'
$root = 'F:\OpenScience\audits\bio-atac-seq-allele-specific-accessibility\reaudit2-opt10-20260928'
$relativePaths = @(
    'report.json',
    'viewer.md',
    'source-identity.json',
    'candidate-manifest.json',
    'finding-ledger.md',
    'scientific-source-notes.md',
    'inputs.json',
    'inputs/rasqual-two-features.tsv',
    'inputs/rasqual-zero-feature.tsv',
    'scripts/run_static_reaudit2.ps1',
    'scripts/run_fixture_reaudit2.sh',
    'scripts/run_real_pipeline_reaudit2.sh',
    'scripts/run_real_rasqual_reaudit2.sh',
    'scripts/build_artifact_manifest.ps1',
    'validate_report.py',
    'evidence/schema-validation.json',
    'evidence/static.txt',
    'evidence/fixtures.txt',
    'evidence/real-pipeline.txt',
    'evidence/real-rasqual.txt',
    'evidence/structural-precheck.json'
)
$artifacts = foreach ($relative in $relativePaths) {
    $path = Join-Path $root $relative
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "missing artifact: $relative" }
    $item = Get-Item -LiteralPath $path
    [ordered]@{
        path = $relative.Replace('\', '/')
        bytes = $item.Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLowerInvariant()
    }
}
$manifest = [ordered]@{
    skill = 'bio-atac-seq-allele-specific-accessibility'
    phase = 'second-independent-reaudit'
    candidate_sha256 = '275ff0a1b8d9bed7a80e8316f97fe421296cb081c837ed01aaa53a0f96e48ae2'
    artifacts = @($artifacts)
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -Encoding utf8 -LiteralPath (Join-Path $root 'artifact-manifest.json')
