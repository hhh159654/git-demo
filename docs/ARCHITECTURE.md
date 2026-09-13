# Architecture

## 核心设计

本平台把“研究判断”和“代码执行”拆开：

```text
                 ┌────────────────────────────┐
                 │ ChatGPT Web Reviewer       │
                 │ 只看 paperN 的研究产物      │
                 └─────────────┬──────────────┘
                               │ review_roundN.md
                               ▼
┌──────────────┐   pull   ┌──────────────────────┐   run   ┌─────────────────┐
│ GitHub       │◄────────►│ Local Linux / WSL    │───────►│ A800 (optional) │
│ paperN branch│   push   │ Codex CLI + conda    │        │ experiment only │
└──────────────┘          │ auto_research        │        └─────────────────┘
                          └──────────┬───────────┘
                                     │
                                     ▼
                         steps / results / response
```

## 为什么保留 16 stages

参考 ResearchClaw experiment-toolbox 思路，把 paper-writing 自动化从主流水线中拿掉，把重点放在：

- 找到真实研究缺口；
- 复现 baseline 的算法缺陷；
- 生成可证伪假设；
- 实验设计与可复现执行；
- 结果诊断与 PIVOT / REFINE 决策。

论文叙事和审稿则由 Reviewer ↔ Codex 循环反复打磨。

## 三个强制 Gate

### Stage 5 — Research Opportunity Gate

没有真实、算法层、近邻未解决的缺陷，不进入后续。

### Stage 8 — Baseline Reproduce Gate

没有最小证据确认 baseline 缺陷，就不能直接发明新方法。

### Stage 10 — Paper-Candidate Novelty Gate

在大实验前，必须说清：

1. 最强方法为什么不够；
2. 新算法改变了什么；
3. 为什么该改变应有效；
4. 如何用消融和 killer baseline 证伪。

## 文件映射

| 研究阶段 | 本仓库主要产物 |
|---|---|
| Topic / Decompose | `ideas/topic.md`, `ideas/problem_tree.md` |
| Search / Collect / Screen / Extract | `reference_papers_processed/` |
| Synthesis | `ideas/synthesis.md` |
| Baseline Reproduce | `experiments/reproduce/` |
| Hypothesis | `ideas/idea_main.md`, `ideas/idea_backup.md` |
| Design / Codegen | `experiments/` |
| Resource Plan | `configs/schedule.yaml` |
| Experiment / Refine | `results/runs/`, `steps/` |
| Analysis / Decision | `results/analysis.md`, `results/decision.md` |
| Reviewer Loop | `responce_from_reviewer/` |
