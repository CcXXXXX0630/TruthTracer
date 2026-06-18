# VeritasKit

**学术数据鉴伪工具包 · Academic Data Forensics Toolkit**

> 不是语法检查器，不是查重软件——VeritasKit 做的是统计学家审稿时在脑子里做的事：用数学法则检验数据的内在一致性。

---

## 为什么需要这个工具？

学术造假检测长期依赖人工经验——审稿人凭直觉觉得"这数据不太对"，但说不清哪里不对。VeritasKit 把这种直觉变成了可复现的统计检验。

与单一检测工具（statcheck 只查 APA 格式、GRIM 只查均值粒度）不同，VeritasKit 提供 **10 项检测的集成工作流**——一次审计覆盖从数据输入到统计推断的完整链路。

| 检测 | 查什么 | 信号强度 |
|------|--------|---------|
| Benford 定律 | 人为编造的数字首位分布异常 | ★★★ |
| GRIM 检验 | 均值×样本量≠整数 | ★★★ |
| SPRITE | 整数量表多变量不一致 | ★★ |
| p-curve | p-hacking 选择性报告 | ★★☆ |
| Statcheck | APA 统计量重算不匹配 | ★★ |
| Bootstrap 一致性 | 描述统计内部矛盾 | ★★ |
| 效应量一致性 | 效应量-样本量-功效三角不闭合 | ★☆ |
| 参数审计 | 模型参数分布不合理 | ★★ |
| Mass Balance | 物料/能量不守恒 | ★★★ |
| 数字偏好 | 末位数字非均匀分布 | ★☆ |

---

## 方法论特色

**不是黑箱。** 每项检测输出可审计的中间结果——原始数据→检测统计量→判定阈值→证据链，全程可追溯。

**不是指控工具。** 多信号交叉验证（≥3 项 RED FLAG 才标记为 HIGH），降低假阳性。

---

## 安装

```bash
git clone git@github.com:CcXXXXX0630/VeritasKit.git
cp -r VeritasKit/* ~/.hermes/skills/research/academic-data-forensics/
```

Python 脚本可独立使用：
```bash
cd VeritasKit/scripts
python forensics.py --benford --grim --bootstrap your_data.csv
```

---

## 文件结构

```
├── SKILL.md            Hermes Agent skill 定义
├── scripts/            核心检测引擎
│   ├── forensics.py    10 项检测统一入口
│   ├── investigator.py 批量审计编排
│   └── case_builder.py 证据链生成
├── references/         方法论文档
└── templates/          数据模板
```

---

## 引用

```bibtex
@software{VeritasKit,
  author = {CcXXXXX0630},
  title = {VeritasKit: Academic Data Forensics Toolkit},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/CcXXXXX0630/VeritasKit}
}
```

## 致谢

部分检测方法基于已发表的统计检验文献（Benford 1938, Brown & Heathers 2017 GRIM test, Simonsohn et al. 2014 p-curve, Nuijten et al. 2016 statcheck）。VeritasKit 的独创贡献在于**集成工作流、证据链生成和批量审计编排**。

## 许可证

MIT · [CcXXXXX0630](https://github.com/CcXXXXX0630)
