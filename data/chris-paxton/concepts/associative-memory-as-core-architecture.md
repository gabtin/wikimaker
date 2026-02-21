---
author: chris-paxton
last_updated: '2026-02-16T16:26:40.122128+00:00'
sources:
- 'Paper Notes: Nested Learning'
tags:
- learning
- machine-learning
- memory
- systems
title: Associative Memory as Core Architecture
---

Chris Paxton's concept "Associative Memory as Core Architecture" challenges foundational distinctions in machine learning. He argues that architectural categories—like neural networks versus optimizers—are superficial, as both are fundamentally associative memories. This memory maps keys to values, with learning emerging from neural updates. As Paxton states, > "The core claim of the paper is that architecture is an illusion: that both optimizers (Adam, for example) and neural networks are the same thing: an associative memory." Learning is thus recast as memory formation: > "Memory is a neural update caused by an input, and learning is the process for acquiring effective and useful memory."

## Core Insights and Analysis
**Unified Framework:** Paxton reduces all learning systems to associative memory operations. For instance, a neural network associates input features with predictions, while Adam associates gradients with parameter updates—both are key-value mappings. This reframing implies that design separations between model and optimizer are arbitrary.

**Key Assumptions:** The perspective assumes that neural updates inherently constitute memory, and that learning efficacy depends on accumulating useful associations. It presumes a functional equivalence across architectures, downplaying unique structural roles.

**Implications:** By erasing traditional boundaries, this view encourages integrated designs where memory and optimization coalesce. It suggests progress may come from enhancing associative recall rather than stacking layers or tuning optimizers independently.

**Broader Connections:** Paxton's thinking aligns with embodied and distributed cognition, where intelligence arises from interactive memory systems. It pushes toward holistic, memory-centric paradigms in AI, moving beyond compartmentalized architecture.

## Related Concepts

- [[Nested Learning]]