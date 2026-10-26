# Abre uma janela de PowerShell FORA do Claude Code e roda o rodar_ondas.ps1 nela, sem prender a sessao que chamou.
# Uso (de qualquer shell, inclusive o do Claude Code): .\framework\skills\operacao\rodar-onda\lancar_lote.ps1 -Lote 2
#   Os parametros vao direto para o rodar_ondas.ps1 (-Lote, -Ondas, -MaxFalas, -Teste...). A janela fica aberta no fim.
# A janela filha nao herda as variaveis de sessao do Claude Code nem FORCE_PROMPT_CACHING_5M, e a politica
# de execucao vale so nela (-Scope Process). Este script nao traduz nada: so abre a janela.
# Cuidado: o Start-Process nao protege aspas duplas dentro do -Command (elas somem); o comando usa so aspas simples.
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
$ps1 = Join-Path $PSScriptRoot 'rodar_ondas.ps1'
$cmd = "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; " +
    "Get-ChildItem Env: | Where-Object { `$_.Name -match '^(CLAUDECODE|CLAUDE_CODE_(?!OAUTH)|CLAUDE_PID|CLAUDE_EFFORT|FORCE_PROMPT_CACHING_5M)' } | ForEach-Object { [Environment]::SetEnvironmentVariable(`$_.Name, `$null) }; " +
    "Set-Location '$root'; & '$ps1' $($Args -join ' ')"
Start-Process powershell -ArgumentList '-NoExit', '-NoProfile', '-Command', $cmd
Write-Host "Janela aberta: rodar_ondas.ps1 $($Args -join ' '). Acompanhe por ela; nao use o Claude Code ate o fim."
