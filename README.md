<p align="center">
  <img src="https://img.shields.io/github/stars/CcXXXXX0630/VeritasKit?style=social" alt="Stars">
  <img src="https://img.shields.io/github/license/CcXXXXX0630/VeritasKit" alt="License">
  <img src="https://img.shields.io/badge/Hermes-Agent-6C5CE7" alt="Hermes Agent">
</p>

<h1 align="center">🔍 VeritasKit</h1>
<h3 align="center">让学术数据经得起真相的凝视</h3>
<p align="center"><em>The lie detector for academic data — 10 forensic tests, one verdict.</em></p>

---

## 这是什么？

**VeritasKit** 是一套面向学术论文的统计鉴伪工具包。它不读论文结论，只读数据——用数学法则判断数据是否"太完美以至于不可能真实"。

> 发表于 *Nature* 的数据不一定真。但 Benford 定律会告诉你真相。

## 十项检测

| # | 检测方法 | 攻击目标 | 适用场景 |
|---|---------|---------|---------|
| 1 | **Benford 定律** | 人为编造的数字 | 财务数据、人口统计、实验测量 |
| 2 | **GRIM 检验** | 捏造的均值和样本量 | 心理学、医学小样本研究 |
| 3 | **SPRITE** | 伪造的整数量表数据 | 问卷、Likert量表、评分 |
| 4 | **p-curve** | p-hacking / 选择性报告 | 任何报告多个p值的研究 |
| 5 | **Statcheck** | APA格式统计量错误 | 心理学、社会科学 |
| 6 | **Bootstrap 一致性** | 描述统计不自洽 | 均值/SD/范围矛盾 |
| 7 | **效应量一致性** | 效应量与样本量不匹配 | Meta分析、综述 |
| 8 | **蒙特卡洛参数审计** | 模型参数不合理 | 环境模型、工程模拟 |
| 9 | **Mass Balance** | 物料/能量不守恒 | 环境工程、化工 |
| 10 | **数字偏好分析** | 末位数字分布异常 | 任何人工输入的数据 |

## 快速开始

```bash
# 安装到 Hermes Agent
git clone git@github.com:CcXXXXX0630/VeritasKit.git
cp -r VeritasKit/* ~/.hermes/skills/research/academic-data-forensics/
```

在 Hermes 中加载 skill 后，直接说：

> "用 Benford + GRIM + Bootstrap 审计这篇论文的 Table 2"

## 使用场景

- ✅ **同行评审辅助**：审稿时快速扫描可疑数据
- ✅ **Meta分析前筛查**：识别可能篡改的原始研究  
- ✅ **学术不端调查**：为正式指控提供统计证据链
- ✅ **自检工具**：投稿前确保自己的数据经得起审查

---

## 文件结构

```
├── SKILL.md                    # Hermes Agent skill 定义
├── references/
│   ├── detection-playbook.md   # 十项检测完整操作手册
│   ├── sample-audit-guide.md   # 审计报告模板与判据
│   └── domains/                # 领域专项指南
│       ├── environmental.md
│       ├── medicine.md
│       └── psychology.md
├── scripts/
│   ├── forensics.py            # 核心检测引擎
│   ├── investigator.py         # 批量审计编排
│   ├── case_builder.py         # 证据链生成
│   └── pysprite_vendor.py      # SPRITE 算法实现
└── templates/
    └── paper_data_template.json # 结构化数据录入模板
```

---

## ⚠️ 重要声明

本工具提供**统计证据**而非法律证据。检测到异常 ≠ 证明造假。真实数据偶尔也会偏离预期模式。请始终结合上下文判断，并在做出指控前寻求领域专家验证。

---

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=CcXXXXX0630/VeritasKit&type=Date)](https://star-history.com/#CcXXXXX0630/VeritasKit&Date)

---

<p align="center">
  <sub>Created with ❤️ by <a href="https://github.com/CcXXXXX0630">CcXXXXX0630</a> · Powered by <a href="https://hermes-agent.nousresearch.com">Hermes Agent</a></sub>
</p>
