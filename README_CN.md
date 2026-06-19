<p align="right">
  <sub>学术风险预警系统 · v2.2</sub>
</p>

<p align="center">
  <a href="README.md">English</a>
</p>

# TruthTracer

*科学中最伤人的不是"这篇论文造假"——是"支撑这个结论的证据，到这里就断了"。*

---

TruthTracer 找的就是这个断点。七个检测引擎。30+ 种方法。只问一个问题：证据链从哪里开始对不上？

---

## v2.2 新特性

四个新引擎。中文同名作者消歧。模块化架构——每个引擎独立运行。

| 引擎 | 方法数 | 查什么 |
|------|:-----:|--------|
| **统计** | 21 | 数学上不成立的东西——GRIM、Benford、p-curve、SPRITE、statcheck |
| **网络** | 10 | 撤稿史、引文圈、论文工厂签名 |
| **文本** | 6 | 折磨短语（Cabanac 2023）、AI痕迹、香肠切片 |
| **附录** | 5 | 缺失补充材料、不可访问数据、不可复现声明 |
| **引用** | 3 | 引用已撤稿论文、伪造引用、自引滥用 |
| **分布** | 2 | 过度/不足离散、方差异常齐性 |
| **预印本** | 2 | 结局指标切换、摘要版本差异 |

评分器把所有信号融合，带论文类型感知。经济模型自动降 Benford 权重。临床试验自动升生存分析权重。综述跳过统计检测。

---

## 信号严重度

| 级别 | 权重 | 示例 | 含义 |
|------|:----:|------|------|
| 危急 | 3分 | GRIM不可能、均值超量程、事件数>风险人数 | 数学上不可能。近乎确定造假。 |
| 强 | 2分 | Benford偏离>0.03、10+折磨短语、撤稿率>10% | 高度可疑。 |
| 中 | 1分 | 数字偏好、SD齐性、2+折磨短语 | 值得细看。 |
| 弱 | 0.5分 | 取整均匀、1条折磨短语 | 通常是假阳性。 |

铁律：零项危急信号 → 风险上限为中危。只有数学不可能性才构成近乎确定的造假证据。

---

## 同名消歧为什么重要

一个常见中文名，OpenAlex 里可以有 195 篇论文。TruthTracer 按研究领域过滤后剩 124 篇。被筛掉的论文来自完全不相关的领域——同名不同人。不过滤的话，作者档案里 36% 是别人的成果。这种污染会让每个网络信号都不可靠。TruthTracer 在分析前就把这层噪音洗掉。

---

## 真案测试

| 对象 | 已知事实 | 判定 | 关键信号 |
|------|---------|------|---------|
| 已知造假者 | 183篇撤稿 | 高危 | 撤稿率21.4% |
| 诺贝尔奖得主 | 4篇主动撤稿 | 中危 | 0.4%，全为主动撤稿 |
| 干净经济学论文 | 无争议 | 低危 | 经济模型 → Benford降权 |
| 撤稿论文（多作者合谋） | 危急 | 网络引擎捕到合谋模式 |
| 清洁LCA论文 | 无争议 | 低危 | LCA模型识别，正确降权 |
| 常见名研究者 | 无污点 | 低危 | 0撤稿，0折磨短语 |

---

## 上手

```bash
# 全引擎审计
python scripts/scorer.py --stats audit.json --network investigator.json --output report.md

# 纯文本检查
python scripts/text_engine.py check suspicious.txt

# 作者调查
python scripts/network_engine.py investigate "作者姓名" --deep
```

---

## 文件结构

```
scripts/
  scorer.py              证据融合 + 报告生成
  stats_engine.py        21项统计检测
  network_engine.py      10项作者网络信号
  text_engine.py         折磨短语、AI痕迹、香肠切片
  citation_engine.py     引用已撤稿论文、伪造引用
  distribution_engine.py 过度/不足离散检测
  preprint_engine.py     结局切换、摘要差异
  supplement_engine.py   附录完整性审计
  forensics.py           完整统计引擎（详细版）
  investigator.py        完整网络引擎（详细版）
  case_builder.py        遗留案件构建器
  pysprite_vendor.py     GRIM+SPRITE（改编自QuentinAndre/pysprite, MIT）
  extract_pdf.py         PDF提取
```

---

## 引用

```bibtex
@software{TruthTracer,
  title = {TruthTracer: Academic Risk Early-Warning System},
  author = {CcXXXXX0630},
  year = {2026},
  version = {2.2.0},
  url = {https://github.com/CcXXXXX0630/TruthTracer}
}
```

### 致谢

RIGID框架：莫纳什大学 (2024)。折磨短语检测：改编自 Cabanac et al. (2021)。GRIM+SPRITE：改编自 QuentinAndre/pysprite (MIT)。

### 声明

TruthTracer 给出的是风险信号，不是判决书。每份报告都需要人来读。

---

## 星标历史

[![Star History Chart](https://api.star-history.com/svg?repos=CcXXXXX0630/TruthTracer&type=Date)](https://star-history.com/#CcXXXXX0630/TruthTracer&Date)

---

<p align="center">
  <sub>MIT · <a href="https://github.com/CcXXXXX0630">CcXXXXX0630</a></sub>
</p>
