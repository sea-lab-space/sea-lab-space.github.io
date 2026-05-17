---
title: 'Health-LLM: Large Language Models for Health Prediction via Wearable Sensor Data'
authors:
- Yubin Kim
- Xuhai Xu
- Daniel McDuff
- Cynthia Breazeal
- Hae Won Park
date: '2024-04-01'
publishDate: '2024-09-29T06:40:21.541879Z'
publication_types:
- paper-conference
publication: '*Proceedings of Machine Learning Research, Conference on Health, Inference, and Learning (CHIL)*'
abstract: Large language models (LLMs) are capable of many natural language tasks,
  yet they are far from perfect. In health applications, grounding and interpreting
  domain-specific and nonlinguistic data is important. This paper investigates the
  capacity of LLMs to deliver multimodal health predictions based on contextual information
  (e.g. user demographics, health knowledge) and physiological data (e.g. resting
  heart rate, sleep minutes). We present a comprehensive evaluation of eight state-of-the-art
  LLMs with diverse prompting and fine-tuning techniques on six public health datasets
  (PMData, LifeSnaps, GLOBEM, AW_FB, MITBIH & MIMIC-III). Our experiments cover thirteen
  consumer health prediction tasks in mental health, activity, metabolic, sleep, and
  cardiac assessment. Our fine-tuned model, HealthAlpaca exhibits comparable performance
  to larger models (GPT-3.5 and GPT-4), achieving the best performance in 5 out of
  13 tasks. Ablation studies highlight the effectiveness of context enhancement strategies,
  and generalization capability of the fine-tuned models across training datasets
  and the size of training samples. Notably, we observe that our context enhancement
  can yield up to 23.8% improvement in performance. While constructing contextually
  rich prompts (combining user context, health knowledge and temporal information)
  exhibits synergistic improvement, the inclusion of health knowledge context in prompts
  significantly enhances overall performance.
links:
- name: URL
  url: http://arxiv.org/abs/2401.06866
tags:
  - 'health prediction'
---
