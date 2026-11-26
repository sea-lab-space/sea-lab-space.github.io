---
title: 'Listen2Cough: Leveraging End-to-End Deep Learning Cough Detection Model to
  Enhance Lung Health Assessment Using Passively Sensed Audio'
authors:
- Xuhai Xu
- Ebrahim Nemati
- Korosh Vatanparvar
- Viswam Nathan
- Tousif Ahmed
- Md Mahbubur Rahman
- Daniel McCaffrey
- Jilong Kuang
- Jun Alex Gao
date: '2021-03-01'
publishDate: '2024-09-29T06:40:21.830839Z'
publication_types:
- article-journal
publication: '*Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous
  Technologies*'
publication_short: '*ACM IMWUT*'
doi: 10.1145/3448124
abstract: 'The prevalence of ubiquitous computing enables new opportunities for lung
  health monitoring and assessment. In the past few years, there have been extensive
  studies on cough detection using passively sensed audio signals. However, the generalizability
  of a cough detection model when applied to external datasets, especially in real-world
  implementation, is questionable and not explored adequately. Beyond detecting coughs,
  researchers have looked into how cough sounds can be used in assessing lung health.
  However, due to the challenges in collecting both cough sounds and lung health condition
  ground truth, previous studies have been hindered by the limited datasets. In this
  paper, we propose Listen2Cough to address these gaps. We first build an end-to-end
  deep learning architecture using public cough sound datasets to detect coughs within
  raw audio recordings. We employ a pre-trained MobileNet and integrate a number of
  augmentation techniques to improve the generalizability of our model. Without additional
  fine-tuning, our model is able to achieve an F1 score of 0.948 when tested against
  a new clean dataset, and 0.884 on another in-the-wild noisy dataset, leading to
  an advantage of 5.8% and 8.4% on average over the best baseline model, respectively.
  Then, to mitigate the issue of limited lung health data, we propose to transform
  the cough detection task to lung health assessment tasks so that the rich cough
  data can be leveraged. Our hypothesis is that these tasks extract and utilize similar
  effective representation from cough sounds. We embed the cough detection model into
  a multi-instance learning framework with the attention mechanism and further tune
  the model for lung health assessment tasks. Our final model achieves an F1-score
  of 0.912 on healthy v.s. unhealthy, 0.870 on obstructive v.s. non-obstructive, and
  0.813 on COPD v.s. asthma classification, outperforming the baseline by 10.7%, 6.3%,
  and 3.7%, respectively. Moreover, the weight value in the attention layer can be
  used to identify important coughs highly correlated with lung health, which can
  potentially provide interpretability for expert diagnosis in the future. CCS Concepts:
  • Human-centered computing → Ubiquitous and mobile computing; • Applied computing
  → Life and medical sciences.'
links:
- name: URL
  url: https://dl.acm.org/doi/10.1145/3448124
directions:
  - human-centered-health-foundation-models
---
