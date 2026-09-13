# Sensitivity-Supervised Analog Circuit Representation Learning for Cross-Topology Transfer

## 1. Research Motivation

现有模拟电路表示学习方法通常主要利用以下信息：

- 电路拓扑结构；
- 器件类型和静态参数；
- DC operating point 或其他静态状态；
- 电路物理约束。

但是这些信息并没有直接描述一个对于模拟电路设计非常关键的问题：

> 如果改变某个器件的设计参数，整个电路的电气性能会发生什么变化？

这种“器件参数变化 → 电路性能响应”的关系直接包含了电路的设计敏感性、
器件重要性以及功能信息。

本研究希望利用电路模拟器自动产生 component-level interventions，
并将这些 intervention 对电路性能产生的响应作为表示学习的监督信号。

---

## 2. Core Research Question

核心问题为：

> 能否通过 simulator-generated component-level interventions，
> 学习一种包含模拟电路设计敏感性与功能信息的表示，
> 并使这种表示在未见过的新拓扑和小样本下游任务上具有更好的迁移能力？

---

## 3. Component-Level Intervention

对于一个模拟电路中的器件 i，其某个设计参数记为：

p_i

例如：

- MOS transistor width W；
- MOS transistor length L；
- resistor resistance R；
- capacitor capacitance C。

首先运行 nominal circuit，获得原始性能：

y_k

其中性能指标可以包括：

- Gain；
- Bandwidth / UGBW；
- Phase Margin；
- Power。

然后对单个器件参数施加小幅扰动，例如：

p_i -> p_i × 0.95

或：

p_i -> p_i × 1.05

重新运行 HSPICE，并获得扰动后的性能：

y'_k

---

## 4. Sensitivity Supervision

我们不希望模型只学习“参数变了多少”，而是希望它学习：

“某个器件的某个参数变化，对整个电路性能产生多大的影响。”

初步定义 normalized sensitivity：

S_ik = (Δy_k / y_k) / (Δp_i / p_i)

其中：

- i 表示器件/参数；
- k 表示电路性能指标。

因此，每个器件可以获得一个 sensitivity response vector，例如：

[M1.W]

- Gain sensitivity
- Bandwidth sensitivity
- Phase Margin sensitivity
- Power sensitivity

该向量描述这个器件对于整个电路功能的重要程度以及影响方式。

---

## 5. Working Hypothesis

当前工作假设为：

如果一个电路表示模型能够预测不同器件参数扰动所引起的电气响应，
那么其 embedding 将不仅包含拓扑信息，还会包含：

- component importance；
- design sensitivity；
- functional role；
- circuit-level interaction。

因此，相比仅使用 topology 或 static operating state 训练得到的表示，
这种 sensitivity-supervised representation 应当在新拓扑和少标注数据情况下
具有更好的迁移能力。

---

## 6. Primary Scientific Claim to Test

当前不是假设该方法一定有效，而是需要验证以下 claim：

> Sensitivity supervision 提供了 topology/static-state supervision
> 中缺失的功能信息，并且这种信息能够提升 unseen-topology transfer。

如果这个 claim 无法通过实验得到支持，则当前研究方向需要 REFINE 或 PIVOT。

---

## 7. Initial Baselines

后续实验至少需要公平比较：

Topology Only

Topology + Static Operating State

Topology + Simulator Performance Labels

Topology + Sensitivity Supervision

所有方法尽可能采用相同 encoder、模型容量、训练预算和 downstream protocol。

这样才能判断性能提升是否真正来自 sensitivity information，
而不是因为增加了更多 simulator-generated labels。

---

## 8. Primary Evaluation Setting

论文最重要的实验设置不是随机划分相同拓扑的数据，而是：

Held-Out Topology Transfer。

例如：

Train:

T1
T2
T3
T4

Test / Transfer:

T5

预训练阶段完全不使用 T5。

随后只提供 T5 的一小部分 downstream labels，例如：

1%
5%
10%
20%
100%

重点观察 sensitivity-supervised representation 是否在
1% - 20% low-data regime 中表现出明显优势。

---

## 9. Minimal Feasibility Experiment

在设计复杂模型以前，首先验证 sensitivity signal 本身是否存在。

初始实验使用少量模拟电路 topology。

对每种 topology：

1. 运行 nominal HSPICE simulation；
2. 选择关键器件；
3. 分别对 W / L / R / C 等参数进行 ±5% intervention；
4. 重新运行仿真；
5. 记录 Gain、Bandwidth、Phase Margin、Power；
6. 计算 normalized sensitivity；
7. 比较不同 topology 中是否出现稳定、可迁移的 sensitivity structure。

只有这个实验能够证明存在可学习信号后，
才进入大规模 representation-learning experiment。

---

## 10. Main Rejection Risk

目前最关键的审稿风险是：

> “这是否只是把有限差分 sensitivity 当作一个普通 auxiliary task？”

因此后续研究必须提供证据证明：

1. 现有 circuit representation 确实缺少 intervention-response information；
2. sensitivity supervision 学到的不是 topology shortcut；
3. sensitivity supervision 的价值不是简单增加 simulator labels；
4. sensitivity information 能真正改善 unseen-topology low-data transfer。

---

## 11. Current Status

Current stage:

Research Problem Definition

Next stages:

Problem Decomposition
→ Literature Search
→ Literature Screening
→ Baseline Defect Reproduction
→ Hypothesis Validation
→ Experiment Design

当前的 sensitivity-based method 只视为 working hypothesis，
在完成文献检索和 baseline defect reproduction 前，不将其视为已经成立的论文方法。
