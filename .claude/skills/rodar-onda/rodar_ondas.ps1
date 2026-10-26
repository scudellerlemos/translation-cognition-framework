# Roda ondas em sequencia, uma sessao nova do `claude -p` por onda. Para na primeira PARADA/FIM/erro.
# Uso: .\.claude\skills\rodar-onda\rodar_ondas.ps1 -Lote 8   (ou -Ondas N; retoma da proxima onda gravada em logs/estado.json)
#   O limite de cota (sessao ou semana) e esperado e a onda refeita sozinha: framework/runtime/espera_reset.py.
#   -TesteAgente : igual, mas lanca um scene-translator que so escreve em scratch/ e roda python com UTAP_DATA_DIR (checa as permissoes do subagente).
#   -Modelo sonnet|haiku|opus : modelo da janela da onda (padrao haiku, decisao do usuario de 2026-10-21 apos o benchmark A x B). No fim, conformidade_onda.py confere o lote.
#   -Esforco low|medium|high|xhigh|max, -PrefixoEstavel : flags do claude -p da janela (opcionais, padrao desligados: so atuam na janela, que custa ~US$ 0,03 por onda; ganho possivel < 3% do custo da onda, benchmark A x B de 2026-10-21).
#   -Teste : so confere permissoes headless (roda panorama.py e responde PARADA: teste); nao traduz nada, nao grava log de onda nem resumo de lote.
#   No inicio imprime a estimativa de tempo do lote (estimar_lote.py) e, durante a onda e a espera de cota, um batimento a cada 3/5 min.
#   Para abrir numa janela fora do Claude Code: lancar_lote.ps1.
param(
    [int]$Ondas = 1,
    [int]$Lote = 0,
    [int]$MaxFalas = 380,
    [string]$Projeto = 'projects/utawarerumono_prelude',
    [int]$OndaInicial = 1,
    [switch]$Teste,
    [switch]$TesteAgente,
    [switch]$Lore,
    [ValidateSet('sonnet', 'haiku', 'opus')][string]$Modelo = 'haiku',   # modelo da JANELA da onda (padrao haiku desde 2026-10-21, benchmark A x B); subagentes seguem o proprio arquivo
    [string]$Cenas = '',
    [ValidateSet('', 'low', 'medium', 'high', 'xhigh', 'max')][string]$Esforco = '',   # --effort da janela (vazio = padrao do claude)
    [switch]$PrefixoEstavel   # --exclude-dynamic-system-prompt-sections: cwd/env/memoria/git status saem do prompt do sistema (cache entre ondas)
)
$ErrorActionPreference = 'Stop'
if ($Lote -gt 0) { $Ondas = $Lote }
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $root
$logs = Join-Path $PSScriptRoot 'logs'
New-Item -ItemType Directory -Force $logs | Out-Null
if ($Lore) {
    # Levantamento de lore antes do lote: kb_phase onda das proximas $Ondas ondas do panorama.py, numa tabela so.
    $pan = & python (Join-Path $root '.claude\skills\panorama-ondas\panorama.py') $Projeto
    $plano = @($pan | Select-String '^\s*onda \+(\d+): ([\d_ ]+) =' | Select-Object -First $Ondas)
    $saida = Join-Path $logs ("lore_{0}.md" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))
    foreach ($l in $plano) {
        $cenas = $l.Matches[0].Groups[2].Value.Trim() -split '\s+'
        "## onda +$($l.Matches[0].Groups[1].Value): $($cenas -join ' ')" | Add-Content -Encoding utf8 $saida
        & python (Join-Path $root 'framework\runtime\kb_phase.py') $Projeto onda --scenes @cenas | Add-Content -Encoding utf8 $saida
    }
    Write-Host "Lore das proximas $($plano.Count) onda(s) -> $saida. Decida as formas (glossario) antes de lancar o lote."
    exit 0
}
$parada = @((Join-Path $root 'scratch\PARADA.md'), (Join-Path $root "$Projeto\scratch\PARADA.md"))
$parada | Remove-Item -ErrorAction SilentlyContinue
# Estado: proxima onda e numero do lote. -OndaInicial explicito vence; sem estado, vale o padrao (1).
$estadoF = Join-Path $logs 'estado.json'
$estado = if (Test-Path $estadoF) { Get-Content $estadoF -Raw | ConvertFrom-Json } else { $null }
if ($estado -and -not $PSBoundParameters.ContainsKey('OndaInicial')) { $OndaInicial = [int]$estado.proxima_onda }
$loteN = if ($estado) { [int]$estado.lote + 1 } else { 1 }
# Tudo o que a janela mostra (inclusive o texto de um erro do script) vai tambem para logs/lote_<n>_console.log; o vigia le o fim dele.
$transcrito = $false
if (-not $Teste -and -not $TesteAgente) {
    try { Start-Transcript -Path (Join-Path $logs "lote_${loteN}_console.log") -Append | Out-Null; $transcrito = $true } catch { Write-Host 'transcript indisponivel.' }
}
# estado.json mais velho que o run_state.json = ondas fechadas fora deste script: a numeracao (e o multiplo de 3 do levantar-melhorias) sairia errada.
$rs = Join-Path $root "$Projeto\artifacts\run_state.json"
if ($estado -and -not $Teste -and -not $TesteAgente -and (Test-Path $rs) -and -not $PSBoundParameters.ContainsKey('OndaInicial') -and
    ((Get-Item $rs).LastWriteTime - (Get-Item $estadoF).LastWriteTime).TotalMinutes -gt 10) {
    Write-Host "AVISO: logs/estado.json (onda $($estado.proxima_onda)) esta mais velho que o run_state.json: houve onda fora deste script. Se o numero estiver errado, pare e rode com -OndaInicial <n> (a Retomada do ROADMAP diz qual)."
}
$t0 = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
if (-not $Teste -and -not $TesteAgente) {
    try { (& python (Join-Path $root '.claude\skills\panorama-ondas\panorama.py') $Projeto) | & python (Join-Path $root 'framework\runtime\estimar_lote.py') $logs $Ondas | Write-Host }
    catch { Write-Host 'estimativa indisponivel (panorama ou estimar_lote falhou).' }
}
$logsLote = @()

