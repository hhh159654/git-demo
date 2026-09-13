# Codex Reviewer-Response Prompt

你正在处理 `{{PAPER_DIR}}` 的最新审稿意见。

1. 先完整读取 `{{PAPER_DIR}}/AGENTS.md`。
2. 找到最新 `review_roundN.md`。
3. 按 P0 → P1 顺序执行原子化工单。
4. 不允许只改文字来掩盖实验或方法缺陷。
5. 每个已执行动作都记录到 `steps/roundN_*.md`，包含：
   - 原 review 问题；
   - 实际修改；
   - 执行命令；
   - 验证结果；
   - 仍未解决的风险。
6. 若需要远程 GPU，只准备可复现实验包与命令；服务器凭据不得写入仓库。
7. 完成后运行：
   - `ruff check .`
   - `black --check .`
   - `pytest`
   - `autoresearch check-secrets .`
8. 在 `responce_from_reviewer/response_roundN.md` 逐条回复，不覆盖历史文件。
9. 如果某条无法完成，明确写出阻塞原因和最小下一步，不伪造结果。
