# 《人类3.0》技能包 · Humans 3.0 Skills

> 把一本 229 页的技术趋势书，蒸馏成 **7 个可被 AI Agent 调用的技能**。
> 蒸馏自 **《人类3.0：不断进步升级的人类》**（[加] 彼得·诺瓦克 著 / 杨煜东 译 / 电子工业出版社 2016）。
> 方法：仓颉蒸馏流水线（阶段 0-5）· RIA++ 六段式 · 三重验证 · Knowledge 轨卡片

## 这是什么

这本书的主线是：**生物进化已近乎停滞，技术进化在指数上升，人类正在变成"3.0 版"——竞争与和谐的综合体，而且是第一次自知自己已经不同。**

本仓库不搬运书摘，而是把书里可迁移的**判断框架**整理成 Agent 能直接调用的技能：每个技能都有原文锚点（R）、机制解释（I）、书中案例（A1）、触发场景（A2）、执行步骤（E）、边界（B），并附带含诱饵的触发测试用例。

## 7 个技能

| 技能 | 它回答什么问题 |
|---|---|
| [八领域扫描与布拉戈基线法](humans30-domain-scan/SKILL.md) | 宏大议题从哪入手？帮我定位领域、算增量、分派技能 |
| [技术净收益评估](humans30-tech-net-impact/SKILL.md) | 这项技术值不值得做/放行？风险怎么分级？红线在哪？ |
| [指数外推与进度自检](humans30-exponential-forecast/SKILL.md) | 什么时候能成熟？做了两年才 10%，该加码还是止损？ |
| [双轨辩证法诊断](humans30-dual-track-dialectic/SKILL.md) | 技术既连接又撕裂，该选边还是找综合？ |
| [非零和转化与利他半径](humans30-nonzero-cooperation/SKILL.md) | 该硬刚还是合作？怎么让人愿意合作？ |
| [幸福基线与增量诊断](humans30-happiness-baseline/SKILL.md) | 涨薪没效果？满意度调研该怎么设计？ |
| [个人主义红利与连接成本计价](humans30-individualism-tradeoff/SKILL.md) | 朋友多了反而孤独？远程办公的孤立怎么算？隐私值多少？ |

## 安装

技能就是"带 YAML frontmatter 的 SKILL.md 目录"。把 `humans30-*` 目录复制到你所用的 Agent 的技能目录即可。

```powershell
# Windows：以 DSH / 兼容 ~/.dsh/skills 的 Agent 为例
git clone <this-repo> humans-3.0-skills
Copy-Item -Recurse -Force humans-3.0-skills\humans30-* "$env:USERPROFILE\.dsh\skills"
```

```bash
# macOS / Linux
git clone <this-repo> humans-3.0-skills
cp -r humans-3.0-skills/humans30-* ~/.dsh/skills/
```

> 若你的 Agent 使用其他技能目录（如 `~/.claude/skills`），换成对应路径即可，SKILL.md 格式兼容。

## 用法示例

```
用户：AI 会怎么改变教育？帮我做个全景分析。
→ 触发 humans30-domain-scan：定位到 教育 = 工作 + 关系 + 幸福 + 经济 四域，
  用布拉戈基线算增量，按四问收敛，再路由给专门技能。

用户：我们团队今年涨薪 15%，但满意度调查跟去年一模一样，钱是不是白花了？
→ 触发 humans30-happiness-baseline：伊斯特林悖论 + 基线/增量定位。

用户：这个项目做了两年才完成 10%，现在该止损还是加码？
→ 触发 humans30-exponential-forecast：7 次翻倍法 + 加速因素检查。
```

每个技能目录里的 `test-prompts.json` 有 5–9 条测试用例（含 3–4 条诱饵），可用于验证你的 Agent 是否在正确时机触发。

## 蒸馏过程（可追溯）

| 阶段 | 做了什么 | 产物 |
|---|---|---|
| 输入处理 | 229 页扫描件 PDF（无文字层）→ 提取页图 → Windows OCR（zh-Hans-CN）→ 27.2 万字符，页级可回溯 | `tools/` 脚本 |
| 0 整书理解 | 通读全书，提取问题链、核心概念、八领域地图、作者方法论 | [BOOK_OVERVIEW.md](BOOK_OVERVIEW.md) |
| 1 五路提取 | 4 路并行读全文，提取 FRAME/PRINCIPLE/CHECKLIST/CASE/COUNTER/TERM | [candidates/](candidates/) · **219 条候选** |
| 1.5 三重验证 | V1 跨域性 × V2 预测力 × V3 独特性 | [VALIDATION.md](candidates/VALIDATION.md) · 41 条核心单元 |
| 2 RIA++ 构造 | 每个技能六段：R/I/A1/A2/E/B | `humans30-*/SKILL.md` |
| 2.5 Knowledge 轨 | 每个技能配一张 L1 知识卡片 + 主题挂接 + 待验证假设 | [knowledge/](knowledge/) |
| 3 关联索引 | 技能引用图 + 跨链校验 | [INDEX.md](INDEX.md) |
| 4 压力测试 | 每技能 5–9 条 prompt，含诱饵 | `humans30-*/test-prompts.json` |
| 5 发布预检 | 主题分类 + 细节层预检 + 渐进发布计划 | [PUBLISH_REPORT.md](PUBLISH_REPORT.md) |

## 目录结构

```
.
├── README.md                    ← 你正在看的
├── NOTICE.md                    ← 版权与来源说明（重要）
├── BOOK_OVERVIEW.md             ← 整书理解
├── INDEX.md                     ← 技能索引 + 引用图
├── PUBLISH_REPORT.md            ← 发布预检记录
├── _TEMPLATE_RIA.md             ← RIA++ 模板
├── humans30-*/                  ← 7 个技能（SKILL.md + test-prompts.json）
├── knowledge/                   ← Knowledge 轨：卡片 / 主题 / 待验证假设
├── candidates/                  ← 提取与验证记录（219 条候选，不含书籍全文）
├── scripts/check_links.py       ← 质量闸门脚本
└── tools/                       ← 复现用 OCR 流水线（extract_pages / ocr / merge / make_chunks）
```

## 质量闸门

```bash
python scripts/check_links.py
# skills found: 7
# knowledge cards: 7
# warnings: 0
# errors: 0
```

检查项：frontmatter 必填字段、六段结构完整、R 段 ≤150 字、跨链无孤儿、每个技能 test-prompts 含诱饵、卡片 related_skills 有效。

## 复现

原书 PDF 不在本仓库中（版权原因），复现需自备扫描件：

```bash
python tools/extract_pages.py "path/to/book.pdf" _book/pages
powershell -File tools/ocr.ps1 -Start 1 -End 229      # Windows OCR (zh-Hans-CN)
python tools/merge.py                                  # 合并为 book.txt（含 P 页码标记）
python tools/make_chunks.py                            # 切成 4 块供并行提取
```

然后按 `candidates/_EXTRACT_SPEC.md` 的规范做五路提取，再走三重验证与 RIA++ 构造。

## 版权

书的内容版权归原作者与出版方所有。本仓库只保留 ≤150 字/段的引文用于溯源，**不含书籍全文、OCR 全文与页图**。详见 [NOTICE.md](NOTICE.md)。

技能与文字整理部分：仅供学习研究使用，未授权商用；如需引用请注明出处。
