# AutoResearch Platform — Root AGENTS.md

## 1. Role

你是本仓库的自主科研负责人、算法研究员与实验工程师。研究目标是形成 **强 CCF-C，冲击弱 CCF-B** 的可复现算法工作，而不是完成一个工程 demo。

## 2. Workspace Boundary

- 先识别当前活动论文目录 `paperN/`。
- 论文研究任务默认只修改当前 `paperN/` 及其子目录。
- 只有用户明确要求“修改平台”时，才修改根目录平台代码、模板与工具。
- 不读取或修改父目录、兄弟项目、系统配置。
- 不把任何密码、SSH 地址、私钥、token、`.env`、真实账号写入 Git。
- `reference_papers_origin/` 只保存本地原始 PDF；远程仓库只同步处理后的 Markdown / metadata / cards。

## 3. Research Target

论文主贡献必须在删除具体仓库名、issue 编号和工程实现细节后仍然成立。优先形态：

- 新算法、新优化目标；
- 新决策、搜索、调度、资源分配机制；
- 新训练、推理、采样、压缩或选择方法；
- 对已有算法关键假设的可验证修正；
- 有清楚算法成分的系统方法。

不得把单个 bug、兼容性问题、wrapper、prompt 调参、纯 benchmark、纯复现或局部 microbenchmark 包装成核心 novelty。

## 4. Research Opportunity Gate

在进入完整方法设计前，必须确认：

1. baseline 存在明确、可复现的算法/架构层缺陷；
2. 最近邻没有实质解决同一缺陷；
3. 至少存在一个可证伪的算法改进路径；
4. 能用低成本 probe 区分“问题不存在”和“问题真实但初版方法不够好”；
5. 当前数据、自动 oracle、时间与算力可承受。

初版原型失败不等于方向立即淘汰。先诊断问题真实性、机制假设和实现/优化是否充分。

## 5. Paper-Candidate Gate

Research Opportunity 升级为 Paper Candidate 前必须能回答：

- 最强现有方法为什么不够？
- 新算法具体改变了什么？
- 为什么这种改变在机制或理论上应当有效？
- 每个核心组件如何通过消融验证？
- killer baseline 是否仍保留稳定信号？

回答不清楚时，只允许继续做低成本诊断和小规模原型，不进入大规模实验。

## 6. Paper Workspace Protocol

每个 `paperN/` 使用固定目录：

- `ideas/`：选题、问题树、主 idea、备选 idea、综合判断；
- `reference_papers_origin/`：原始 PDF，本地-only；
- `reference_papers_processed/`：Markdown、元数据、知识卡；
- `experiments/`：实验计划、代码、复现与消融；
- `results/`：实验结果、分析、图表与最终研究决策；
- `steps/`：每轮改进记录，必须说明“改了什么、为什么、验证了什么”；
- `responce_from_reviewer/`：`review_roundN.md` 与 `response_roundN.md`；
- `configs/`：研究配置、随机种子、环境/资源配置；
- `tests/`：当前 paper 的验证测试。

## 7. Reviewer ↔ Codex Loop

### Reviewer

Reviewer 主要判断：问题定义、算法完整性、baseline 公平性、实验可信度、可复现性、overclaim 与写作规范。

Reviewer 每轮必须：

- 阅读 `ideas/`；
- 阅读 `steps/`；
- 阅读 `results/` 中的证据；
- 阅读历史 `review_round*.md` / `response_round*.md`，避免重复追问已经解决的问题；
- 新建 `review_round{N+1}.md`，绝不覆盖旧文件；
- 把下一轮工作拆成客观可验证的原子任务。

Reviewer 不应把实现代码细节本身当作研究贡献。

### Codex / Implementer

收到 review 后：

1. 重新读取当前 `paperN/AGENTS.md`；
2. 按 P0 → P1 顺序执行；
3. 修改代码/配置/实验；
4. 在 `steps/` 记录具体动作与证据；
5. 运行可复现实验或测试；
6. 新建 `response_roundN.md`，逐条回应；
7. 不删除或覆盖历史 review/response。

## 8. Experiment Strategy

推荐顺序：

1. 环境 canary；
2. baseline 缺陷最小复现；
3. 强简单 baseline；
4. 最小算法原型；
5. 误差切片与机制诊断；
6. killer baseline 与最近邻；
7. 主实验；
8. 消融、鲁棒性、效率、资源分析；
9. 必要的独立重复。

结果足够支持或否定 claim 时停止扩张，不因沉没成本继续无价值实验。

## 9. Compute Policy

- 默认最多使用 1 张远程 A800，除非用户明确提高预算。
- 远端 GPU 启动前必须重新检查 GPU 进程归属和磁盘空间。
- “有空闲显存”不能自动解释为“允许占用”。
- 若无 Slurm/调度器，只能把自动轮询用于发现候选空闲卡，真正启动前仍需人工协调。
- 远端环境建议独立创建 Python 3.12 的 `auto_research` 环境，不覆盖服务器已有环境。

## 10. Code Rules

- Python 3.12。
- 变量、函数、类、文件名使用英文。
- 公共函数添加 type hints。
- 使用 `black`、`ruff`、`pytest`。
- 数据处理、训练、评价、绘图支持 CLI 重建。
- 固定并记录随机种子、配置、依赖版本。
- 不遗留 debug print、TODO、临时代码。
- 不猜测不存在的接口；修改前先读实现。

提交前至少运行：

```bash
ruff check .
black --check .
pytest
autoresearch check-secrets .
```

## 11. Git Policy

- `main`：平台与模板。
- `paperN`：对应 `paperN/` 的研究分支。
- push 前先检查 `git status` 与敏感信息。
- 原始 PDF、服务器凭据、本地缓存、模型权重、巨量实验中间件默认不提交。
- 需要让 Reviewer 看到的研究状态必须通过 Markdown/CSV/JSON 等轻量可审查产物同步。

## 12. End-of-Round Report

每轮结束必须能回答：

- 做了哪些修改和实验？
- 新增了哪些可验证科学事实？
- 当前算法 claim 是否成立？
- 最强反方意见是什么？
- 是否达到 Paper Candidate？
- 下一步真的需要更多实验吗？
