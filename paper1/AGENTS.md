# paper1 — Local AGENTS.md

本文件是当前论文目录的就近规则。若与根目录 `AGENTS.md` 冲突，以更严格的科研与安全约束为准。

## 工作边界
- 默认只修改 `paper1/`。
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
