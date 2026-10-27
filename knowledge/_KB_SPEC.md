# 知识卡片落盘规范（Knowledge 轨 · 阶段 2.5 本地适配版）

原版 skill 的 `KB_ROOT` 是 `H:/长红的工作间/蒸馏知识库/`。本机不存在 H 盘，因此本次蒸馏把 KB_ROOT 落在工作区内：

`KB_ROOT = outputs/humans-3.0-peter-nowak/knowledge/`

```
knowledge/
├── _index.md                      # 总索引 + 待跨书比对标记
├── cards/humans-3.0-peter-nowak/
│   ├── _index.md                  # 本书卡片清单
│   └── card-<skill-slug>.md       # 每 skill 一张 L1 原子卡片
├── topics/<主题>.md               # 按主题挂接（8 领域 + 元方法）
├── synthesis/                     # 跨书综合（本次仅占位）
└── bridge/待验证假设.md            # verifiable=true 的可证伪声明
```

## 卡片模板

```markdown
---
card_id: card-<skill-slug>
book: 人类3.0：不断进步升级的人类
book_slug: humans-3.0-peter-nowak
author: 彼得·诺瓦克（Peter Nowak）
chapter: 第X章 <章名>
pages: P<起>-P<止>
tags: [<主题标签>]
confidence: high|medium|low
verifiable: true|false
verified: false
related_skills: [<skill-slug>]
source_quote_page: P<页码>
---

# <原则名>

- **一句话**：……
- **机制**：……（为什么成立，2-4 句）
- **原文锚点**：`"…"`（P123）
- **适用场景**：……
- **失效条件**：……
- **可证伪声明**（verifiable=true 必填）：如果出现 <可观测现象>，则本原则被削弱/推翻。
- **关联**：同主题其它卡片 / 跨书待比对项
```

## 约束

1. 每张卡片必须能回溯到 skill 与原文页码
2. `verifiable=true` 必须写可证伪声明（否则只是格言）
3. 主题挂接：`topics/` 下每行一条 `- [卡片名](../cards/.../card-x.md) — 一句话`
