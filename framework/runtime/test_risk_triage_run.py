import argparse
import json
import subprocess

import risk_triage_run as rtr


def test_parse_keeps_only_batch_ids_and_counts_junk():
    assert rtr.parse('a1\tsentido trocado\nlixo\nzz\tfora do lote\nVAZIO\n', {'a1'}) == (['a1\tsentido trocado'], 2)
    assert rtr.parse('VAZIO', {'a1'}) == ([], 0)


def test_one_writes_verdict_and_retries_bad_format(tmp_path, monkeypatch):
    (tmp_path / 'lote_001.tsv').write_text('a1\tsrc\ttgt\n', encoding='utf-8')
    (tmp_path / 'triagem_prompt.md').write_text('p', encoding='utf-8')
    replies = iter(['lixo', 'a1\tmotivo'])
    monkeypatch.setattr(rtr.shutil, 'which', lambda n: 'claude')
    monkeypatch.setattr(subprocess, 'run', lambda *a, **k: argparse.Namespace(
        returncode=0, stdout=json.dumps({'result': next(replies), 'total_cost_usd': 0.01})))
    assert 'ok' in rtr.one(1, tmp_path, 'haiku', tmp_path)
    assert (tmp_path / 'veredito_001.tsv').read_text(encoding='utf-8') == 'a1\tmotivo\n'


def test_main_without_go_only_lists_and_never_calls_model(tmp_path, monkeypatch, capsys):
    (tmp_path / 'lote_001.tsv').write_text('a1\ts\tt\n', encoding='utf-8')
    monkeypatch.setattr(rtr.paths, 'require_project', lambda p: tmp_path)
    monkeypatch.setattr(rtr.risk_triage, '_dir', lambda r: tmp_path)
    monkeypatch.setattr(subprocess, 'run', lambda *a, **k: (_ for _ in ()).throw(AssertionError('chamou o modelo')))
    monkeypatch.setattr(rtr.sys, 'argv', ['x', 'p'])
    rtr.main()
    assert '1 lote(s)' in capsys.readouterr().out


def test_one_sem_claude_no_path_falha_com_mensagem_clara(tmp_path, monkeypatch):
    (tmp_path / 'lote_001.tsv').write_text('a1\tsrc\ttgt\n', encoding='utf-8')
    (tmp_path / 'triagem_prompt.md').write_text('p', encoding='utf-8')
    monkeypatch.setattr(rtr.shutil, 'which', lambda n: None)
    r = rtr.one(1, tmp_path, 'haiku', tmp_path)
    assert 'FALHOU' in r and 'nao esta no PATH' in r              # antes: TypeError dentro do subprocess.run


def test_one_claude_travado_vira_falha_com_timeout(tmp_path, monkeypatch):
    (tmp_path / 'lote_001.tsv').write_text('a1\tsrc\ttgt\n', encoding='utf-8')
    (tmp_path / 'triagem_prompt.md').write_text('p', encoding='utf-8')
    monkeypatch.setattr(rtr.shutil, 'which', lambda n: 'claude')

    def trava(*a, **k):
        raise subprocess.TimeoutExpired('claude', k['timeout'])
    monkeypatch.setattr(subprocess, 'run', trava)
    assert 'sem resposta em 900 s' in rtr.one(1, tmp_path, 'haiku', tmp_path)
