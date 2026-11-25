---
title: 'RADAR: Benchmarking Language Models on Imperfect Tabular Data'
authors:
- Ken Gu
- Zhihan Zhang
- Kate Lin
- Yuwei Zhang
- Akshay Paruchuri
- Hong Yu
- Mehran Kazemi
- Kumar Ayush
- A Ali Heydari
- Maxwell A Xu
- Girish Narayanswamy
- Yun Liu
- Ming-Zher Poh
- Yuzhe Yang
- Mark Malhotra
- Shwetak Patel
- Hamid Palangi
- Xuhai Xu
- Daniel McDuff
- Tim Althoff
- Xin Liu
date: '2025-09-01'
publishDate: '2026-11-25T06:51:07.872164Z'
publication_types:
- paper-conference
publication: '*Advances in Neural Information Processing Systems, Datasets and Benchmarks
  Track*'
doi: 10.52202/085713-3699
abstract: Language models (LMs) are increasingly being deployed to perform autonomous
  data analyses. However, their data awareness—the ability to recognize, reason over,
  and appropriately handle data artifacts such as missing values, outliers, and logical
  inconsistencies—remains underexplored. These artifacts are especially common in
  real-world tabular data and, if mishandled, can significantly compromise the validity
  of analytical conclusions. To address this gap, we present RADAR, a benchmark for
  systematically evaluating data-aware reasoning on tabular data. We develop a framework
  to simulate data artifacts via programmatic perturbations to enable targeted evaluation
  of model behavior. RADAR comprises 2,980 table-query pairs, grounded in real-world
  data spanning 9 domains and 5 data artifact types. In addition to evaluating artifact
  handling, RADAR systematically varies table size to study how reasoning performance
  holds when increasing table size. Our evaluation reveals that, despite decent performance
  on tables without data artifacts, frontier models degrade significantly when data
  artifacts are introduced, exposing critical gaps in their capacity for robust, data-aware
  analysis. Designed to be flexible and extensible, RADAR supports diverse perturbation
  types and controllable table sizes, offering a valuable resource for advancing tabular
  reasoning.
links:
- name: arXiv
  url: https://arxiv.org/abs/2506.08249
- name: URL
  url: 
    https://proceedings.neurips.cc/paper_files/paper/2025/hash/a0434f04b6437e875d52d0b0e25c1729-Abstract-Datasets_and_Benchmarks_Track.html
directions:
  - human-centered-evaluation
selected: true
highlight: human-centered-evaluation
highlight_rank: 2
---
