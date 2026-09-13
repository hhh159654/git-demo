from pathlib import Path

from autoresearch_platform.review import next_review_round


def test_review_round_increment(tmp_path: Path) -> None:
    paper = tmp_path / "paper9"
    review = paper / "responce_from_reviewer"
    review.mkdir(parents=True)
    assert next_review_round(paper) == 1
    (review / "review_round1.md").write_text("x", encoding="utf-8")
    (review / "response_round1.md").write_text("x", encoding="utf-8")
    (review / "review_round3.md").write_text("x", encoding="utf-8")
    assert next_review_round(paper) == 4
