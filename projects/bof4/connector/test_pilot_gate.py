from pilot_gate import check


def test_check_blocks_what_the_pilot_missed():
    state = {"A": {"status": "verified", "bypassed_gates": []},
             "B": {"status": "verified", "bypassed_gates": ["kb"]}}
    scope = {"A": "sim", "B": "sim", "C": "sim", "D": "nao", "E": "?"}
    got = check({"A", "B", "C", "D", "E", "F"}, scope, state)
    assert [p.split(":")[0] for p in got] == ["B", "C", "E", "F"]
    assert check({"A", "D"}, scope, state) == []
