from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    path: Path
    reason: str


BLOCKED_NAMES = {
    "sshconfig.md",
    "id_rsa",
    "id_ed25519",
    ".env",
}

BLOCKED_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}

CONTENT_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"(?im)^\s*(password|passwd)\s*[:=]\s*(?!<|your_|changeme|example|$)\S+"),
        "possible plaintext password",
    ),
    (
        re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
        "private key material",
    ),
    (
        re.compile(r"(?i)\b(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,})\b"),
        "possible API/token secret",
    ),
)


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"})


def scan_tree(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in root.rglob("*"):
        if should_skip(path) or not path.is_file():
            continue

        name = path.name.lower()
        if (
            (name in BLOCKED_NAMES or path.suffix.lower() in BLOCKED_SUFFIXES)
            and not name.endswith(".example")
            and ".example." not in name
        ):
            # Allow public-safe examples.
            findings.append(Finding(path, "blocked credential/secret filename"))
            continue

        # Raw paper PDFs are intentionally local-only.
        if "reference_papers_origin" in path.parts and path.name != ".gitkeep":
            findings.append(Finding(path, "raw reference paper should stay local"))
            continue

        # Skip likely binary / very large files.
        try:
            if path.stat().st_size > 2_000_000:
                continue
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for pattern, reason in CONTENT_PATTERNS:
            if pattern.search(text):
                findings.append(Finding(path, reason))
                break

    return findings
