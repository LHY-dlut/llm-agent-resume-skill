# 公开参考与来源边界

整理日期：2026-10-08。以下资料用于核对格式、接口与技术语义，**不证明任何人的项目确实实现过相关功能，也不证明某类简历有更高命中率**。下列链接为公开一手资料；本仓库未复跑论文实验。

## 格式与使用

**S1 — Agent Skills Specification**  
https://agentskills.io/specification  
用于：目录中的 `SKILL.md`、YAML 元数据、name/description 与按需资源约定。本仓库选择 `skills/llm-agent-resume/` 为可独立复制的技能目录。普通 Markdown 文件也可作提示词，但不自动等于可发现的原生 Skill。

**S2 — OpenAI：Build skills**  
https://developers.openai.com/codex/skills/  
访问时重定向至 https://learn.chatgpt.com/docs/build-skills 。用于：Codex 的 `.agents/skills/` 本地目录与显式技能调用。工具版本、宿主环境与账户功能可能变化；不承诺所有产品或账户支持同一安装方法。

**S3 — Claude Code：Extend Claude with skills**  
https://code.claude.com/docs/en/skills  
用于：Claude Code 的 `.claude/skills/<name>/SKILL.md` 项目级安装与技能调用。仓库根部的 `skills/` 本身不是对所有客户端都通用的自动发现路径。

## 技术语义

**S4 — WHATWG HTML Standard：Server-sent events**  
https://html.spec.whatwg.org/multipage/server-sent-events.html  
用于：EventSource 重连、事件 ID 与 Last-Event-ID。业务状态恢复、服务端事件持久化和外部副作用去重不由 SSE 协议自动保证。

**S5 — LangGraph：Persistence**  
https://docs.langchain.com/oss/python/langgraph/persistence  
用于：持久状态与检查点；内存检查点不跨进程重启保存。项目是否真的接入持久化存储，仍需确认其具体配置和执行行为。

**S6 — DAPO: An Open-Source LLM Reinforcement Learning System at Scale**  
https://arxiv.org/html/2503.14476v1  
用于：Clip-Higher、Dynamic Sampling、Token-Level Policy Gradient Loss、Overlong Reward Shaping；该参考版本移除 KL 惩罚项。不要把 KL 监控误写成 DAPO 必含的 loss。论文讨论的采样、步数与时间关系，不可直接当作某个复现项目的测量结果。

**S7 — OpenAI HumanEval：pass@k 实现**  
https://github.com/openai/human-eval/blob/master/human_eval/evaluation.py  
相关论文：https://arxiv.org/abs/2107.03374  
用于：基于每题 n 个样本与 c 个成功样本的 pass@k 估计。数学任务需要另行说明答案核验器；本仓库的演示数据不是该基准结果。

**S8 — Anthropic：Building effective agents**  
https://www.anthropic.com/engineering/building-effective-agents  
用于：明确工作流与自主 Agent 的区别，强调按任务选择简单、透明、可评估的设计。本文没有将该资料解释为字节、阿里或腾讯的招聘标准。

## 关于 EvoAgent 与输入范例

用户草稿提到的“EvoAgent PPT”未随本次请求提供。因此，本仓库保留其表达的工程组织思路，**不声称已核验该 PPT，不把它作为可追溯学术来源**。

公开资料中存在不同的 EvoAgent 项目，例如：

**S9 — EvoAgent: Towards Automatic Multi-Agent Generation via Evolutionary Algorithms**  
https://aclanthology.org/2025.naacl-long.315/  
这是多智能体演化生成工作；不能仅凭同名确认它就是草稿所指 PPT。

**S10 — EvoAgent: An Evolvable Agent Framework with Skill Learning and Multi-Agent Delegation**  
https://arxiv.org/abs/2604.20133  
这是另一同名工作；列出只用于说明名称不唯一，不表示已将其结论纳入本规范。

RAG 范例中的 46、71.7%、56.5% 来自用户提供的草稿，而非本仓库运行产生。其选择规则、分母与运行条件未由本仓库独立核验。后训练范例中的数值是显式假设数据，只用于演示完整的报告口径，不是截图作者、用户或论文的结果。

原始简历截图与未提供的 PPT 不随仓库分发。仓库许可证仅适用于本仓库新增的规范、模板与脚本；第三方资料仍受各自的许可或权利约束。

## CI 配置参考

**S11 — GitHub 官方 Actions**  
https://github.com/actions/checkout  
https://github.com/actions/setup-python  
整理时官方 README 的示例使用 v7。工作流只申请 contents: read，关闭 checkout 凭据持久化。远程执行尚未发生；本地检查结果不能替代 GitHub Actions 运行记录。
