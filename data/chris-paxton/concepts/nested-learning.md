---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.181655+00:00'
sources:
- 'Paper Notes: Nested Learning'
title: Nested Learning
---

Nested Learning is a proposed approach to lifelong learning in AI that reframes the machine learning optimization problem as a set of nested sub-problems. It aims to mitigate [[Catastrophic Forgetting]] by designing inner loops that update rapidly for new information and outer loops that update slowly to anchor general information. Chris Paxton introduces it as a way to view models hierarchically, leveraging the inherent properties of existing optimizers.

## Core Mechanism
> "We introduce Nested Learning, a new approach to machine learning that views models as a set of smaller, nested optimization problems, each with its own internal workflow, in order to mitigate or even completely avoid the issue of '[[Catastrophic Forgetting]]'..."
The structure operates on different temporal scales: fast inner loops adapt to recent data, while slow outer loops stabilize core knowledge. This is possible because, as Paxton notes, > "The key insight here is that momentum-based optimizers like Adam are, in and of themselves, a sort of associative memory — basically a model." Thus, the learning process itself becomes a nested memory system.

## Analysis
This concept assumes that optimization can be decomposed into separable timescales and that momentum in optimizers implicitly stores knowledge. It implies that [[Catastrophic Forgetting]] might be addressed through algorithmic redesign rather than just architectural changes, connecting to broader ideas about making AI systems more fluid and biological in their continuous learning. However, it relies on carefully orchestrated learning rates and may increase computational complexity during training.

## Related Concepts

- [[Associative Memory as Core Architecture]]
- [[Catastrophic Forgetting]]