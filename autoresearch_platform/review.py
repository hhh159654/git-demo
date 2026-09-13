from __future__ import annotations

import re
from pathlib import Path

from .workspace import load_research_config

_REVIEW_RE = re.compile(r"^review_round(\d+)\.md$")


def existing_review_rounds(review_dir: Path) -> list[int]:
    if not review_dir.exists():
        return []
    rounds: list[int] = []
    for path in review_dir.iterdir():
        match = _REVIEW_RE.match(path.name)
        if match:
            rounds.append(int(match.group(1)))
    return sorted(rounds)


def next_review_round(paper_dir: Path) -> int:
    rounds = existing_review_rounds(paper_dir / "responce_from_reviewer")
    return (rounds[-1] + 1) if rounds else 1


def next_review_path(paper_dir: Path) -> Path:
    return paper_dir / "responce_from_reviewer" / f"review_round{next_review_round(paper_dir)}.md"


def _root_for(paper_dir: Path) -> Path:
    # paperN is expected to be directly under repo root.
    return paper_dir.resolve().parent


def render_reviewer_prompt(paper_dir: Path) -> str:
    repo_root = _root_for(paper_dir)
    template = repo_root / "prompts" / "reviewer_strong_ccfc.md"
    if not template.exists():
        raise FileNotFoundError(f"Missing prompt template: {template}")

    cfg = load_research_config(paper_dir)
    domain = str(cfg.get("domain", "YOUR_RESEARCH_DOMAIN"))
    paper_name = paper_dir.name
    n = next_review_round(paper_dir)

    text = template.read_text(encoding="utf-8")
    return (
        text.replace("{{PAPER_DIR}}", paper_name)
        .replace("{{DOMAIN}}", domain)
        .replace("{{NEXT_ROUND}}", str(n))
    )