# Trava: uma execucao por vez (duas escrevendo nas mesmas cenas corrompem o estado). Sessao interativa aberta traduzindo cenas: nao rode.
$lock = Join-Path $logs '.lock'
if (Test-Path $lock) {
    $old = [int](Get-Content $lock -ErrorAction SilentlyContinue)
    if ($old -and (Get-Process -Id $old -ErrorAction SilentlyContinue)) { Write-Host "Ja ha uma execucao (PID $old). Parou."; exit 4 }
}
$PID | Out-File $lock
# Pedido do lote em disco (o vigia le daqui, nao da linha de comando da janela): numero, ondas pedidas, onda inicial, inicio.
if (-not $Teste -and -not $TesteAgente) {
    @{ lote = $loteN; pedidas = $Ondas; onda_inicial = $OndaInicial; inicio = $t0; pid = $PID } | ConvertTo-Json | Out-File -Encoding utf8 (Join-Path $logs 'lote_atual.json')
}
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
Voce e a sessao claude -p do lote (aberta pelo rodar_ondas.ps1), nao a sessao interativa: a regra "Onde roda" da skill NAO se aplica a voce; execute os passos 3 a 5e da onda.
Rode a skill rodar-onda em MODO CONTINUO para $Projeto. Esta e a onda numero $n (a ultima deste lote e a $($OndaInicial + $Ondas - 1)).
$(if ($Cenas) { "Aval do usuario (Felipe): esta onda tem SOMENTE a(s) cena(s) $Cenas, nenhuma outra, mesmo que passe de $MaxFalas falas; sem esperar o sim do passo 1." } else { "Aval permanente do usuario (Felipe): propor cenas na ordem do panorama.py, ate $MaxFalas falas, sem esperar o sim do passo 1." })
Siga o processo a risca, sem flag de bypass e sem contornar gate. Escalonamento do tradutor e lore sem forma: a onda termina,
com hitl_fila diferida (project.json) o escalonamento NAO para a onda: lore novo sem forma (nome, item, criatura, lugar) fica no original com lore_novo na fala; duvida real fica com escalate e vai para a fila. Conte os itens da fila no ONDA_OK. Decisao do usuario (2026-10-20): o fim do lote NAO para por causa da fila; ela e resolvida so quando o projeto acabar. Na ultima onda do lote termine com ONDA_OK normal. So no FIM (nenhuma cena restante) rode quality_gate.py e glossary_lint.py com --fechar e, se a fila tiver item, PARE com a tabela em scratch/PARADA.md (pasta .claude e protegida). Lore com 3 ou mais ocorrencias,
glossary_lint fora da fila nao corrigido e gate aberto tambem param. Fala critical sem retrotradução (back_translation_risk do project.json; high nao exige): passo 5c da skill (subagente Opus), sem parar. Veredito revise: passo 5e (Sonnet reescreve, ate 2 tentativas, o Opus re-julga so a fala; esgotou, a fala segue na fila e a onda NAO para); no --fechar o revise aberto entra na tabela do PARADA.
Subagente: comando unico no formato UTAP_DATA_DIR=<raiz>/projects/<nome>/backup_original/DataBase2.sdat python framework/runtime/wave.py projects/<nome> <cena> --backend in-session, sem export, sem cd, sem pipe (outro formato e negado em modo sem supervisao). Nao use Monitor nem run_in_background (quem vigia o lote e o vigia externo; monitor armado na sessao da onda a mantem viva depois do ONDA_OK). Lance TODOS os subagentes em primeiro plano e so escreva a linha final depois de receber o relatorio de cada um: encerrar o turno com subagente rodando faz o claude -p mata-lo e derruba a onda. Rode o levantar-melhorias apenas se $n for multiplo de 3.
Termine com uma unica linha final: ONDA_OK: <n cenas>, <x falas> | PARADA: <motivo> | FIM. Depois dela nao faca mais nada: encerre o turno na hora.
"@
    }
    $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    $log = Join-Path $logs "onda_${n}_$stamp.log"
    Write-Host "== onda $n ($stamp) -> $log"
    $tent = 0
    while ($true) {
        # A onda roda num job para o console poder bater a cada 3 min (o claude -p so devolve texto no fim).
        $job = Start-Job -ArgumentList $root, $prompt, $allow, $deny, $Modelo, $Esforco, $PrefixoEstavel -ScriptBlock {
            param($dir, $texto, $permite, $nega, $modelo, $esforco, $estavel)
            $extra = @()
            if ($esforco) { $extra += @('--effort', $esforco) }
            if ($estavel) { $extra += '--exclude-dynamic-system-prompt-sections' }
            Set-Location $dir
            $env:CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS = '1800000'   # tarefa em segundo plano pode levar ate 30 min (padrao 10) antes de o claude -p mata-la
            $o = $texto | & claude -p --no-chrome --model $modelo @extra --permission-mode acceptEdits `
                --allowedTools $permite --disallowedTools $nega 2>&1 | ForEach-Object { "$_" }
            [pscustomobject]@{ out = @($o); code = $LASTEXITCODE }
        }
        while (-not (Wait-Job $job -Timeout 180)) {
            $est = (& python (Join-Path $root 'framework\runtime\estimar_lote.py') --estado $Projeto) -join ' '
            Write-Host ("   [{0:HH:mm}] onda {1} em andamento: {2}" -f (Get-Date), $n, $est)
        }
        $res = Receive-Job $job
        Remove-Job $job
        $out = $res.out
        $code = $res.code
        # Limite de sessao ou de semana da assinatura: espera o horario de liberacao (+2 min, ver espera_reset.py)
        # e refaz a mesma onda (o estado vem do disco). Sem horario no aviso ou 8 tentativas: segue o fluxo normal.
        $seg = ($out -join "`n") | & python (Join-Path $root 'framework\runtime\espera_reset.py')
        if ($LASTEXITCODE -ne 0 -or -not $seg -or $tent -ge 8) { break }
        $tent++
        Write-Host "   limite de cota: espero $([int]$seg) s (ate $((Get-Date).AddSeconds([int]$seg))) e refaco a onda $n (tentativa $tent de 8)"
        $ate = (Get-Date).AddSeconds([int]$seg)
        while ((Get-Date) -lt $ate) {
            Start-Sleep -Seconds ([Math]::Max(1, [Math]::Min(300, [int]($ate - (Get-Date)).TotalSeconds)))
            if ((Get-Date) -lt $ate) { Write-Host ("   [{0:HH:mm}] esperando o reset da cota: faltam {1} min (volta as {2:HH:mm})" -f (Get-Date), [int]($ate - (Get-Date)).TotalMinutes, $ate) }
        }
    }
    if (-not $Teste -and -not $TesteAgente) {
        $out | Out-File -Encoding utf8 $log
        $logsLote += $log
    }
    # Vale a ULTIMA linha com a forma do contrato (ONDA_OK/PARADA/FIM), mesmo com texto solto depois (onda_fim.py);
    # sem nenhuma, cai na ultima linha nao vazia e o teste abaixo para a onda como fora do contrato.
    $last = (($out -join "`n") | & python (Join-Path $root 'framework\runtime\onda_fim.py'))
    if ($LASTEXITCODE -ne 0 -or -not $last) { $last = ($out | Where-Object { $_ -match '\S' } | Select-Object -Last 1) }
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
    if ($transcrito) { try { Stop-Transcript | Out-Null } catch { } }
    # Resumo do lote (so le o ledger e o run_state); roda em qualquer saida, inclusive PARADA.
    if ($logsLote.Count -gt 0) { & python (Join-Path $PSScriptRoot 'resumo_lote.py') $Projeto $t0 $loteN @logsLote; & python (Join-Path $PSScriptRoot 'conformidade_onda.py') $Projeto $t0 $Modelo @logsLote }
}
