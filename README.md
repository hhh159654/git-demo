# AutoResearch Platform Starter

这是一个面向 **ChatGPT Web 审稿 + Codex CLI 本地研究/实现 + GitHub 分支同步 + A800 实验** 的科研工作台。

它不直接复制 AutoResearchClaw 的完整代码，而是保留其最适合当前工作流的思想：

- 16-stage research-to-experiment pipeline；
- `AGENTS.md` 作为最高优先级研究规则；
- 文献筛选、baseline 缺陷复现、实验设计三个 gate；
- 每个 paper 独立工作区；
- ChatGPT 只负责审稿/研究判断，不负责读实现代码；
- Codex CLI 负责本地实现、实验、测试、响应审稿；
- 原始 PDF 与服务器私密配置仅保存在本地；
- GitHub 只同步可复现、可审查、无敏感信息的研究产物。

## 1. 推荐目录模型

```text
repo/
├── AGENTS.md
├── autoresearch_platform/      # 平台轻量 CLI
├── prompts/                    # Reviewer / Codex 提示词模板
├── templates/paper/            # 新论文工作区模板
├── tools/                      # Git / A800 / reference bootstrap 工具
├── docs/                       # 架构和操作说明
├── paper1/                     # 示例/第一篇论文工作区
└── tests/
```

每个 `paperN/` 内部固定为：

```text
paperN/
├── AGENTS.md
├── README.md
├── configs/
├── experiments/
├── ideas/
├── reference_papers_origin/        # 本地原始 PDF，禁止提交
├── reference_papers_processed/     # Markdown / cards，可提交
├── responce_from_reviewer/         # 保留既有拼写，兼容原流程
├── results/
├── steps/
└── tests/
```

> `responce_from_reviewer` 是为兼容现有流程而保留的历史拼写，不建议中途改名。

## 2. 初始化

推荐 Linux / WSL，Python 3.12，Conda 环境固定为 `auto_research`：

```bash
conda env create -f environment.yml
conda activate auto_research
pip install -e ".[dev]"

autoresearch doctor
pytest
```

如果环境已经存在：

```bash
conda activate auto_research
pip install -e ".[dev]"
```

## 3. 第一篇论文

仓库已带一个 `paper1/` 空工作区。修改：

```text
paper1/configs/research.yaml
```

然后生成面向 ChatGPT Web 的审稿提示词：

```bash
autoresearch review-prompt paper1 --write
```

输出：

```text
paper1/configs/reviewer_prompt.generated.md
```

## 4. 新建 paper2 / paper3

推荐“一篇论文一个分支 + 一个同名目录”：

```bash
git switch main
git pull
git switch -c paper2

autoresearch init paper2 \
  --topic "你的题目" \
  --domain "你的研究领域"

git add paper2
git commit -m "init paper2 workspace"
git push -u origin paper2
```

之后 ChatGPT Web 只读取 `paper2/`，Codex CLI 在本地处理 `paper2/`。

## 5. 高频 reviewer ↔ Codex 循环

### Codex 完成一轮

```bash
ruff check .
black --check .
pytest

git add .
git commit -m "paper2: research iteration"
git push origin paper2
```

### ChatGPT Web 审稿

1. 只读取当前 `paperN/`。
2. 重点读取 `ideas/`、`steps/`、`results/`、`responce_from_reviewer/`。
3. 不以源代码实现细节作为论文 novelty。
4. 新建 `review_roundN.md`，不覆盖历史文件。

### Codex 响应

```bash
git pull --ff-only origin paper2
```

把最新 `review_roundN.md` 交给 Codex，并要求它：

- 重新读取当前 paper 的 `AGENTS.md`；
- 逐项执行 P0/P1 工单；
- 把修改记录写到 `steps/`；
- 把对审稿意见的逐条回应写到 `responce_from_reviewer/response_roundN.md`；
- 必须运行测试/检查后才能 push。

查看下一轮编号：

```bash
autoresearch next-review paper2
```

## 6. 16-stage 研究骨架

```text
1  topic       -> 选题与约束
2  decompose   -> 问题拆解
3  search      -> 检索策略
4  collect     -> 文献收集
5  screen      -> Research Opportunity Gate
6  extract     -> 知识卡
7  synthesize  -> 缺口综合
8  reproduce   -> baseline 缺陷复现 Gate
9  hypothesize -> 主方向 + 备选方向
10 design      -> Paper-Candidate Novelty Gate
11 codegen     -> 实验代码
12 plan        -> 资源规划
13 experiment  -> 实验执行
14 refine      -> 诊断与迭代
15 analyze     -> 结果分析
16 decide      -> PROCEED / REFINE / PIVOT / ARCHIVE
```

查看某一步应产出什么：

```bash
autoresearch stage paper1 8
autoresearch status paper1
```

## 7. AutoResearchClaw 参考实现

仓库提供一个可选 bootstrap 脚本，把参考项目装到本地 `.vendor/`，但不提交：

```bash
bash tools/bootstrap_reference.sh
```

它用于对照/复用 ResearchClaw CLI，不是本仓库的敏感配置存放位置。

## 8. A800

服务器地址、账号、密码、SSH 私钥 **都不能进入 Git**。

只在本机创建：

```bash
cp config/a800.env.example config/local/a800.env
```

然后配置一个本地 SSH alias，再运行：

```bash
set -a
source config/local/a800.env
set +a

bash tools/a800_status.sh
bash tools/a800_wait_candidate.sh
```

`a800_wait_candidate.sh` **只报告候选空闲 GPU，不自动占卡**。没有调度器时，显存空闲不等于 GPU 可直接使用，真正启动训练前仍需要人工确认。

## 9. 安全检查

```bash
autoresearch check-secrets .
```

CI 也会执行同样检查。`sshconfig.md`、`.env`、私钥、原始 PDF 等默认都被 `.gitignore` 拦截。

## 10. 推送到目标 GitHub 仓库

将本目录内容复制到你本地 clone 的空仓库后：

```bash
git add .
git commit -m "bootstrap autoresearch platform"
git push -u origin main
```

本项目不存储任何真实服务器密码或账号。
