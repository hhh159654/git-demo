from pathlib import Path

from autoresearch_platform.workspace import init_paper, load_research_config


def test_init_paper(tmp_path: Path) -> None:
    paper = init_paper(tmp_path, "paper2", "topic", "domain")
    assert (paper / "AGENTS.md").exists()
    assert (paper / "ideas" / "topic.md").exists()
    assert (paper / "reference_papers_origin" / ".gitkeep").exists()
    cfg = load_research_config(paper)
    assert cfg["paper_id"] == "paper2"
    assert cfg["compute"]["max_remote_gpus"] == 1
