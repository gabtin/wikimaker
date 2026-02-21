---
author: chris-paxton
last_updated: '2026-02-16T16:27:50.881539+00:00'
sources:
- 'Paper Notes: Nested Learning'
tags:
- lifelong learning
- machine learning
- neural networks
- robotics
title: Catastrophic Forgetting
---

**Overview**

Catastrophic forgetting is identified as the central obstacle in achieving lifelong learning for artificial systems, particularly in robotics. It describes the phenomenon where a model, trained sequentially on new tasks or data, loses its previously acquired skills. This occurs because the model's parameters are overwritten during new training, without any mechanism to preserve the knowledge embedded in them from past experiences. The result is a system that gains new abilities at the total expense of old ones, rather than accumulating knowledge. As Chris Paxton states: > "The core problem we want to solve with lifelong learning is called catastrophic forgetting."

**Key Points**

*   **The Core Problem:** It is the fundamental technical barrier to building a robot or AI that can learn continually over its lifetime, akin to human learning.
*   **Mechanism of Forgetting:** Forgetting happens during sequential training. When a system learns Task B (e.g., stacking plates), the neural network updates that optimize performance for B inadvertently degrade the specific configuration needed for Task A (e.g., putting away cups).
*   **Practical Consequence:** The loss of prior skills is total and severe. Paxton illustrates this with a direct example: > "Unsurprisingly, when I next try to train on A, I see that I’ve now lost all performance on A — my robot can no longer put away cups properly."
*   **The Goal:** The aim of lifelong learning research is to develop algorithms that can learn new tasks while mitigating or eliminating this catastrophic interference, enabling the retention and reuse of old skills.

**Analysis of Underlying Assumptions and Implications**

The concept assumes a learning paradigm where data or tasks arrive sequentially and where storing all past data for retraining is impractical or impossible—a common real-world constraint for embodied robots. It implies that naive training methods are insufficient for continual learning, demanding explicit architectural or algorithmic solutions to stabilize knowledge. This frames the challenge not merely as one of model capacity, but of *knowledge management* over time. For Paxton, overcoming catastrophic forgetting is essential for practical robotics, where a single system must adapt to new environments and tasks without requiring complete retrebuilding from scratch or maintaining separate models for every skill. It connects directly to his broader focus on creating flexible, generalist robots that can learn and remember across a lifetime of diverse experiences.

## Related Concepts

- [[Naive Solution: Retraining on All Data]]