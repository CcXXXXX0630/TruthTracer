<p align="right">
  <sub>学术风险预警系统 · v2.1</sub>
</p>

<p align="center">
  <a href="README.md">🇬🇧 English</a>
</p>

# 🔍 TruthTracer · 真相追踪者

### *不问论文是不是造假。只问证据链从哪里开始断裂。*

<br>

> **"科学中最致命的不是'这篇论文造假'——而是'支撑这个结论的证据，到这里就断了'。"**
>
> TruthTracer 是一个学术风险预警系统。它不宣判"造假"——它像审稿人、科研诚信官和出版商调查员的合体一样，系统性地审计研究逻辑、数据、统计、引用网络和可复现性，精确定位证据链从哪个环节开始失去支撑。

<br>

---

### 🏗️ 三引擎架构

<p align="center">
  <img src="https://img.shields.io/badge/方法-31种-red?style=for-the-badge" alt="31 methods">
  <img src="https://img.shields.io/badge/引擎-3个-blue?style=for-the-badge" alt="3 engines">
  <img src="https://img.shields.io/badge/证据-全程可追溯-success?style=for-the-badge" alt="traceable">
  <img src="https://img.shields.io/badge/许可-MIT-green?style=for-the-badge" alt="MIT">
</p>

```
       论文 / 作者 / 数据集
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
  统计引擎   网络引擎   案件构建器
  (21种)    (10种)     (智能评分)
    │         │         │
    └─────────┼─────────┘
              ▼
     风险评级报告
     （证据链可追溯）
```

| 引擎 | 方法数 | 检测什么 |
|:------|:-----:|:--------|
| **统计引擎** | 21 | 报告数据中的数学不可能性（GRIM/Benford/p-curve/SPRITE/Statcheck...） |
| **网络引擎** | 10 | 开放API扫描：撤稿率、引文圈、合著闭包、发表速度... |
| **案件构建器** | — | 信号加权 + 论文类型感知 + 证据链生成 |

<br>

---

### 📊 五级风险分层

| 等级 | 标准 | 行动建议 |
|:------|:-----|:--------|
| 🔴 **危急** | 2项以上数学不可能性 | 上报伦理委员会；申请原始数据 |
| 🟠 **高危** | 1项不可能性 或 多项强信号 | 申请原始数据；标记统计审查 |
| 🟡 **中危** | 统计异常，无不可能性 | 要求作者澄清；交叉核验附录 |
| 🟢 **低危** | 轻微模式异常 | 标准同行评审即可 |
| ⚪ **清洁** | 无相关信号 | 正常推进 |

> **低危与中危的边界，是 TruthTracer 最重要的区分。**

<br>

---

### ✅ 真案验证

| 对象 | 已知事实 | TruthTracer 判定 |
|:------|:--------|:---------------|
| 藤井善隆 (Yoshitaka Fujii) | 183篇撤稿（史上最多） | **高危** — 撤稿率21.4%，撤稿后仍发表96篇 |
| 弗朗西斯·阿诺德 (Frances Arnold) | 2018年诺贝尔化学奖，4篇主动撤稿 | 中危 — 自撤后继续发表100篇 |
| 一篇无争议的经济学论文 | 正常发表 | **低危** — 自动识别为"经济模型"，Benford权重自动折扣70% |

<br>

---

### 🧬 RIGID 框架实现

基于莫纳什大学 (2024) 的 [RIGID 框架](https://doi.org/10.1016/j.eclinm.2024.102717)：

| RIGID 原则 | TruthTracer 实现 |
|:-----------|:---------------|
| 系统化评估 | 3引擎 × 31方法全自动运行 |
| 多维度 | 统计 + 网络 + 文本信号 |
| 证据可追溯 | 每个 RED FLAG 关联到具体数据点和方法 |
| 风险分层 | 5级系统，根据论文类型自适应调整 |
| 不替代人类判断 | 每份报告标注"需要人类判断" |

<br>

---

### ⚡ 快速开始

```bash
# 1. 统计审计
python scripts/forensics.py audit --paper data.json > audit.json

# 2. 作者调查
python scripts/investigator.py investigate "作者姓名" --deep > investigator.json

# 3. 证据整合
python scripts/case_builder.py audit.json investigator.json \
    --text extracted_text.txt --output report.md
```

<p align="center">
  <b>31种方法中29种仅需Python标准库，无需pip安装任何依赖。</b>
</p>

<br>

---

### 📁 项目结构

```
TruthTracer/
├── scripts/
│   ├── forensics.py          ← 21种统计检测 (78 KB)
│   ├── investigator.py       ← 10种网络信号 (36 KB)
│   ├── case_builder.py       ← 证据链生成 (19 KB)
│   ├── extract_pdf.py        ← PDF文本提取
│   └── pysprite_vendor.py    ← GRIM + SPRITE 算法
├── examples/                    示例审计报告
├── investigations/              真实案件调查档案
├── references/                  方法论文档
├── SKILL.md                     Hermes Agent 定义
├── README.md                    英文主页
├── README_CN.md                 中文主页
├── LICENSE                      MIT
└── CITATION.cff                 引用格式
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

- RIGID 框架：莫纳什大学 (2024), doi:10.1016/j.eclinm.2024.102717
- GRIM + SPRITE 算法：改编自 QuentinAndre/pysprite (MIT)
- 31种方法中29种为原创实现

### ⚠️ 声明

TruthTracer 输出的是**风险信号**，不是**定罪证据**。所有报告均需人类判断。检测到异常 ≠ 证明造假。

---

<p align="center">
  <sub>MIT License · <a href="https://github.com/CcXXXXX0630">CcXXXXX0630</a></sub>
</p>
