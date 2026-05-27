from humantone.parser import load_rulepack, load_rulepacks


def test_load_rulepack_yaml():
    data = load_rulepack("rulepacks/zh/base-ai-trace.yml")
    assert data["name"] == "base-ai-trace"
    assert data["rules"][0]["rule_id"] == "base_001"


def test_load_rulepacks_dir():
    packs = load_rulepacks("rulepacks/zh")
    assert len(packs) >= 6
