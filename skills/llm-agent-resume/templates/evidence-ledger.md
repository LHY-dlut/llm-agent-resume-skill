# 事实台账与指标卡

## 1. 主张台账

| ID | 原始主张 | 本人贡献 | 完成状态 | 证据类型 | 来源/位置 | 适用范围与冲突 | 写入决定 |
|---|---|---|---|---|---|---|---|
| C01 | {{原子主张}} | {{复用/扩展/实现/参与等}} | {{已实现/已测/未知等}} | {{用户陈述/已读取/已复跑/计算/未知}} | {{来源}} | {{边界}} | {{保留/降级/追问/删除}} |

相同主张的不同版本保留修订记录；不能覆盖不利结果而不记录原因。证据类型不是个人可信度评分，只表示助手实际看到了什么。

## 2. 指标卡

```text
metric_id:
claim_ids:
metric_name:
metric_definition:
direction: higher_is_better / lower_is_better / descriptive
unit:
denominator:
dataset_source_and_version:
split_and_selection_rule:
sample_count:
statistical_unit:
baseline_version:
baseline_value:
candidate_version:
candidate_value:
controlled_conditions:
changed_factors:
training_seeds:
generation_repeats:
judge_repeats:
scorer_and_version:
failure_and_exclusion_policy:
aggregation_and_variability:
evidence_type:
evidence_location:
allowed_interpretation:
forbidden_extrapolation:
```

缺失值写 unknown，不用零代替。只有数据规模或测试数量等交付事实时，不套比较性指标卡。

## 3. 数值派生记录

```text
原始数值与精度：
计算公式：
计算结果与单位：
是否基于四舍五入值：
是否需要约数符号：
是否有样本量/口径变化：
```

若原始比例已四舍五入，不反推精确计数。能够计算两数差值，不意味着比较具有因果解释。

## 4. 终稿审计

正文句子 → 对应 Cxx：
删除或降级的主张及原因：
仍为用户陈述、未独立核验的重点：
最关键的补证事项：
是否可以作为终稿：是 / 否（未知占位或重要冲突未解决时为否）
