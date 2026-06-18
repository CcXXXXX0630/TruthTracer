<p align="right">
  <sub>Academic Data Forensics Toolkit · v1.0</sub>
</p>

# 🔍 VeritasKit

### *让每一行数据，经得起真相的凝视*

<br>

> **"统计学家的直觉，现在有了可复现的代码。"**
>
> 审稿时你觉得某个表格"看起来太完美了"。VeritasKit 把这种直觉变成数学检验——10 种检测方法，一份审计报告，全程可追溯。

<br>

---

### 📋 一次审计，十条线索

<p align="center">
  <img src="https://img.shields.io/badge/检测方法-10-red?style=for-the-badge" alt="10 methods">
  <img src="https://img.shields.io/badge/假阳性控制-3%20signal%20cross--check-success?style=for-the-badge" alt="cross-check">
  <img src="https://img.shields.io/badge/输出-结构化审计报告-blue?style=for-the-badge" alt="report">
  <img src="https://img.shields.io/badge/许可-MIT-green?style=for-the-badge" alt="MIT">
</p>

| 检测 | 查什么 | 致命性 |
|:-----|:-------|:------:|
| **Benford 定律** | 人为编造的数字，首位分布会偏离对数规律 | 🔴🔴🔴 |
| **GRIM 检验** | 均值×样本量 ≠ 整数 → 至少一个数据是编的 | 🔴🔴🔴 |
| **Mass Balance** | 输入 ≠ 输出 + 积累 → 物质不守恒 | 🔴🔴🔴 |
| **SPRITE** | 整数量表多道题的答案互相矛盾 | 🔴🔴 |
| **p-curve** | p 值分布左偏 → 存在 p-hacking | 🔴🔴 |
| **Statcheck** | APA 格式报告的统计量，重新算一遍对不上 | 🔴🔴 |
| **参数审计** | 模型参数的先验分布不可能出现在自然界 | 🔴🔴 |
| **Bootstrap 一致性** | 描述的均值、SD、范围彼此矛盾 | 🔴 |
| **效应量一致性** | 效应量—样本量—统计功效三角不闭合 | 🔴 |
| **数字偏好** | 人工填写的数据末位回避 0 和 5 | 🔴 |

<br>

---

### 🎯 与单一检测工具的区别

| | statcheck | GRIM test | p-curve app | **VeritasKit** |
|:--|:--:|:--:|:--:|:--:|
| 检测数量 | 1 | 1 | 1 | **10** |
| 交叉验证 | — | — | — | **≥3 信号 = HIGH** |
| 证据链 | — | — | — | **逐项可追溯** |
| 批量审计 | — | — | — | **多篇论文并行** |

> **不是 10 个工具的集合，是一个工具运行 10 条规则。**

<br>

---

### ⚡ 开始使用

```bash
git clone git@github.com:CcXXXXX0630/VeritasKit.git
cd VeritasKit/scripts
python forensics.py --all your_data.csv
```

```text
████████████████████████████████████████
   VeritasKit v1.0 · Audit Report
████████████████████████████████████████

  Benford.......... PASS  (p = 0.42)
  GRIM............. FLAG  (3 of 12 means fail integer check)
  Mass Balance..... PASS  (Δ = 1.8% < 5% threshold)
  p-curve.......... FLAG  (right-skew p < 0.01)
  Statcheck........ PASS
  ...

  VERDICT: REVIEW RECOMMENDED (2 RED, 0 AMBER)
  Evidence chain → audit_report.json
```

<br>

---

### 📁 结构

```
VeritasKit/
├── scripts/
│   ├── forensics.py       ← 10 检测统一入口
│   ├── investigator.py    ← 批量审计编排
│   └── case_builder.py    ← 证据链生成
├── references/             方法论文档
├── templates/              数据模板
├── SKILL.md                Hermes Agent 定义
├── LICENSE                 MIT
└── CITATION.cff            学术引用
```

---

### 📖 引用

```bibtex
@software{VeritasKit,
  title = {VeritasKit: Academic Data Forensics Toolkit},
  author = {CcXXXXX0630},
  year = {2026},
  url = {https://github.com/CcXXXXX0630/VeritasKit}
}
```

### 🙏 致谢

检测方法基于已发表文献：Benford (1938), Brown & Heathers (2017) GRIM, Simonsohn et al. (2014) p-curve, Nuijten et al. (2016) statcheck。  
VeritasKit 的独创贡献在**集成工作流、多信号交叉验证和证据链自动生成**。

### ⚠️ 声明

统计异常 ≠ 学术不端。真实数据偶尔偏离预期。请结合领域知识判断，勿单凭一项检测下结论。

---

<p align="center">
  <sub>MIT License · <a href="https://github.com/CcXXXXX0630">CcXXXXX0630</a></sub>
</p>
