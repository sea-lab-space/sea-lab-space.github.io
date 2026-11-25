---
title: Capable language models can outgrow the benefits of collaboration
authors:
- Yubin Kim
- Ken Gu
- Chanwoo Park
- Chunjong Park
- Samuel Schmidgall
- A Ali Heydari
- Yao Yan
- Zhihan Zhang
- Yuchen Zhuang
- Yun Liu
- Mark Malhotra
- Paul Pu Liang
- Hae Won Park
- Yuzhe Yang
- Xuhai Xu
- Yilun Du
- Shwetak Patel
- Tim Althoff
- Daniel McDuff
- Xin Liu
date: '2026-07-01'
publishDate: '2026-11-25T06:51:07.834281Z'
publication_types:
- article-journal
publication: '*Nature Machine Intelligence*'
doi: 10.1038/s42256-026-01268-y
abstract: Agents, language model-based systems that can reason, plan and act with
  tools to accomplish tasks, are widely deployed, yet it remains unclear when multi-agent
  coordination outperforms a strong single agent. Here we conduct a controlled experiment
  that holds task prompts, tools and compute budgets constant while varying only coordination
  structure and model capability. Across 260 configurations spanning six benchmarks,
  five architectures and three LLM families, we derive a predictive model using empirical
  coordination metrics. Across benchmarks, single-agent baseline performance emerges
  as the most robust predictor of whether coordination improves or decreases performance.
  In particular, we identify an empirical capability-saturation threshold beyond which
  additional agents are unlikely to improve performance. This threshold correctly
  predicts the effect of multi-agent coordination on performance in 94% of validation
  configurations on SWE-bench Verified and Terminal-Bench. We therefore interpret
  this threshold as a practical selection rule rather than a universal scaling principle.
  A second effect, baseline-scaled error amplification, survives cluster-robust inference
  (Probust = 0.030) and supports the failure-mode taxonomy. The fitted model achieves
  cross-validated R2 = 0.373 (0.413 with a task-grounded capability metric) and selects
  the best architecture in 87% of held-out configurations. These results provide a
  quantitative framework for within-domain architecture selection and for estimating
  when multi-agent coordination is likely to improve performance or add overhead.
links:
- name: arXiv
  url: https://arxiv.org/abs/2512.08296
- name: URL
  url: https://www.nature.com/articles/s42256-026-01268-y
directions:
  - personal-health-agents
selected: true
highlight: personal-health-agents
highlight_rank: 3
---
