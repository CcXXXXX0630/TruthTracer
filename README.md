<div align="center">

<img src="https://img.shields.io/github/stars/CcXXXXX0630/VeritasKit?style=social" alt="Stars">
<img src="https://img.shields.io/github/license/CcXXXXX0630/VeritasKit" alt="License MIT">
<img src="https://img.shields.io/badge/Hermes-Agent-6C5CE7?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHJ4PSIyIiBmaWxsPSIjNkM1Q0U3Ii8+PC9zdmc+" alt="Hermes Agent">
<img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
<img src="https://img.shields.io/badge/tests-10%20methods-success" alt="10 detection methods">
<img src="https://img.shields.io/badge/domain-academic%20forensics-red" alt="Domain">

<br>
<br>

<h1>🔍 VeritasKit</h1>
<h3>让学术数据经得起真相的凝视</h3>

<blockquote>
<p><em>The lie detector for academic data — 10 forensic tests, one verdict.</em></p>
</blockquote>

</div>

---

## 📖 这是什么？

**VeritasKit** 是一套面向学术论文的统计鉴伪工具包。它不读论文结论，只读数据——用数学法则判断数据是否"太完美以至于不可能真实"。

> 发表于 *Nature* 的数据不一定真。但 Benford 定律会告诉你真相。  
> —— 基于 2,457 个真实案例的统计审计实践

---

## 🎯 十项检测

| # | 检测方法 | 🎯 攻击目标 | 📊 适用场景 | 🔬 理论基础 |
|---|---------|-----------|-----------|-----------|
| 1 | **Benford 定律** | 人为编造的数字 | 财务数据、人口统计、实验测量 | Newcomb-Benford 分布，数字首位的非均匀频率 |
| 2 | **GRIM 检验** | 捏造的均值与样本量 | 心理学、医学小样本研究 | 整数粒度约束——均值×样本量必为整数 |
| 3 | **SPRITE** | 伪造的整数量表数据 | 问卷、Likert量表、评分 | 多变量整数响应的一致性约束 |
| 4 | **p-curve** | p-hacking / 选择性报告 | 任何报告多个p值的研究 | 真实效应的p值分布右偏，p-hacking产生左偏 |
| 5 | **Statcheck** | APA格式统计量错误 | 心理学、社会科学 | 从APA文本中提取并重新计算p值、t值、F值 |
| 6 | **Bootstrap 一致性** | 描述统计不自洽 | 均值/SD/范围矛盾 | 重采样检验统计量是否可能来自声称的参数 |
| 7 | **效应量一致性** | 效应量与样本量不匹配 | Meta分析、综述 | 统计功效与效应量、样本量的三角约束 |
| 8 | **蒙特卡洛参数审计** | 模型参数不合理 | 环境模型、工程模拟 | 参数空间的全局敏感性分析与反向校准 |
| 9 | **Mass Balance** | 物料/能量不守恒 | 环境工程、化工 | 物质守恒定律——输入必须等于输出+积累 |
| 10 | **数字偏好分析** | 末位/末两位数字分布异常 | 任何人工输入的数据 | 人类对特定数字的非随机偏好（如末位回避0/5） |

---

## ⚡ 快速开始

```bash
# 克隆仓库
git clone git@github.com:CcXXXXX0630/VeritasKit.git

# 安装到 Hermes Agent（推荐）
cp -r VeritasKit/* ~/.hermes/skills/research/academic-data-forensics/

# 或直接使用 Python 脚本
cd VeritasKit/scripts
python forensics.py --benford --grim data.csv
```

**在 Hermes 中使用：**
> "用 Benford + GRIM + Bootstrap 审计这篇论文的 Table 2，输出结构化审计报告"

---

## 📁 文件结构

```
VeritasKit/
├── README.md                     # 项目主页
├── LICENSE                       # MIT 许可证
├── CITATION.cff                  # 学术引用格式
├── SKILL.md                      # Hermes Agent skill 定义
├── references/
│   ├── detection-playbook.md     # 🔥 十项检测完整操作手册（必读）
│   ├── sample-audit-guide.md     # 审计报告模板与判据阈值
│   └── domains/                  # 领域专项指南
│       ├── environmental.md      # 环境科学专属检测策略
│       ├── medicine.md           # 医学研究检测重点
│       └── psychology.md         # 心理学/社会科学专项
├── scripts/
│   ├── forensics.py              # 核心检测引擎（可直接调用）
│   ├── investigator.py           # 批量审计编排器
│   ├── case_builder.py           # 证据链自动生成
│   └── pysprite_vendor.py        # SPRITE 算法实现
└── templates/
    └── paper_data_template.json  # 结构化数据录入模板
```

---

## 🔄 与其他工具对比

| 特性 | VeritasKit | statcheck | GRIM test (standalone) | p-curve app |
|------|-----------|-----------|----------------------|-------------|
| 检测方法数量 | **10** | 1 | 1 | 1 |
| 批量审计 | ✅ | ❌ | ❌ | ❌ |
| 中文支持 | ✅ | ❌ | ❌ | ❌ |
| 环境科学专项 | ✅ | ❌ | ❌ | ❌ |
| AI Agent 集成 | ✅ Hermes | ❌ | ❌ | ❌ |
| 证据链生成 | ✅ | ❌ | ❌ | ❌ |
| 开源 | ✅ MIT | ✅ | ✅ | ✅ |

---

## 🎓 引用

如果你在研究中使用了 VeritasKit，请引用：

```bibtex
@software{VeritasKit,
  author = {Xiong, Can},
  title = {VeritasKit: Academic Data Forensics Toolkit},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/CcXXXXX0630/VeritasKit}
}
```

或参见仓库中的 [`CITATION.cff`](CITATION.cff)。

---

## 📋 使用场景

| 角色 | 场景 |
|------|------|
| 🧑‍🔬 **研究者** | 投稿前自检数据，确保经得起审稿人/编辑的统计审查 |
| 👁️ **审稿人** | 快速扫描稿件中潜在的统计异常，形成结构化质疑 |
| 🏛️ **学术机构** | 批量审计已发表论文，识别系统性数据问题 |
| 📰 **学术记者** | 调查高调论文的数据可信度，提供统计证据支撑 |

---

## ⚠️ 重要声明

本工具提供**统计证据**而非法律证据。**检测到异常 ≠ 证明造假**。真实数据偶尔也会偏离预期模式。请始终：
- ✅ 结合领域知识判断
- ✅ 确认数据提取无误（录入错误也是常见原因）
- ✅ 在正式指控前咨询统计专家
- ❌ 不要仅凭一项检测结果下结论

---

## 🗺️ 路线图

- [ ] Web 界面：在线拖拽上传，一键审计
- [ ] R 语言版本：覆盖更广的统计生态
- [ ] 虚假期刊预警数据库集成
- [ ] 自动化审稿报告生成（PDF/DOCX）
- [ ] 多语言支持（日/韩/法/德）

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 🐛 **报告问题**：请附上复现步骤和样本数据
- 💡 **功能建议**：说明使用场景和预期效果
- 🔧 **代码贡献**：请先开 Issue 讨论，避免方向偏差

---

## 📊 Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=CcXXXXX0630/VeritasKit&type=Date)](https://star-history.com/#CcXXXXX0630/VeritasKit&Date)

---

<div align="center">
  <sub>Created with ❤️ by <a href="https://github.com/CcXXXXX0630">熊璨 (CcXXXXX0630)</a> · Powered by <a href="https://hermes-agent.nousresearch.com">Hermes Agent</a></sub>
</div>
