---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.256805+00:00'
sources:
- https://www.youtube.com/watch?v=pwGI527luV8
title: Simulation Fidelity for Policy Correlation
---

## Overview
In discussing the utility of simulation for robotics, Chris Paxton argues that the primary objective is not to achieve perfect visual realism, but rather to ensure a reliable correlation between a policy's performance in simulation and its performance in the real world. The concept of "Simulation Fidelity for Policy Correlation" posits that a simulator only needs to be "barely good enough" to maintain this statistical relationship, shifting the focus from photorealism to functional validity for policy evaluation and training.

## Key Points & Analysis
> "maybe one of the takeaways here is that our goal isn't actually perfect accuracy. Our goal is to be just like kind of barely good enough so that your that your correlation holds."

This re-framing changes the benchmark for success in simulation. Instead of expending resources to minimize all visual discrepancies, the effort should be directed toward identifying and correcting the specific sim-to-real gaps that break policy correlation. A policy is a decision-making algorithm, and "policy correlation" refers to the consistency of its relative performance across domains.

**Underlying Assumptions:** This view assumes that policies can be robust to certain visual inaccuracies, but are critically sensitive to differences in the underlying data statistics. It also assumes that the cost of improving fidelity grows exponentially for diminishing returns on correlation.

**Implications and Connection to Broader Thinking:** This principle is central to a pragmatic approach in robot learning. It justifies the use of non-photorealistic, domain-randomized, or abstract simulations if they preserve performance rankings. Paxton highlights the sensitivity of models trained on real-world data:
> "small differences in the statistics of these images between real and sim can really throw off models that have only ever seen real world statistics."
Therefore, the concept connects directly to techniques like domain adaptation and randomization, which aim to build policies that are invariant to the irrelevant visual details and responsive only to the statistically meaningful features that govern action outcomes.

## Related Concepts

- [[The Sim-to-Real Transfer Gap]]