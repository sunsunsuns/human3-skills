# Knowledge 轨总索引（KB_ROOT）

> 本书蒸馏的知识卡片库。`KB_ROOT` 原版为 `H:/长红的工作间/蒸馏知识库/`，本机无 H 盘，已适配至本目录。
> 书籍：《人类3.0：不断进步升级的人类》/ 彼得·诺瓦克 / 电子工业出版社 2016 / 蒸馏自 229 页扫描件 OCR。

## 结构

```
knowledge/
├── _index.md                       ← 本文件
├── cards/humans-3.0-peter-nowak/   ← 7 张 L1 原子卡片
│   └── _index.md
├── topics/                         ← 按主题挂接
│   ├── 技术评估与预测.md
│   ├── 关系隐私与幸福.md
│   └── 合作制度与变迁.md
├── synthesis/                      ← 跨书综合（首本书，暂无）
└── bridge/待验证假设.md             ← verifiable=true 的可证伪声明
```

## 卡片清单（7/7）

| 卡片 | 主题 | confidence | verifiable |
|---|---|---|---|
| [新问题必须小于旧问题](./cards/humans-3.0-peter-nowak/card-humans30-tech-net-impact.md) | 技术评估 | high | ✅ |
| [翻倍次数替代完成百分比](./cards/humans-3.0-peter-nowak/card-humans30-exponential-forecast.md) | 技术预测 | high | ✅ |
| [正题—反题—合题：不选边](./cards/humans-3.0-peter-nowak/card-humans30-dual-track-dialectic.md) | 社会变迁 | medium | ✖（方法框架） |
| [利他只在相关性圈内扩](./cards/humans-3.0-peter-nowak/card-humans30-nonzero-cooperation.md) | 博弈与合作 | high | ✅ |
| [收入与幸福：横向成立纵向不成立](./cards/humans-3.0-peter-nowak/card-humans30-happiness-baseline.md) | 幸福 | high | ✅ |
| [连接扩张不加深关系；隐私越稀缺越值钱](./cards/humans-3.0-peter-nowak/card-humans30-individualism-tradeoff.md) | 关系/隐私 | high | ✅ |
| [八领域扫描 + 布拉戈基线 + 四问收敛](./cards/humans-3.0-peter-nowak/card-humans30-domain-scan.md) | 全书法 | high | ✖（方法框架） |

## 待跨书比对（L3 标记）

- 与《非零：人类命运的逻辑》（罗伯特·怀特）的"非零和"论述比对：本书引用了该书，可核对"合作模式成为主流"的论证强度。
- 与《奇点临近》（库兹韦尔）的时点预测比对：本书引用 2045，但作者本人对时点持保留态度。
- 与丹尼尔·卡尼曼/伊斯特林原论文的幸福感数据比对：本书为二手综述，需回原始研究校准。

## 使用方式

1. **检索**：按主题文件（topics/）找相关卡片，再点进卡片看机制与失效条件。
2. **比对**：跨书比对时在 `synthesis/` 新建条目，引用两张以上卡片。
3. **验证**：`verifiable: true` 的卡片，其假设已同步到 `bridge/待验证假设.md`。
