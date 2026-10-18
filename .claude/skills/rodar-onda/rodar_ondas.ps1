# Roda ondas em sequencia, uma sessao nova do `claude -p` por onda. Para na primeira PARADA/FIM/erro.
# Uso: .\.claude\skills\rodar-onda\rodar_ondas.ps1 -Lote 8   (ou -Ondas N; retoma da proxima onda gravada em logs/estado.json)
#   -TesteAgente : igual, mas lanca um scene-translator que so escreve em scratch/ e roda python com UTAP_DATA_DIR (checa as permissoes do subagente).
#   -Teste : so confere permissoes headless (roda panorama.py e responde PARADA: teste); nao traduz nada.
param(
    [int]$Ondas = 1,
    [int]$Lote = 0,
    [int]$MaxFalas = 380,
    [string]$Projeto = 'projects/utawarerumono_prelude',
    [int]$OndaInicial = 1,
    [switch]$Teste,
    [switch]$TesteAgente
)
$ErrorActionPreference = 'Stop'
if ($Lote -gt 0) { $Ondas = $Lote }
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $root
$logs = Join-Path $PSScriptRoot 'logs'
New-Item -ItemType Directory -Force $logs | Out-Null
$parada = @((Join-Path $root 'scratch\PARADA.md'), (Join-Path $root "$Projeto\scratch\PARADA.md"))
$parada | Remove-Item -ErrorAction SilentlyContinue
# Estado: proxima onda e numero do lote. -OndaInicial explicito vence; sem estado, vale o padrao (1).
$estadoF = Join-Path $logs 'estado.json'
$estado = if (Test-Path $estadoF) { Get-Content $estadoF -Raw | ConvertFrom-Json } else { $null }
if ($estado -and -not $PSBoundParameters.ContainsKey('OndaInicial')) { $OndaInicial = [int]$estado.proxima_onda }
$loteN = if ($estado) { [int]$estado.lote + 1 } else { 1 }
$t0 = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$logsLote = @()

# Trava: uma execucao por vez (duas escrevendo nas mesmas cenas corrompem o estado). Sessao interativa aberta traduzindo cenas: nao rode.
$lock = Join-Path $logs '.lock'
if (Test-Path $lock) {
    $old = [int](Get-Content $lock -ErrorAction SilentlyContinue)
    if ($old -and (Get-Process -Id $old -ErrorAction SilentlyContinue)) { Write-Host "Ja ha uma execucao (PID $old). Parou."; exit 4 }
}
$PID | Out-File $lock
try {

$allow = 'Bash(python:*),Bash(UTAP_DATA_DIR=*),Read,Write,Edit,Glob,Grep,Agent,Skill'
$deny  = 'Bash(git add:*),Bash(git commit:*),Bash(git push:*),Bash(git reset:*),Bash(git checkout:*)'

for ($i = 0; $i -lt $Ondas; $i++) {
    $n = $OndaInicial + $i
    if ($TesteAgente) {
        $prompt = "Teste de permissoes de subagente, sem traduzir nada. Lance UM subagente scene-translator com esta tarefa unica: (1) escrever o arquivo scratch/TESTE/ok.txt com o texto ok usando Write; (2) editar esse arquivo trocando ok por feito usando Edit; (3) rodar no Bash o comando UTAP_DATA_DIR=x python -c 'print(1)' (variavel de ambiente antes do python); (4) relatar em uma linha o que passou e o que foi negado. Nao rode run_scene nem wave. Depois responda com uma unica linha final: PARADA: teste-agente <resultado>"
    } elseif ($Teste) {
        $prompt = "Teste de permissoes. Rode apenas: python .claude/skills/panorama-ondas/panorama.py $Projeto (um unico argumento, sem ponto final no comando). Depois responda com uma unica linha final: PARADA: teste"
    } else {
        $prompt = @"
Rode a skill rodar-onda em MODO CONTINUO para $Projeto. Esta e a onda numero $n.
Aval permanente do usuario (Felipe): propor cenas na ordem do panorama.py, ate $MaxFalas falas, sem esperar o sim do passo 1.
Siga o processo a risca, sem flag de bypass e sem contornar gate. Escalonamento do tradutor e lore sem forma: a onda termina,
o wave.py acusa o gate e voce PARA com a tabela em scratch/PARADA.md (pasta .claude e protegida); lore com 3 ou mais ocorrencias,
glossary_lint nao corrigido e gate aberto tambem param. Fala high sem retrotradução: passo 5c da skill (subagente Opus), sem parar.
Subagente: comando unico no formato UTAP_DATA_DIR=<raiz>/projects/<nome>/backup_original/DataBase2.sdat python framework/runtime/wave.py projects/<nome> <cena> --backend in-session, sem export, sem cd, sem pipe (outro formato e negado em modo sem supervisao). Rode o levantar-melhorias apenas se $n for multiplo de 3.
Termine com uma unica linha final: ONDA_OK: <n cenas>, <x falas> | PARADA: <motivo> | FIM
"@
    }
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $log = Join-Path $logs "onda_${n}_$stamp.log"
    Write-Host "== onda $n ($stamp) -> $log"
    $tent = 0
    while ($true) {
        $out = $prompt | & claude -p --no-chrome --model sonnet --permission-mode acceptEdits `
            --allowedTools $allow --disallowedTools $deny 2>&1
        $code = $LASTEXITCODE
        # Limite de sessao da assinatura: espera o horario de liberacao (+2 min) e refaz a mesma onda (estado vem do disco).
        $m = [regex]::Match(($out -join "`n"), 'hit your session limit.*?resets (\d{1,2})(?::(\d{2}))?\s*(am|pm)')
        if (-not $m.Success -or $tent -ge 3) { break }
        $h = [int]$m.Groups[1].Value % 12; if ($m.Groups[3].Value -eq 'pm') { $h += 12 }
        $alvo = (Get-Date).Date.AddHours($h).AddMinutes([int]('0' + $m.Groups[2].Value))
        if ($alvo -lt (Get-Date)) { $alvo = $alvo.AddDays(1) }
        $alvo = $alvo.AddMinutes(2); $tent++
        Write-Host "   limite de sessao: espero ate $alvo e refaco a onda $n"
        Start-Sleep -Seconds ([int][Math]::Max(1, ($alvo - (Get-Date)).TotalSeconds))
    }
    $out | Out-File -Encoding utf8 $log
    $logsLote += $log
    $last = ($out | Where-Object { $_ -match '\S' } | Select-Object -Last 1)
    Write-Host "   exit=$code | $last"
    if ($code -ne 0) { Write-Host 'Parou: claude saiu com erro.'; exit 1 }
    if ($last -match '^\s*PARADA') {
        Write-Host "Parou: $last"
        foreach ($pf in $parada) { if (Test-Path $pf) { Write-Host "--- $pf ---"; Get-Content $pf } }
        exit 2
    }
    if ($last -match '^\s*FIM')    { Write-Host 'Fim: nenhuma cena restante.'; exit 0 }
    if ($last -notmatch '^\s*ONDA_OK') { Write-Host 'Parou: ultima linha fora do contrato (ONDA_OK/PARADA/FIM).'; exit 3 }
    @{ proxima_onda = $n + 1; lote = $loteN } | ConvertTo-Json | Out-File -Encoding utf8 $estadoF
}
} finally {
    Remove-Item $lock -ErrorAction SilentlyContinue
    # Resumo do lote (so le o ledger e o run_state); roda em qualquer saida, inclusive PARADA.
    if ($logsLote.Count -gt 0) { & python (Join-Path $PSScriptRoot 'resumo_lote.py') $Projeto $t0 $loteN @logsLote }
}
