---
title: 'Leveraging Collaborative-Filtering for Personalized Behavior Modeling: A Case
  Study of Depression Detection among College Students'
authors:
- Xuhai Xu
- Prerna Chikersal
- Janine M Dutcher
- Yasaman Sefidgar
- Woosuk Seo
- Michael J Tumminia
- Daniella K Villalba
- Sheldon Cohen
- Kasey Creswell
- J David Creswell
- Afsaneh Doryab
- Paula S Nurius
- Eve A Riskin
- Anind K Dey
- Jennifer Mankoff
date: '2021-03-01'
publishDate: '2024-09-29T06:40:21.820683Z'
publication_types:
- article-journal
publication: '*Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous
  Technologies*'
publication_short: '*ACM IMWUT*'
doi: 10.1145/3448107
abstract: The prevalence of mobile phones and wearable devices enables the passive
  capturing and modeling of human behavior at an unprecedented resolution and scale.
  Past research has demonstrated the capability of mobile sensing to model aspects
  of physical health, mental health, education, and work performance, etc. However,
  most of the algorithms and models proposed in previous work follow a one-size-fits-all
  (i.e., population modeling) approach that looks for common behaviors amongst all
  users, disregarding the fact that individuals can behave very differently, resulting
  in reduced model performance. Further, black-box models are often used that do not
  allow for interpretability and human behavior understanding. We present a new method
  to address the problems of personalized behavior classification and interpretability,
  and apply it to depression detection among college students. Inspired by the idea
  of collaborative-filtering, our method is a type of memory-based learning algorithm.
  It leverages the relevance of mobile-sensed behavior features among individuals
  to calculate personalized relevance weights, which are used to impute missing data
  and select features according to a specific modeling goal (e.g., whether the student
  has depressive symptoms) in different time epochs, i.e., times of the day and days
  of the week. It then compiles features from epochs using majority voting to obtain
  the final prediction. We apply our algorithm on a depression detection dataset collected
  from first-year college students with low data-missing rates and show that our method
  outperforms the state-of-the-art machine learning model by 5.1% in accuracy and
  5.5% in F1 score. We further verify the pipeline-level generalizability of our approach
  by achieving similar results on a second dataset, with an average improvement of
  3.4% across performance metrics. Beyond achieving better classification performance,
  our novel approach is further able to generate personalized interpretations of the
  models for each individual. These interpretations are supported by existing depression-related
  literature and can potentially inspire automated and personalized depression intervention
  design in the future.
links:
- name: URL
  url: https://dl.acm.org/doi/10.1145/3448107
directions:
  - human-centered-health-foundation-models
---
