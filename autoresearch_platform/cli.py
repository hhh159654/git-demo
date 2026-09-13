from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from .review import next_review_path, render_reviewer_prompt
from .security import scan_tree
from .stages import STAGES, by_number, stage_complete
from .workspace import init_paper


def repo_root() -> Path:
    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        if (candidate / "AGENTS.md").exists() and (candidate / "prompts").exists():
            return candidate
    return here


def cmd_init(args: argparse.Namespace) -> int:
    root = repo_root()
    path = init_paper(root, args.paper, args.topic, args.domain, force=args.force)
    print(f"Initialized {path.relative_to(root)}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = repo_root()
    paper_dir = (root / args.paper).resolve()
    if not paper_dir.exists():
        print(f"Paper workspace not found: {paper_dir}", file=sys.stderr)
        return 2

    for stage in STAGES:
        ok = stage_complete(paper_dir, stage)
        gate = " GATE" if stage.gate else ""
        mark = "✓" if ok else "·"
        print(f"{mark} {stage.number:02d} {stage.command:<11} {stage.name}{gate}")
    return 0


def cmd_stage(args: argparse.Namespace) -> int:
    root = repo_root()
    paper_dir = root / args.paper
    stage = by_number(args.number)
    print(f"Stage {stage.number}: {stage.name} ({stage.command})")
    print(f"Gate: {'yes' if stage.gate else 'no'}")
    print("Expected outputs:")
    for output in stage.outputs:
        print(f"  - {paper_dir.name}/{output}")
    print(f"Definition of done: {stage.done}")
    return 0


def cmd_next_review(args: argparse.Namespace) -> int:
    root = repo_root()
    paper_dir = root / args.paper
    print(next_review_path(paper_dir).relative_to(root))
    return 0


def cmd_review_prompt(args: argparse.Namespace) -> int:
    root = repo_root()
    paper_dir = root / args.paper
    text = render_reviewer_prompt(paper_dir)
    if args.write:
        target = paper_dir / "configs" / "reviewer_prompt.generated.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        print(target.relative_to(root))
    else:
        print(text)
    return 0


def _version(cmd: list[str]) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return "not found"
    output = (proc.stdout or proc.stderr).strip().splitlines()
    return output[0] if output else f"exit={proc.returncode}"


def cmd_doctor(_: argparse.Namespace) -> int:
    print(f"python: {sys.version.split()[0]}")
    print(f"git:    {_version(['git', '--version'])}")
    print(f"conda:  {_version(['conda', '--version'])}")
    print(f"codex:  {_version(['codex', '--version'])}")
    print(f"ruff:   {_version(['ruff', '--version'])}")
    print(f"black:  {_version(['black', '--version'])}")
    print(f"pytest: {_version(['pytest', '--version'])}")
    if sys.version_info[:2] != (3, 12):
        print("WARNING: project policy expects Python 3.12")
    return 0


def cmd_check_secrets(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    findings = scan_tree(root)
    if not findings:
        print("Secret scan: OK")
        return 0
    print("Secret scan: BLOCKED", file=sys.stderr)
    for finding in findings:
        try:
            rel = finding.path.relative_to(root)
        except ValueError:
            rel = finding.path
        print(f"- {rel}: {finding.reason}", file=sys.stderr)
    return 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="autoresearch")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create a paper workspace.")
    p_init.add_argument("paper", help="Directory/branch style name, e.g. paper2")
    p_init.add_argument("--topic", required=True)
    p_init.add_argument("--domain", required=True)
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_status = sub.add_parser("status", help="Show 16-stage artifact status.")
    p_status.add_argument("paper")
    p_status.set_defaults(func=cmd_status)

    p_stage = sub.add_parser("stage", help="Show one stage contract.")
    p_stage.add_argument("paper")
    p_stage.add_argument("number", type=int)
    p_stage.set_defaults(func=cmd_stage)

    p_next = sub.add_parser("next-review", help="Show next review_roundN.md path.")
    p_next.add_argument("paper")
    p_next.set_defaults(func=cmd_next_review)

    p_prompt = sub.add_parser("review-prompt", help="Render reviewer prompt for a paper.")
    p_prompt.add_argument("paper")
    p_prompt.add_argument("--write", action="store_true")
    p_prompt.set_defaults(func=cmd_review_prompt)

    p_doctor = sub.add_parser("doctor", help="Check local research tooling.")
    p_doctor.set_defaults(func=cmd_doctor)

    p_scan = sub.add_parser("check-secrets", help="Fail if likely secrets/raw papers are present.")
    p_scan.add_argument("root", nargs="?", default=".")
    p_scan.set_defaults(func=cmd_check_secrets)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
