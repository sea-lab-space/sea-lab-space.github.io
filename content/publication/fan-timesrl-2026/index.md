---
title: 'TimeSRL: Generalizable Time-Series Behavioral Modeling via Semantic RL-Tuned
  LLMs – A Case Study in Mental Health'
authors:
- Yuang Fan
- Lilin Xu
- Millie Mengyuan Wu
- Jingping Nie
- Qingyu Chen
- Yuzhe Yang
- Zhuo Zhang
- Xin Liu
- Subigya Nepal
- Xiaofan Jiang
- Xuhai Xu
date: '2026-01-01'
publishDate: '2026-11-25T06:51:07.839770Z'
publication_types:
- article-journal
publication: '*Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous
  Technologies*'
doi: 10.48550/arXiv.2605.21295
abstract: Longitudinal passive sensing enables continuous health prediction, yet models
  often fail under cross-dataset distribution shifts. Traditional ML overfits cohort-specific
  artifacts, while Large Language Models (LLMs) struggle to reason reliably over long,
  heterogeneous time-series. We introduce TimeSRL, a two-stage LLM framework that
  routes predictions through an explicit semantic bottleneck. The model first abstracts
  raw signals into high-level natural language, then predicts behavioral outcomes
  from these abstractions alone. This forces the model to reason over semantic concepts
  that we argue generalize better than raw numbers. We optimize this process end-to-end
  using Group Relative Policy Optimization (GRPO) with Reinforcement Learning from
  Verifiable Rewards (RLVR), learning outcome-aligned abstractions without gold intermediate
  annotations. Instantiated on mental-health prediction, TimeSRL achieves state-of-the-art
  performance on a benchmark designed to stress-test cross-cohort generalization under
  a rigorous leave-one-dataset-out (LOSO) protocol, reducing mean absolute error (MAE)
  over strong non-LLM ML and LLM baselines by 3.1--10.1% and 9.5--44.1% for anxiety,
  and 3.2--9.6% and 27.4--57.6% for depression (all $p$s<0.05). TimeSRL significantly
  outperforms prior methods in cross-benchmark transfer across different sensing pipelines,
  rivaling its own within-domain performance without target-domain fine-tuning. These
  results demonstrate that semantic abstractions are reusable and point to a new direction
  for generalizable behavior modeling via RL-tuned LLMs.
links:
- name: arXiv
  url: https://arxiv.org/abs/2605.21295
- name: URL
  url: https://arxiv.org/abs/2605.21295
directions:
  - human-centered-health-foundation-models
selected: true
highlight: human-centered-health-foundation-models
highlight_rank: 1
---
