#!/bin/bash
# Vigia de lote para o Monitor do Claude Code (cada linha de saida vira um aviso). Checa a cada `passo` segundos (padrao 60)
# se a janela do rodar_ondas.ps1 esta viva, mas so fala quando ha o que dizer:
#   - batimento a cada 10 min (hora, cenas verified, idade do ultimo evento);
#   - onda nova fechada (linha final do log da onda);
#   - "PARADO?" se a janela vive e nenhum evento novo ha mais de 20 min (o espera_reset.py pode explicar; confirme na janela);
#   - cota (cota_uso.py: 1 chamada Haiku, ~US$ 0,003): no 1o ciclo, a cada onda fechada e ao acabar; "COTA ALTA" se a semana passar de
#     LIMITE_7D (env, padrao 85) -- o vigia so avisa, quem para o lote e voce (Ctrl+C na janela);
#   - ao acabar: "LOTE ENCERRADO" com o diagnostico (ondas fechadas x pedidas, ultima linha do ultimo log, estado, lock),
#     marcando "ENCERROU ANTES DO FIM" quando fecharam menos ondas do que o -Lote pedido.
# Uso: bash .claude/skills/rodar-onda/vigia_lote.sh [projects/<nome>] [segundos entre checagens, padrao 60]
cd "$(dirname "$0")/../../.." || exit 1
projeto="${1:-projects/utawarerumono_prelude}"
passo="${2:-60}"
logs=".claude/skills/rodar-onda/logs"

consulta() {
  # Vivo = o rodar_ondas.ps1 esta rodando = existe o .lock (ele o apaga ao sair). Nao serve olhar a janela: ela abre com
  # -NoExit e continua viva depois do fim do lote. Saida: "<1|0>|<inicio epoch (mtime do lock)>|<linha de comando da janela>"
  local cmd
  if [ -e "$logs/.lock" ]; then
    cmd=$(powershell -NoProfile -Command "(Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -match 'rodar_ond[a]s.ps1' -and \$_.Name -eq 'powershell.exe' } | Select-Object -First 1).CommandLine" | tr -d '\r')
    echo "1|$(stat -c %Y "$logs/.lock")|$cmd"
  else
    echo "0||"
  fi
}

fechadas_desde() {
  # logs de onda com ONDA_OK modificados depois do inicio do lote
  local ini="$1" n=0 f
  for f in "$logs"/onda_*.log; do
    [ -e "$f" ] || continue
    [ "$(stat -c %Y "$f")" -ge "$ini" ] && tail -n 3 "$f" | grep -q "^[^[:alnum:]]*ONDA_OK" && n=$((n+1))
  done
  echo "$n"
}

cota() {
  # "<hora> cota: 5h=..% 7d=..% reset5h=.." e aviso se a semana passar do teto; silencioso se a leitura falhar
  local c; c=$(python framework/runtime/cota_uso.py 2>/dev/null) || return 0
  echo "$(date +%H:%M) cota: $c"
  local w; w=$(echo "$c" | grep -o '7d=[0-9]*' | grep -o '[0-9]*$')
  [ -n "$w" ] && [ "$w" -ge "${LIMITE_7D:-85}" ] && echo "$(date +%H:%M) COTA ALTA: semana em ${w}% (teto ${LIMITE_7D:-85}%); considere parar o lote"
}

pedidas=""; inicio=0; vistas=-1; ultimo_bat=0; ult_ev_visto=""; parado_avisado=0
while true; do
  r=$(consulta); vivo=${r%%|*}; resto=${r#*|}
  if [ "$vivo" != "0" ]; then
    inicio=${resto%%|*}; cmd=${resto#*|}
    pedidas=$(echo "$cmd" | grep -o -E -- '-(Lote|Ondas) *[0-9]+' | grep -o '[0-9]*$' | head -1)
  fi
  # O rodar_ondas.ps1 grava o pedido em logs/lote_atual.json: vale mesmo com o vigia ligado depois do fim do lote.
  if [ -f "$logs/lote_atual.json" ]; then
    p=$(grep -o '"pedidas": *[0-9]*' "$logs/lote_atual.json" | grep -o '[0-9]*$'); [ -n "$p" ] && pedidas=$p
    i=$(grep -o '"inicio": *[0-9]*' "$logs/lote_atual.json" | grep -o '[0-9]*$'); [ -n "$i" ] && inicio=$i
  fi
  agora=$(date +%s)
  if [ "$vivo" = "0" ]; then
    if [ "$inicio" = "0" ]; then n="?"; else n=$(fechadas_desde "$inicio"); fi   # vigia ligado depois do fim: sem inicio conhecido
    cota
    echo "$(date +%H:%M) LOTE ENCERRADO: $n onda(s) fechada(s) de ${pedidas:-?} pedida(s)"
    [ -n "$pedidas" ] && [ "$n" != "?" ] && [ "$n" -lt "$pedidas" ] && echo "ENCERROU ANTES DO FIM: o texto do erro esta no fim de logs/lote_<n>_console.log (impresso abaixo)"
    python framework/runtime/lote_status.py "$projeto" "$logs"
    exit 0
  fi
  n=$(fechadas_desde "$inicio")
  if [ "$n" != "$vistas" ]; then
    cota
    [ "$vistas" != "-1" ] && echo "$(date +%H:%M) onda fechada ($n de ${pedidas:-?}): $(tail -n 1 "$(ls -t "$logs"/onda_*.log | head -1)" | cut -c1-120)"
    vistas=$n
  fi
  python framework/runtime/alerts.py correcoes "$projeto" --carencia 1800   # parada por defeito da traducao: alerta uma vez
  est=$(python framework/runtime/estimar_lote.py --estado "$projeto")
  ult=$(echo "$est" | grep -o 'ultimo evento ha [0-9]*' | grep -o '[0-9]*$')
  # evento anterior ao inicio do lote nao conta como silencio do lote (falso "PARADO?" no comeco)
  [ -n "$ult" ] && [ "$inicio" != "0" ] && [ $(( (agora - inicio) / 60 )) -lt "$ult" ] && ult=$(( (agora - inicio) / 60 ))
  if [ -n "$ult" ] && [ "$ult" -ge 20 ] && [ "$parado_avisado" = "0" ]; then
    echo "$(date +%H:%M) PARADO? janela viva, mas sem evento novo ha ${ult} min. $est"; parado_avisado=1
  fi
  [ -n "$ult" ] && [ "$ult" -lt 20 ] && parado_avisado=0
  if [ $((agora - ultimo_bat)) -ge 600 ]; then
    echo "$(date +%H:%M) lote_vivo=$vivo ondas=$n/${pedidas:-?} $est"; ultimo_bat=$agora
  fi
  sleep "$passo"
done
