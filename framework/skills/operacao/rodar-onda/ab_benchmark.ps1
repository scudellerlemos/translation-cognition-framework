# Benchmark A x B intercalado: 1 onda por lote, bracos alternados (A, B, A, B...), mesmo teto de falas.
#   A = janela Haiku sem flags | B = janela Haiku + -Esforco low + -PrefixoEstavel.
# Uso (numa janela FORA do Claude Code, como o lancar_lote.ps1): .\framework\skills\operacao\rodar-onda\ab_benchmark.ps1 -PorBraco 4
# Antes de cada onda le a cota (cota_uso.py) e para se a semana passou de -Limite7d. Para na primeira onda que nao fecha.
# Grava logs/ab_plano.jsonl (lote -> braco) para o resumo A x B (ab_resumo.py).
param([int]$PorBraco = 4, [int]$Limite7d = 85, [string]$Projeto = 'projects/utawarerumono_prelude')
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
Set-Location $root
Get-ChildItem Env: | Where-Object { $_.Name -match '^(CLAUDECODE|CLAUDE_CODE_(?!OAUTH)|CLAUDE_PID|CLAUDE_EFFORT|FORCE_PROMPT_CACHING_5M)' } | ForEach-Object { [Environment]::SetEnvironmentVariable($_.Name, $null) }
$logs = Join-Path $PSScriptRoot 'logs'
$plano = Join-Path $logs 'ab_plano.jsonl'
for ($i = 1; $i -le 2 * $PorBraco; $i++) {
    $braco = if ($i % 2 -eq 1) { 'A' } else { 'B' }
    $c = (& python (Join-Path $root 'framework\runtime\cota_uso.py')) -join ' '
    Write-Host "[$braco $i/$(2 * $PorBraco)] cota: $c"
    if ($c -match '7d=(\d+)%' -and [int]$Matches[1] -ge $Limite7d) { Write-Host "Parou: semana em $($Matches[1])% (teto $Limite7d%)."; exit 4 }
    $estado = Get-Content (Join-Path $logs 'estado.json') -Raw | ConvertFrom-Json
    $loteN = [int]$estado.lote + 1
    (@{ lote = $loteN; braco = $braco; ordem = $i } | ConvertTo-Json -Compress) | Add-Content -Encoding utf8 $plano
    $args2 = @{ Lote = 1; Modelo = 'haiku'; Projeto = $Projeto }
    if ($braco -eq 'B') { $args2.Esforco = 'low'; $args2.PrefixoEstavel = $true }
    & (Join-Path $PSScriptRoot 'rodar_ondas.ps1') @args2
    if ($LASTEXITCODE -ne 0) { Write-Host "Parou no lote $loteN (braco $braco): exit=$LASTEXITCODE."; exit $LASTEXITCODE }
}
Write-Host 'Benchmark A x B concluido. Rode: python framework/skills/operacao/rodar-onda/ab_resumo.py'
