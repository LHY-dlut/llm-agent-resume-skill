# LLM / Agent Resume Skill

**用真实机制解释贡献，用可追溯证据约束成果。**

[![Validate skill assets](https://github.com/LHY-dlut/llm-agent-resume-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/LHY-dlut/llm-agent-resume-skill/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

完成一个项目后，用 `$llm-agent-resume` 将已有项目材料整理为中文简历简介：**项目定位 → 个人设计的机制 → 有证据的成果**。支持 RAG、Agent 与后训练项目，并提供独立的事实核对备注。

### 每个项目都能调用：Codex 全局安装

首次安装，在 PowerShell 执行：

```powershell
git clone https://github.com/LHY-dlut/llm-agent-resume-skill.git
$skillRoot = Join-Path $env:USERPROFILE '.codex\skills'
New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null
Copy-Item -LiteralPath '.\llm-agent-resume-skill\skills\llm-agent-resume' -Destination $skillRoot -Recurse
```

如已存在 `llm-agent-resume` 目录，先备份再更新；若设置了 `CODEX_HOME`，安装到该目录下的 `skills`。重新开启 Codex 会话后，在任何项目中使用：

```text
$llm-agent-resume
目标岗位：大模型应用开发实习。
请根据当前项目的 README、实现说明和已有评测记录，写一份能放进简历的项目介绍。
使用 compact 模式。已有信息足够就直接输出；缺少某项收益证据时省略该收益。
只对影响真实性的关键冲突提问，不启动新测试或付费模型调用。
将内部核对备注放在简历正文之外。
```

Claude Code 可将同一个完整 Skill 目录放到 `~/.claude/skills/llm-agent-resume/`，通过 `/llm-agent-resume` 调用；普通聊天可直接使用下方的单文件提示词。

面向 LLM 应用算法、Agent、RAG 与后训练方向的项目简历写作规范。把杂乱笔记转为“底盘层 → 架构层 → 治理层 → 评测层 → 成果与边界”，但先做事实审查；不补造工程能力，不照搬别人的指标。

本仓库提供可复制的 Agent Skills 目录与单文件提示词。不承诺“大厂高命中率”，不代表任何公司的招聘标准；默认不读取私有账号、不运行训练、不发布材料。

## 1. 为什么不是“多接几个 API 就够了”？

一个功能清单只能说明系统会做什么，未必说明失败后会发生什么，也未必说明哪一部分确实是候选人完成的。这个仓库因此优先问：状态如何保存，工具结果如何校验，旧版本证据会不会混入答案，实验条件有没有冻结，修复后如何知道没有退化。

**“底盘优先”是本仓库的叙事选择，不是“底盘永远比算法重要”的招聘定律。** 对应用工程项目，应让运行约束与失败处理可见；对训练算法项目，“底盘”应落到采样—奖励—更新循环、数据隔离与实验可复现性。真实简单的设计，优于未经证据支持的复杂系统标签。Anthropic 的工程经验同样强调按任务需要选择简单、可评估的方案，而不是为了 Agent 化增加复杂度。[技术参考](skills/llm-agent-resume/references/sources.md)

| 阅读层次 | 回答的问题 | 应呈现的证据 |
|---|---|---|
| 底盘 | 系统/实验在什么约束下运行？失败如何处理？ | 本人实现的状态、数据、执行或训练基础 |
| 架构 | 关键数据流/训练流如何组织？ | 模块边界、算法组件与个人增量 |
| 治理 | 如何观察问题并确认修复？ | 实际记录、诊断案例与已执行回归 |
| 评测 | 凭什么相信结论？ | 数据来源、分母、对照条件与重复方式 |
| 成果与边界 | 得到什么，不能推出什么？ | 基线→候选、正确单位、适用范围 |

存在日志不等于形成闭环，完成本地测试不等于工业上线。本文的“工业级范例”指工程表述与实验口径的完整度，不是给项目颁发生产认证。

## 2. 仓库结构

```text
llm-agent-resume-skill/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── .github/workflows/validate.yml
├── skills/
│   ├── llm_agent_resume_prompt.md       # 自动导出的单文件提示词
│   └── llm-agent-resume/                # 可独立复制的 Skill 目录
│       ├── SKILL.md                    # 唯一核心指令源文件
│       ├── agents/openai.yaml          # Codex 展示名称与默认调用示例
│       ├── references/
│       │   ├── evidence-and-metrics.md  # 证据、指标与术语审查
│       │   └── sources.md               # 一手资料及来源边界
│       ├── templates/
│       │   ├── project-intake.md         # 用户事实输入表
│       │   ├── evidence-ledger.md        # 主张台账与指标卡
│       │   └── resume-project.md         # 五段式空白模板
│       └── examples/
│           ├── rag-before-after.md
│           ├── post-training-before-after.md
│           └── demo-metrics.json         # 显式合成的演示数据
├── scripts/export_prompt.py
└── tests/
    ├── test_repo.py                     # 确定性结构与算术检查
    └── behavior-cases.md                # 20 个待实际执行的行为规格
```

核心文件使用带 name/description 的 `SKILL.md`，资源随整个目录携带；单文件版本用于直接粘贴，不把孤立的 Markdown 文件误当成所有客户端都会自动发现的技能。[格式与安装来源](skills/llm-agent-resume/references/sources.md)

## 3. 快速使用

### A. 直接交给 GPT / Codex / Claude

打开 [单文件提示词](skills/llm_agent_resume_prompt.md)，将其正文作为本次任务的执行规范，再附项目材料。支持设置 system/developer 指令的宿主可放入相应位置；普通聊天中粘贴文本或上传文件不会自动改变消息权限。

```text
请按本文件执行项目简历写作。
目标岗位：大模型应用算法 / Agent / 后训练（选择实际方向）。
输入是项目事实，不是已经核验的成稿。
先做 Gap Check。若基线、消融、隔离机制或边界未知，
先问 3–4 个具体问题并等待，不自行补齐。
我确认“没有做”的内容应降级，不要反复追问。
资料如下：
【粘贴真实笔记，或填写 project-intake.md】
```

### B. 安装为目录型 Skill

需复制整个 `skills/llm-agent-resume/`，而不只复制 SKILL.md。以下为首次项目级安装示例，命令从本仓库根目录执行。

Codex：

```bash
mkdir -p .agents/skills
cp -R skills/llm-agent-resume .agents/skills/
```

随后在支持本地 Skills 的 Codex 会话中显式调用 `$llm-agent-resume`。Claude Code 对应的项目路径为 `.claude/skills/llm-agent-resume/`，显式调用 `/llm-agent-resume`。[官方用法与版本说明](skills/llm-agent-resume/references/sources.md)

```bash
mkdir -p .claude/skills
cp -R skills/llm-agent-resume .claude/skills/
```

Windows PowerShell 的 Codex 首次安装示例：

```powershell
New-Item -ItemType Directory -Force .agents/skills | Out-Null
Copy-Item -Recurse -LiteralPath skills/llm-agent-resume -Destination .agents/skills/
```

更新时重新同步整个目录，避免旧模板与新核心混用。本仓库忽略这两处本地安装副本，避免维护重复源文件。不同客户端与账户的功能以官方文档为准；这里未完成跨客户端加载实测。

## 4. 执行工作流

```text
材料输入
   ↓
原子主张台账：贡献归属 / 完成状态 / 来源 / 可写范围
   ↓
Gap Check
   ├── 关键项未知 → 3–4 个具体问题 → 等待用户
   └── 事实明确，或确认未做 → 保留 / 降级 / 删除
                                      ↓
                                五段式项目简介
                                      ↓
                           主张审计 + 独立内部核对
```

以下规则解决模板最容易造成的误导：

| 原草稿容易过度推断的地方 | 本仓库规则 |
|---|---|
| 没有底盘也要凑底盘 | 映射到真实运行/数据/训练基础；没有就明说，不制造 Runtime |
| 所有数字都必须有基线 | 所有收益主张必须有基线；真实交付数量不需要虚构比较 |
| 成果一定要三类指标齐全 | 优先效果、可靠性、效率；缺哪个就不报哪个 |
| 拒答下降即无理由拒答减少 | 需要应答/应拒标签，不能由总体拒答比例推断 |
| 一次配对排除随机性 | 仅降低评估样本差异，仍需说明训练/生成/评审随机性 |
| 累计加模块证明独立贡献 | 称增量对照，结论限于当前组合条件 |
| 有 SSE 就能任务恢复 | 区分连接、事件、计算与副作用语义 |
| 有训练配置就是完成训练 | 分开记录 preflight、正式训练、合并与独立评测 |

详见 [核心执行文件](skills/llm-agent-resume/SKILL.md) 与 [指标审查手册](skills/llm-agent-resume/references/evidence-and-metrics.md)。

### 一次合格的首次响应

```text
已确认：你使用 LangGraph 编排 RAG，并记录了两次拒答比例。
暂不能确认：运行隔离、题单选择、对照条件与拒答标签。

1. 任务取消与旧任务提交在哪校验？重连只回放事件，还是恢复计算？
2. 46 题是预先冻结还是两次共同题？基线、候选版本与原始分母是什么？
3. 两次运行改了哪些因素，各重复几次？是否进行真实策略对照？
4. 评分规则及应答/应拒标签是什么？哪些能力已测试，哪些尚未验证？

暂不能写：自研 Runtime、全链路恢复、错误拒答下降、准确率提升。
```

首次缺项时不同时给“脑补补齐版”。用户明确没有做后，允许输出实现与验收版，而不是永久卡在问答环节。

## 5. 标准空白模板

填报时可以保留占位符；投递终稿必须替换为真实信息或删除相应主张。完整输入字段见 [事实输入表](skills/llm-agent-resume/templates/project-intake.md)。

```text
{{项目名称}}｜{{实际起止时间}}｜{{实际角色}}
技术栈：{{实际使用的语言/运行基础、存储、框架、模型、算法组件}}

项目介绍：面向{{具体场景}}，针对{{已观察的问题}}，构建/扩展{{系统或训练流程}}，支持{{已经实现的目标}}。

- 底盘层：针对{{运行/数据/实验风险}}，在{{具体模块}}实现/扩展{{真实机制}}，支持{{已确认能力}}。
- 架构层：设计{{主要数据流或训练流}}；实现{{本人负责的关键模块}}，并明确{{复用与新增边界}}。
- 治理层：记录{{实际观测字段}}，通过{{实际诊断/异常处理}}处理{{已发生的问题}}；以{{已经执行的回归}}检查修复。
- 评测层：基于{{来源、版本、分割，N 与统计单位}}，进行{{实际对照类型}}，验证{{明确问题}}；控制/记录{{实际实验条件}}。

项目成果：在{{数据范围与协议}}上，相比{{基线版本}}，{{指标}}由{{X 与单位}}变为{{Y 与单位}}，变化{{差值及正确单位}}；{{其他已测指标或已验证交付}}。
边界说明：{{开发回归/单次观测/非等算力/部署范围等关键边界}}；{{不能由现有证据推出的结论}}。
```

无效果基线但有真实交付时，成果写“完成哪些模块、哪些测试与产物”，并说明尚未开展何种评测。不要为了排版完整而添加准确率或成本提升。

## 6. 对比范例一：RAG / Agentic RAG

**来源声明：以下机制与数值来自用户草稿，未独立核验；这是修改示范，不是可直接投递的个人终稿。** 日期与角色不推测。

### 修改前

> 使用 FastAPI 和 LangGraph 开发企业级 RAG，支持上传、检索、问答和引用。自研 Runtime，实现双库强一致和流式断点续跑；拒答率从 71.7% 降到 56.5%，显著提高回答准确率。

### 修改后

使用前提：用户确认下述实现及本人贡献，确认 46 题两个拒答比例同口径；否则必须先追问。

**Agentic RAG 文档问答与回归评测平台｜{{实际时间}}｜{{实际角色}}**

技术栈：Python、MySQL、PostgreSQL/pgvector、FastAPI、LangGraph；BM25、RRF、Cross-Encoder Rerank。

项目介绍：面向企业文档问答，针对索引版本混用、证据追溯困难与任务中断后的结果处理问题，构建包含执行管控、证据检索和失败诊断的 Agentic RAG 平台。

- **底盘层：** 基于双库管理业务状态与向量索引，实现任务租约、取消与过期执行隔离；持久化 SSE 事件，支持事件续订及服务重启后的历史回放。
- **架构层：** 以父子块组织文档，保存出处与版本元数据；搭建 Dense/BM25 双路召回、RRF 融合与重排链路，通过 LangGraph 编排改写、检索、证据评估、生成和核验/拒答分支。
- **治理层：** 设置节点重试边界并留存执行轨迹，追踪引用与文档版本；围绕否定证据误拒、引用协议失效等问题开展定位与修复。
- **评测层：** 在 CRUD-RAG 的 46 题开发回归比较中，留存逐题答案、引用和 AI 审阅冲突记录，分析两次 Dense 运行的拒答分布及失败轨迹。

**项目成果：** 上述两次 Dense 运行记录的拒答率分别为 71.7% 和 56.5%，后次较前次低约 15.2 个百分点；交付文档版本过滤、事件回放与执行轨迹查询能力。

**边界说明：** 该比较是开发阶段观测，不是独立线上质量评估；拒答比例减少不能单独证明错误拒答减少或答案正确率提升，亦不足以归因为某一检索策略。

这里没有把 46 题擅自命名为预先冻结的独立集，也没有认定它是事后交集；应根据真实选题方式补充。现有比例只支持受限观测，不能推导错误拒答或准确率收益。详见 [完整 RAG 范例与四个追问](skills/llm-agent-resume/examples/rag-before-after.md)。

## 7. 对比范例二：GRPO / RLVR / 后训练

**DEMO：下文为完全假设案例，全部数字为合成演示，未实际训练，不属于用户或截图作者，也不是费用估算。** 它展示“怎么写一个证据完整的结果”，而不是提供可以借用的成绩。

假设条件：五个累计配置；同一基座与初始条件；每组固定 1000 个优化步、三个训练种子；同一假想数学保留集 200 题，每题采样 8 次；最终评价固定末步 checkpoint；另外统计开发阈值达到步数与同硬件全流程 GPU-hours。该设计是等步数，不是等算力。

### 修改前

> 从零实现完整 DAPO，加入多个优化模块，解决熵坍缩，准确率提升很多，训练成本降低 35%。

### 修改后（仅合成示范）

**DEMO｜Qwen 数学推理后训练：GRPO 复现与增量对照｜示例时间｜示例角色**

技术栈：Python、PyTorch、Transformers、Qwen2.5-1.5B-Instruct、LoRA；GRPO / DAPO 风格优化。

项目介绍：面向可验证数学推理，围绕组内奖励退化、策略探索不足与长度偏差，构建可记录训练动态和比较优化配置的后训练实验流程。

- **底盘层：** 基于 Transformers 加载模型，自实现采样、组相对优势与参数更新循环；隔离训练/开发/保留数据，并对奖励解析、掩码及异常输入设置校验。
- **架构层：** 在明确不含 KL-loss 的 GRPO 基线中，依次接入 Clip-Higher、Dynamic Sampling、Token-Level Loss 与超长奖励处理，保持可切换的累积实验配置。
- **治理层：** 记录策略熵、诊断 KL、生成长度、筛选前零方差组比例及原始采样量，关联配置与 checkpoint，追踪奖励异常和训练退化现象。
- **评测层：** 固定基座、数据与 1000 个更新步，对五组配置分别运行三个训练种子；在假想 DEMO-MATH-v1 的 200 题保留集上，以每题 8 次采样评估 pass@1/8，并单独统计开发阈值步数和 GPU-hours。

**项目成果（合成演示）：** G4 相比 G0，pass@1 均值由 40.0%→47.0%（+7.0 pp），pass@8 由 62.0%→72.0%（+10.0 pp）；开发阈值步数由 800→520（−35.0%），但完整训练 GPU-hours 由 10.4→11.5（约 +10.6%）。

**边界说明：** 这是等优化步数、非等算力的累积配置比较，反映特定组合下的效果与开销取舍；不能拆解为各技术的独立贡献，也不能声称训练总成本下降。所有数值仅为写法演示。

这组例子故意不隐藏成本劣化：优化步数下降与 GPU-hours 上升可以同时成立。累计配置对照也不等于独立贡献分解。完整假设、逐配置表与种子级合成数字见 [后训练对比范例](skills/llm-agent-resume/examples/post-training-before-after.md)。

真实训练未启动时，不使用这个“已训练版本”：应写数据审计、奖励测试、配置校验等已经完成的内容，并将正式训练与最终评测列为未完成。

## 8. 维护、测试与发布

只修改 `skills/llm-agent-resume/SKILL.md` 维护核心规则，再导出单文件副本。不要分别手改两个核心文件。

```bash
python scripts/export_prompt.py
python scripts/export_prompt.py --check
python -m unittest discover -s tests -v
```

脚本与测试只使用 Python 标准库；建议 Python 3.10 或更高。它们检查源文件/导出一致性、相对文件链接、必备资源、模板结构、README 示例同步及合成数据的算术关系；不会调用模型、连接个人账号、验证用户简历事实或运行训练。

[行为用例](tests/behavior-cases.md) 有 20 个案例，包括指标错归、缺基线、SSE 恢复混淆、仅 dry-run、AI 金标、样本泄漏、示例挪用和材料内指令注入。它们是待实际执行的模型行为验收规格，**不因静态检查通过而自动通过**。

GitHub Actions 已提供同样的静态检查工作流；只有发布后的真实运行记录才能证明该远程 CI 通过。本次没有在 Codex / Claude 中进行端到端行为验证，也没有声称跨模型兼容性已经实测。

更新协议或示例时同步修改 CHANGELOG；修改核心事实规则时，补充相应行为用例。Python 测试检查 README 中模板和范例正文与源文件是否一致，防止多处漂移。

### 发布前的资料边界

仓库默认排除 `private/`、`evidence-private/`、`outputs/`、`.env*` 与运行日志，但 `.gitignore` 不是保密审查，也不会清除已被 Git 跟踪的敏感文件。发布前自行检查将要提交的文件与历史，不把公司资料、真实个人信息或密钥放进范例。

本仓库不包含原始简历截图或 EvoAgent PPT。草稿提到的 PPT 未提供，也没有可核验的“高命中率”统计，所以不把它们写成权威依据或官方背书。技术格式与指标语义的一手资料汇总见 [sources.md](skills/llm-agent-resume/references/sources.md)。

## 9. 许可与适用范围

新增规范、模板与脚本采用 [MIT License](LICENSE)，可开源或自用；第三方引用仍受原许可约束。合成例子只服务于报告规范演示，不能以替换项目名的方式冒充真实经历。

本 Skill 是可审查的工作流，不是事实认证器，也不保证模型永不出错。最后的标准是：**每一句职责能解释本人做了什么，每一个收益能找到比较依据，每一个边界都不被漂亮文案抹掉。**
