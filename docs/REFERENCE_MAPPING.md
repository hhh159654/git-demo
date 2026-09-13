# Reference Mapping

参考的 AutoResearchClaw fork 采用“AGENTS.md + 16-stage experiment toolbox”：

- 研究范围 → 文献 → 综合；
- baseline 缺陷复现；
- 假设与实验设计；
- 代码与资源规划；
- 实验 / refine；
- analysis / decision。

本平台没有复制上游完整实现，而是把它作为可选执行引擎，并把你的实际工作流放到第一层：

```text
AGENTS policy
  ├─ paper workspace
  ├─ ChatGPT reviewer loop
  ├─ Codex local implementation
  ├─ Git branch exchange
  └─ A800 remote execution
```

上游与本平台的最关键差异：

1. 本平台保留 `paperN/` 语义目录，方便 ChatGPT Web 只读单一论文上下文。
2. 原始 PDF 与远程服务器凭据明确 local-only。
3. Reviewer 产出固定为 `review_roundN.md`，Codex 固定产出 `response_roundN.md`。
4. 无 Slurm 的 GPU 轮询不自动开跑，只发现候选空闲 GPU。
