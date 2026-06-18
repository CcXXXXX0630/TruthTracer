<p align="right">
  <sub>学术风险预警系统 · v2.1</sub>
</p>

<p align="center">
  <a href="README.md">English</a>
</p>

# TruthTracer

*科学中最伤人的不是"这篇论文造假"——是"支撑这个结论的证据，到这里就断了"。*

---

TruthTracer 找的就是这个断点。它审计研究逻辑、数据、统计、引用网络、可复现性——然后告诉你哪里不对劲。不给结论，只给证据链。像一个审稿人加科研诚信官加调查员的合体，只不过是一段代码。

---

## 里面有什么

三个引擎。31 种方法。不需要 API key。

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
     风险报告（证据可追溯）
```

**统计引擎**（21种方法）。找数学上不可能的东西——GRIM 检验不过、Benford 定律偏离、p-curve 扎堆、SPRITE 不一致、statcheck 重算不对。就那种审稿人半夜盯着表格突然觉得"不对"的事，只不过它自动扫。

**网络引擎**（10种信号）。从 OpenAlex、CrossRef、PubMed 拉数据。撤稿率、引文圈、合著闭包、发稿速度。不用 API key，能上网就行。

**案件构建器**。把信号拼在一起，带点常识。经济学论文自动调低 Benford 权重。临床试验自动调高生存分析权重。两项数学不可能 = 危急。零项 = 最多判到中危。

---

## 风险怎么分

| 等级 | 什么意思 | 怎么办 |
|:------|:--------|:------|
| 危急 | 至少两项数学上不可能 | 拿原始数据。立刻。 |
| 高危 | 一项不可能，或多项强信号 | 申请原始数据，标记统计审查 |
| 中危 | 有异常，但没到不可能 | 问作者，查附录 |
| 低危 | 小毛病 | 正常审稿能逮住 |
| 清洁 | 没发现问题 | 过 |

这个工具最值钱的地方是区分高危和中危。真正有问题的论文，大多数落在高危而不是危急。

---

## 真刀真枪测过

三轮真案验证：

**藤井善隆** —— 史上撤稿最多的研究者，183 篇。测出：高危。撤稿率 21.4%，被撤后还发了 96 篇。网络引擎抓到了统计引擎漏掉的东西：撤稿后的持续发表模式。

**弗朗西斯·阿诺德** —— 2018 年诺贝尔化学奖得主，4 篇主动撤稿。测出：中危。主动撤稿其实是正面信号——说明她自己发现错误自己纠正。工具正确区分了一个造假惯犯和一个敢于认错的科学家。

**一篇干净的经济学论文** —— 无争议。测出：低危。自动识别为"经济模型"，Benford 检测自动折扣。没误报。

---

## 理论根基

TruthTracer 实现了莫纳什大学 2024 年发表的 [RIGID 框架](https://doi.org/10.1016/j.eclinm.2024.102717)——一套科研诚信审计的五原则体系。31 种方法覆盖 RIGID 全部维度。29 种是原创实现。GRIM 和 SPRITE 借用了 QuentinAndre/pysprite（MIT 许可）。

---

## 上手

```bash
# 1. 审计数据
python scripts/forensics.py audit --paper data.json > audit.json

# 2. 调查作者
python scripts/investigator.py investigate "作者姓名" --deep > investigator.json

# 3. 拼起来
python scripts/case_builder.py audit.json investigator.json \
    --text extracted_text.txt --output report.md
```

31 种方法里 29 种只用 Python 标准库，无需 pip install。

---

## 目录结构

```
scripts/
  forensics.py           统计引擎（78 KB）
  investigator.py        网络引擎（36 KB）
  case_builder.py        证据链构建器（19 KB）
  extract_pdf.py         PDF 文本提取
  pysprite_vendor.py     GRIM + SPRITE 实现
examples/                示例审计报告
investigations/          真实案件档案
references/              方法论文档
```

---

## 引用

```bibtex
@software{TruthTracer,
  title = {TruthTracer: Academic Risk Early-Warning System},
  author = {CcXXXXX0630},
  year = {2026},
  url = {https://github.com/CcXXXXX0630/TruthTracer}
}
```

## 声明

TruthTracer 给出的是风险信号，不是判决书。每份报告都需要人来看。

---

## 星标历史

[![Star History Chart](https://api.star-history.com/svg?repos=CcXXXXX0630/TruthTracer&type=Date)](https://star-history.com/#CcXXXXX0630/TruthTracer&Date)

---

<p align="center">
  <sub>MIT · <a href="https://github.com/CcXXXXX0630">CcXXXXX0630</a></sub>
</p>
