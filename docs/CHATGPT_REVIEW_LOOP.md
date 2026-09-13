# ChatGPT Review Loop

## 推荐 Reviewer 上下文

只给 Reviewer 当前 `paperN/`，避免它被平台实现代码和其他论文污染。

核心输入：

- `AGENTS.md`
- `ideas/`
- `steps/`
- `results/`
- `responce_from_reviewer/`
- `reference_papers_processed/` 中真正需要判断 novelty 的文献摘要/知识卡

Reviewer 不需要直接阅读 `experiments/src/` 的大段源代码。实现可信度通过测试输出、配置、manifest、结果文件来审查。

## 一轮结束标准

只有当以下内容都可追溯时才进入下一轮：

- review 文件已落盘；
- action items 有明确 owner（Codex/实验）；
- 每项 action 有输出路径；
- Codex 的 response 指向实际产物；
- 若 claim 依赖新实验，结果文件真实存在。
