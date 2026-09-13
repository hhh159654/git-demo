from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StageContract:
    number: int
    command: str
    name: str
    outputs: tuple[str, ...]
    gate: bool = False
    done: str = ""


STAGES: tuple[StageContract, ...] = (
    StageContract(
        1,
        "topic",
        "TOPIC_INIT",
        ("ideas/topic.md", "configs/hardware_profile.json"),
        done="Topic, scope, target venue level, and compute constraints are explicit.",
    ),
    StageContract(
        2,
        "decompose",
        "PROBLEM_DECOMPOSE",
        ("ideas/problem_tree.md",),
        done="At least three prioritized, falsifiable sub-questions.",
    ),
    StageContract(
        3,
        "search",
        "SEARCH_STRATEGY",
        ("configs/search_plan.yaml",),
        done="Search plan covers direct neighbors, mechanisms, and failure modes.",
    ),
    StageContract(
        4,
        "collect",
        "LITERATURE_COLLECT",
        ("reference_papers_processed/metadata.jsonl",),
        done="High-quality candidate papers are recorded; raw PDFs stay local.",
    ),
    StageContract(
        5,
        "screen",
        "LITERATURE_SCREEN",
        ("reference_papers_processed/shortlist.jsonl",),
        gate=True,
        done="Research Opportunity Gate passed.",
    ),
    StageContract(
        6,
        "extract",
        "KNOWLEDGE_EXTRACT",
        ("reference_papers_processed/cards/",),
        done="Each shortlisted paper has a structured knowledge card.",
    ),
    StageContract(
        7,
        "synthesize",
        "SYNTHESIS",
        ("ideas/synthesis.md",),
        done="Nearest neighbors, gaps, and baseline defects are explicit.",
    ),
    StageContract(
        8,
        "reproduce",
        "BASELINE_REPRODUCE",
        ("experiments/reproduce/defect_report.md",),
        gate=True,
        done="Baseline defect is minimally reproduced or explicitly refuted.",
    ),
    StageContract(
        9,
        "hypothesize",
        "HYPOTHESIS_GEN",
        ("ideas/idea_main.md", "ideas/idea_backup.md"),
        done="Main and backup hypotheses are falsifiable and algorithmic.",
    ),
    StageContract(
        10,
        "design",
        "EXPERIMENT_DESIGN",
        ("experiments/exp_plan.yaml",),
        gate=True,
        done="Paper-candidate novelty gate and fair experiment plan are satisfied.",
    ),
    StageContract(
        11,
        "codegen",
        "CODE_GENERATION",
        ("experiments/src/", "experiments/experiment_spec.md"),
        done="Runnable, typed, CLI-reproducible experiment implementation exists.",
    ),
    StageContract(
        12,
        "plan",
        "RESOURCE_PLANNING",
        ("configs/schedule.yaml",),
        done="Time/GPU/resource plan fits the current budget.",
    ),
    StageContract(
        13,
        "experiment",
        "EXPERIMENT_RUN",
        ("results/runs/",),
        done="Planned runs have structured outputs.",
    ),
    StageContract(
        14,
        "refine",
        "ITERATIVE_REFINE",
        ("steps/refinement_log.md",),
        done="Failure diagnosis and non-equivalent refinements are recorded.",
    ),
    StageContract(
        15,
        "analyze",
        "RESULT_ANALYSIS",
        ("results/analysis.md",),
        done="Main metrics, variance, ablations, failure slices, and caveats are analyzed.",
    ),
    StageContract(
        16,
        "decide",
        "RESEARCH_DECISION",
        ("results/decision.md",),
        done="PROCEED / REFINE / PIVOT / ARCHIVE decision is evidence-based.",
    ),
)


def by_number(number: int) -> StageContract:
    for stage in STAGES:
        if stage.number == number:
            return stage
    raise ValueError(f"Unknown stage: {number}")


def path_is_materialized(path: Path) -> bool:
    if not path.exists():
        return False
    if path.is_dir():
        return any(item.name != ".gitkeep" for item in path.iterdir())
    return path.stat().st_size > 0


def stage_complete(paper_dir: Path, stage: StageContract) -> bool:
    return all(path_is_materialized(paper_dir / output) for output in stage.outputs)
