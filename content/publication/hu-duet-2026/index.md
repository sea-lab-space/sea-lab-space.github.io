---
title: 'DUET: Optimize Token-Budget Allocation for Reinforcement Learning with Verifiable
  Rewards'
authors:
- Haoyu Hu
- Xuandong Zhao
- Xuhai Xu
- Nori Jacoby
date: '2026-09-01'
publishDate: '2026-11-25T06:51:07.856845Z'
publication_types:
- paper-conference
publication: '*Advances in Neural Information Processing Systems*'
abstract: "Reinforcement learning with verifiable rewards (RLVR) generates hundreds
  of thousands of tokens per training step, with rollout generation dominating the
  computational cost. The overall token budget can be controlled along two main dimensions:
  (i) deciding which prompts to allocate rollouts to, and (ii) deciding how long each
  rollout should be. Prior work has generally controlled only one of these dimensions
  at a time. We show that jointly tuning both decisions under a shared compute budget
  improves both reasoning quality and wall-clock training time. We instantiate this
  view as textbfDUal-controlled toktextbfEn allocatextbfTion (DUET), a computationally
  efficient layer over GRPO that uses a lightweight pre-rollout surrogate of prompt
  informativeness to set how many rollouts each prompt receives, and a marker-gated
  abort rule with importance reweighting to set when to stop them. On Qwen3-1.7B trained
  on MATH, DUET outperforms full-budget GRPO and the other three budget-aware baseline
  methods. DUET's advantage further generalizes to other benchmarks across math and
  coding, and is on par with the best baseline on the scientific Q&A domain, while
  also achieving a $1.62times$ wall-clock speedup. More notably, using only 50% of
  the token budget, DUET still outperforms all baseline methods at their full budget,
  achieving an even higher $2.51times$ speedup over full-budget GRPO. We verify the
  high performance of DUET on other backbone LLMs, including Qwen3-4B to 14B and Llama-3.2-3B-Instruct.
  Notably, the gap between DUET and the strongest baseline emphwidens as the budget
  tightens, contrary to the usual pattern in which efficient methods trade off quality
  as compute decreases. More broadly, these results suggest that DUET budget-aware
  control strategies are valuable not only for accelerating training, but also for
  improving the quality of the learning signal. The code and data setup are publicly
  available at https://github.com/Haoyu-Hu/DUET"
links:
- name: arXiv
  url: https://arxiv.org/abs/2605.08441
- name: URL
  url: https://openreview.net/forum?id=N80WSnmidb
---
