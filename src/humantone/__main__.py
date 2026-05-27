from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analyzer import analyze_text
from .rewriter import build_rewrite_instruction
from .validator import validate_rewrite
from .schemas import RewriteInput, Constraints
from .pipeline import run_pipeline


def main() -> None:
    p = argparse.ArgumentParser(prog="humantone")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze")
    a.add_argument("input")
    a.add_argument("--scenario", default="academic_paper")
    a.add_argument("--locale", default="zh-Hant")
    a.add_argument("--region", default="TW")

    b = sub.add_parser("build-prompt")
    b.add_argument("input")
    b.add_argument("--scenario", default="academic_paper")
    b.add_argument("--mode", default="minimal_edit")
    b.add_argument("--locale", default="zh-Hant")
    b.add_argument("--region", default="TW")

    v = sub.add_parser("validate")
    v.add_argument("original")
    v.add_argument("rewritten")
    v.add_argument("--preserve-numbers", action="store_true")

    args = p.parse_args()
    if args.cmd == "analyze":
        text = Path(args.input).read_text(encoding="utf-8")
        out = {"ai_trace_signals": analyze_text(text, args.scenario)}
    elif args.cmd == "build-prompt":
        text = Path(args.input).read_text(encoding="utf-8")
        out = {"rewrite_instruction": build_rewrite_instruction(text, args.scenario, args.locale, args.region, {}, args.mode)}
    else:
        o = Path(args.original).read_text(encoding="utf-8")
        r = Path(args.rewritten).read_text(encoding="utf-8")
        c = Constraints(preserve_numbers=args.preserve_numbers)
        out = {"validation_result": validate_rewrite(o, r, c).__dict__}

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
