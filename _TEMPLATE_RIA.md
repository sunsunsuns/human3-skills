# RIA++ 六段模板（仓颉蒸馏 · 阶段 2）

每个技能 = 一个目录 `<slug>/SKILL.md` + `test-prompts.json`。

## SKILL.md 结构

```markdown
---
name: <slug>
slug: <slug>
displayName: <中文名>
description: <触发条件写清楚：当用户……时使用；含中英关键词>
description_zh: <同上，中文>
description_en: <English trigger description>
version: 0.1.0
agent_created: true
author: 仓颉蒸馏（长红版）· 蒸馏自《人类3.0》
source_book: 人类3.0：不断进步升级的人类 / 彼得·诺瓦克 / 电子工业出版社 2016
tags: [人类3.0, 技术趋势, ...]
triggers: [<中文触发词>, <英文触发词>]
---

# <中文名>

> 蒸馏自《人类3.0：不断进步升级的人类》（彼得·诺瓦克，电子工业出版社，2016）第 X 章。

## R — 原文锚点（≤150 字/段）

> "……"（P123）

## I — 骨架（这条知识的机制）

## A1 — 书中案例（锚点）

## A2 — 触发场景（什么时候该用）

## E — 执行步骤（1-2-3，含 if-then）

## B — 边界（不适用 / 失效条件 / 与相邻技能的分工）
```

## 质量红线

1. R 段必须是 OCR 原文照抄（≤150 字），页码可回溯，OCR 明显错字用 `[OCR: 疑为 X]` 标注
2. I 段要解释"为什么"（机制），不是复述
3. E 段必须可执行：有输入、有判断分支、有输出形态
4. B 段必须写清失效条件与相邻技能分工，避免与其他技能抢触发
5. description 必须含具体触发场景，否则不会被调用
6. test-prompts.json ≥5 条，且含"诱饵"（不该触发的请求）
