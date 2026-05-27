from pathlib import Path
from humantone.schemas import RewriteInput
from humantone.pipeline import run_pipeline


def test_pipeline_output_schema():
    text = Path("tests/fixtures/zh_hant_academic_conclusion.txt").read_text(encoding="utf-8")
    payload = RewriteInput(text=text, scenario="academic_paper")
    out = run_pipeline(payload)
    d = out.to_dict()
    for k in ["ai_trace_signals", "severity_summary", "rewrite_instruction", "validation_result", "change_log"]:
        assert k in d
