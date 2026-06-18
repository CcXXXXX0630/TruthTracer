<p align="right">
  <sub>Academic Risk Early-Warning System · v2.1</sub>
</p>

# 🔍 TruthTracer

### *不问论文是不是造假。只问证据链从哪里开始断裂。*

<br>

> **"The most damaging phrase in science isn't 'this is fraudulent' — it's 'the evidence for this claim stops here.'"**
>
> TruthTracer 是一个学术风险预警系统。它不宣判"造假"——它系统性地审计研究逻辑、数据、统计、引用网络和可复现性，精确标定证据链从哪个环节开始失去支撑。

<br>

---

### 🏗️ 三引擎架构

<p align="center">
  <img src="https://img.shields.io/badge/检测方法-31-red?style=for-the-badge" alt="31 methods">
  <img src="https://img.shields.io/badge/引擎-3个-blue?style=for-the-badge" alt="3 engines">
  <img src="https://img.shields.io/badge/证据链-全程可追溯-success?style=for-the-badge" alt="traceable">
  <img src="https://img.shields.io/badge/许可-MIT-green?style=for-the-badge" alt="MIT">
</p>

```
      论文 / 作者 / 数据集
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
  STATS    NETWORK    CASE
  Engine   Engine    Builder
  (21种)   (10种)    (评分)
    │         │         │
    └─────────┼─────────┘
              ▼
    风险评级报告（证据链可追溯）
```

| 引擎 | 方法数 | 核心能力 |
|:------|:-----:|:--------|
| **STATS** | 21 | 数学不可能性检测（GRIM/Benford/p-curve/SPRITE/Statcheck...） |
| **NETWORK** | 10 | 开放 API 扫描：撤稿率、引文圈、合著闭包、发表速度... |
| **CASE** | — | 信号加权 + 论文类型感知 + 证据链生成 |

<br>

---

### 📊 风险分层

| 等级 | 标准 | 行动 |
|:------|:-----|:-----|
| 🔴 **CRITICAL** | 2+ 数学不可能性 | 上报伦理委员会，申请原始数据 |
| 🟠 **HIGH** | 1 不可能性 或 多强信号 | 申请原始数据，标记统计审查 |
| 🟡 **MEDIUM** | 统计异常，无不可能 | 要求澄清，交叉核验附录 |
| 🟢 **LOW** | 轻微模式异常 | 标准同行评审即�� |
| ⚪ **CLEAN** | 无相关信号 | 正常推进 |

> **LOW与MEDIUM的边界是TruthTracer最重要的区分。**

<br>

---

### ✅ 真案验证

| 对象 | 已知真相 | TruthTracer 判定 |
|:------|:--------|:---------------|
| Yoshitaka Fujii | 183篇撤稿（史上最多） | **HIGH RISK** — 撤稿率 21.4%，撤稿后仍发96篇 |
| Frances Arnold | 诺贝尔化学奖 2018，4篇自撤 | MEDIUM RISK — 自撤论文仍继续发表100篇 |
| 干净的经济学论文 | 无争议 | **LOW RISK** — 自动识别为"经济模型"，Benford折扣70% |

<br>

---

### 🧬 RIGID 框架实现

基于 Monash University (2024) 的 [RIGID 框架](https://doi.org/10.1016/j.eclinm.2024.102717)：

| RIGID 原则 | TruthTracer 实现 |
|:-----------|:---------------|
| 系统化评估 | 3引擎 × 31方法自动运行 |
| 多维度 | 统计 + 网络 + 文本 |
| 证据可追溯 | 每个 RED FLAG → 具体数据点 + 方法 |
| 风险分层 | 5级系统 + 论文类型上下文 |
| 不替代人类判断 | 每份报告标注"需要人类判断" |

<br>

---

### ⚡ 快速开始

```bash
# 1. 统计审计
python scripts/forensics.py audit --paper data.json > audit.json

# 2. 作者调查
python scripts/investigator.py investigate "Author Name" --deep > investigator.json

# 3. 证据整合
python scripts/case_builder.py audit.json investigator.json \
    --text extracted_text.txt --output report.md
```

<p align="center">
  <b>29/31 方法仅需 Python 标准库，无需 pip install。</b>
</p>

<br>

---

### 📁 结构

```
TruthTracer/
├── scripts/
│   ├── forensics.py          ← 21 种统计检测 (78 KB)
│   ├── investigator.py       ← 10 种网络信号 (36 KB)
│   ├── case_builder.py       ← 证据链生成 (19 KB)
│   ├── extract_pdf.py        ← PDF 文本提取
│   └── pysprite_vendor.py    ← GRIM + SPRITE 实现
├── examples/                   示例审计报告
├── investigations/             真实案件调查档案
├── references/                 方法论文档
├── SKILL.md                    Hermes Agent 定义
├── LICENSE                     MIT
└── CITATION.cff                学术引用
```

---

### 📖 引用

```bibtex
@software{TruthTracer,
  title = {TruthTracer: Academic Risk Early-Warning System},
  author = {CcXXXXX0630},
  year = {2026},
  url = {https://github.com/CcXXXXX0630/TruthTracer}
}
```

### 🙏 致谢

- RIGID 框架：Monash University (2024), doi:10.1016/j.eclinm.2024.102717
- GRIM + SPRITE 实现：基于 QuentinAndre/pysprite (MIT)
- 29/31 方法为原创实现

### ⚠️ 声明

TruthTracer 输出是**风险信号**，不是**定罪证据**。所有报告需要人类判断。

---

<p align="center">
  <sub>MIT License · <a href="https://github.com/CcXXXXX0630">CcXXXXX0630</a></sub>
</p>
