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
