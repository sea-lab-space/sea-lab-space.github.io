---
title: 'GLOBEM: Cross-Dataset Generalization of Longitudinal Human Behavior Modeling'
authors:
- Xuhai Xu
- Xin Liu
- Han Zhang
- Weichen Wang
- Subigya Nepal
- Yasaman Sefidgar
- Woosuk Seo
- Kevin S Kuehn
- Jeremy F Huckins
- Margaret E Morris
- Paula S Nurius
- Eve A Riskin
- Shwetak Patel
- Tim Althoff
- Andrew Campbell
- Anind K Dey
- Jennifer Mankoff
date: '2023-01-01'
publishDate: '2024-09-29T06:40:21.788728Z'
publication_types:
- article-journal
publication: '*Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous
  Technologies*'
doi: 10.1145/3569485
abstract: There is a growing body of research revealing that longitudinal passive
  sensing data from smartphones and wearable devices can capture daily behavior signals
  for human behavior modeling, such as depression detection. Most prior studies build
  and evaluate machine learning models using data collected from a single population.
  However, to ensure that a behavior model can work for a larger group of users, its
  generalizability needs to be verified on multiple datasets from different populations.
  We present the first work evaluating cross-dataset generalizability of longitudinal
  behavior models, using depression detection as an application. We collect multiple
  longitudinal passive mobile sensing datasets with over 500 users from two institutes
  over a two-year span, leading to four institute-year datasets. Using the datasets,
  we closely re-implement and evaluated nine prior depression detection algorithms.
  Our experiment reveals the lack of model generalizability of these methods. We also
  implement eight recently popular domain generalization algorithms from the machine
  learning community. Our results indicate that these methods also do not generalize
  well on our datasets, with barely any advantage over the naive baseline of guessing
  the majority. We then present two new algorithms with better generalizability. Our
  new algorithm, Reorder, significantly and consistently outperforms existing methods
  on most cross-dataset generalization setups. However, the overall advantage is incremental
  and still has great room for improvement. Our analysis reveals that the individual
  differences (both within and between populations) may play the most important role
  in the cross-dataset generalization challenge. Finally, we provide an open-source
  benchmark platform GLOBEM- short for Generalization of Longitudinal BEhavior Modeling
  - to consolidate all 19 algorithms. GLOBEM can support researchers in using, developing,
  and evaluating different longitudinal behavior modeling methods. We call for researchers'
  attention to model generalizability evaluation for future longitudinal human behavior
  modeling studies.
links:
- name: URL
  url: https://dl.acm.org/doi/10.1145/3569485
directions:
  - human-centered-evaluation
  - human-centered-health-foundation-models
selected: true
highlight: human-centered-evaluation
highlight_rank: 1
---
