# Workflow

## A. 选题与文献

1. ChatGPT / 人类先确定研究约束：领域、目标级别、1×A800 等。
2. 收集约 20 篇高质量直接近邻/关键 baseline。
3. 原 PDF 放 `reference_papers_origin/`，不提交。
4. 转为 Markdown / metadata / cards 后放 `reference_papers_processed/` 并提交。
5. 形成主方向 + 一个机制不同的备选方向。

## B. 高频闭环

```text
Codex local work
    ↓
steps + results + response
    ↓ git push
GitHub paperN branch
    ↓
ChatGPT Web review
    ↓ review_roundN.md
GitHub paperN branch
    ↓ git pull
Codex fixes / experiments
    ↺
```

## C. 何时上 A800

只有本地 canary 和实验设计通过后再上远端：

- 本地先确认入口命令、依赖、数据路径；
- 先估算单次显存、时间、输出大小；
- 远端先只读检查 GPU / PID 归属 / 磁盘；
- 无调度器时，自动轮询只发现“候选空闲”，不自动抢卡；
- 运行完成把轻量结果、日志摘要、配置和指标同步回 Git；
- 大模型权重、cache、原始数据不进 Git。
