from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PAPER_DIRS: tuple[str, ...] = (
    "configs",
    "experiments/reproduce",
    "experiments/src",
    "ideas",
    "reference_papers_origin",
    "reference_papers_processed/cards",
    "responce_from_reviewer",
    "results/runs",
    "steps",
    "tests",
)


def paper_agents_text(paper_name: str) -> str:
    return f"""# {paper_name} — Local AGENTS.md

本文件是当前论文目录的就近规则。若与根目录 `AGENTS.md` 冲突，以更严格的科研与安全约束为准。

## 工作边界
- 默认只修改 `{paper_name}/`。
- 原始 PDF 只放 `reference_papers_origin/`，不得提交 Git。
- 服务器地址、账号、密码、token、私钥不得出现在本目录任何可提交文件中。

## 研究目标
- 目标：强 CCF-C；有稳定证据后再评估弱 CCF-B。
- 核心贡献必须是算法/机制层创新，不是 bug fix、wrapper、prompt 调参、纯 benchmark 或纯复现。
- 主方向失败时先做机制诊断；只有问题被证伪、近邻已解决或算法空间耗尽时才归档。

## 研究文件
- `ideas/`：问题、综合、主 idea、备选 idea。
- `steps/`：每轮具体修改与证据。
- `results/`：可审查的结构化结果与分析。
- `responce_from_reviewer/`：review / response 历史，只新增不覆盖。

## Codex 响应 reviewer
读取最新 `review_roundN.md` 后：
1. 先处理 P0；
2. 每个任务都要产生可验证文件/数值/测试；
3. 在 `steps/` 记录执行动作；
4. 在同目录新建 `response_roundN.md` 逐条回应；
5. 运行 ruff / black / pytest（若当前 paper 有代码）；
6. 不伪造未运行的实验结果。
"""


def paper_readme_text(paper_name: str, topic: str, domain: str) -> str:
    return f"""# {paper_name}

- Topic: {topic}
- Domain: {domain}
- Target: strong CCF-C; stretch goal weak CCF-B
- Default compute: at most one remote A800 unless explicitly approved otherwise

## Review loop

1. Codex reads `AGENTS.md`, performs research/implementation, writes `steps/` and `results/`.
2. Push current branch to GitHub.
3. ChatGPT reviewer reads this paper folder only and creates a new `review_roundN.md`.
4. Pull the branch locally.
5. Codex implements the atomic action items and writes `response_roundN.md`.
6. Repeat until the evidence is strong enough or the direction is archived.

Use `autoresearch status {paper_name}` to inspect the 16-stage research state.
"""


def research_config(paper_name: str, topic: str, domain: str) -> dict[str, Any]:
    return {
        "paper_id": paper_name,
        "topic": topic,
        "domain": domain,
        "target": {
            "baseline": "strong CCF-C",
            "stretch": "weak CCF-B",
        },
        "agents": {
            "reviewer": "ChatGPT Web",
            "implementer": "Codex CLI",
        },
        "compute": {
            "local_conda_env": "auto_research",
            "python": "3.12",
            "remote_gpu": "A800",
            "max_remote_gpus": 1,
            "remote_credentials_policy": "local-only; never commit",
        },
        "git": {
            "recommended_branch": paper_name,
            "raw_papers_committed": False,
            "processed_papers_committed": True,
        },
    }


def init_paper(
    root: Path, paper_name: str, topic: str, domain: str, *, force: bool = False
) -> Path:
    paper_dir = root / paper_name
    if paper_dir.exists() and any(paper_dir.iterdir()) and not force:
        raise FileExistsError(
            f"{paper_dir} already exists and is not empty. Use --force only if you understand the risk."
        )

    paper_dir.mkdir(parents=True, exist_ok=True)
    for rel in PAPER_DIRS:
        target = paper_dir / rel
        target.mkdir(parents=True, exist_ok=True)
        (target / ".gitkeep").touch(exist_ok=True)

    (paper_dir / "AGENTS.md").write_text(paper_agents_text(paper_name), encoding="utf-8")
    (paper_dir / "README.md").write_text(
        paper_readme_text(paper_name, topic, domain), encoding="utf-8"
    )
    config_path = paper_dir / "configs" / "research.yaml"
    config_path.write_text(
        yaml.safe_dump(
            research_config(paper_name, topic, domain),
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    topic_path = paper_dir / "ideas" / "topic.md"
    if not topic_path.exists() or topic_path.stat().st_size == 0:
        topic_path.write_text(
            f"# Topic\n\n{topic}\n\n## Domain\n\n{domain}\n\n## Constraints\n\n"
            "- Target: strong CCF-C\n"
            "- Default remote compute: 1 × A800 maximum\n"
            "- Raw papers remain local; processed Markdown may be committed\n",
            encoding="utf-8",
        )

    return paper_dir


def load_research_config(paper_dir: Path) -> dict[str, Any]:
    path = paper_dir / "configs" / "research.yaml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}
