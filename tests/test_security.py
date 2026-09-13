from pathlib import Path

from autoresearch_platform.security import scan_tree


def test_scan_catches_password(tmp_path: Path) -> None:
    p = tmp_path / "bad.txt"
    p.write_text("password: real-secret-value", encoding="utf-8")
    findings = scan_tree(tmp_path)
    assert findings


def test_scan_allows_example_placeholder(tmp_path: Path) -> None:
    p = tmp_path / "safe.txt"
    p.write_text("password: <YOUR_PASSWORD>", encoding="utf-8")
    assert scan_tree(tmp_path) == []
