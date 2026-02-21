---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.047779+00:00'
sources:
- 'Paper Notes: Nested Learning'
title: Deep Optimizers
---

## Overview
Within the [[Nested Learning]] framework, Chris Paxton argues for moving beyond hand-designed optimization algorithms. He proposes "Deep Optimizers" as a direct replacement for simple, static optimizers like Stochastic Gradient Descent (SGD). The core idea is that optimization itself is a form of pattern recall and application, which can be learned. As Paxton frames it:

> "Optimizers like SGD are just very simple associative memories, which the authors propose replacing with 'Deep Optimizers' that learn how to update inner networks."

A Deep Optimizer is itself a learned model—typically a neural network with associative memory capabilities—that observes the state of an "inner" network (e.g., its parameters, gradients, and loss) and outputs a tailored parameter update. This creates a meta-learning loop where the update rule is not fixed but discovered from data.

## Key Points & Analysis

**Associative Memory as Optimization:** The foundational assumption is that an optimizer's task—mapping a network state to a parameter update—is analogous to an associative memory recalling a pattern. SGD implements a trivial, fixed "memory" (multiply gradient by learning rate). A Deep Optimizer learns a complex, context-aware mapping.

**Learned Update Rules:** Instead of manually tuning an optimizer's hyperparameters (like learning rate schedules), a Deep Optimizer learns how to update. It internalizes strategies like momentum, adaptation, and learning rate annealing from exposure to many optimization scenarios during its own training.

**Implications:** This concept implies that optimization is not a purely mathematical, predefined process but a learnable skill. It connects to Paxton's broader view of [[Nested Learning]], where systems are built in hierarchical, learned layers, moving away from manual design. The major shift is treating the optimizer *architecture* as a central, trainable component rather than an off-the-shelf tool. The underlying assumption is that data-driven optimizers can discover more efficient, problem-specific paths through loss landscapes than generic algorithms.

## Related Concepts

- [[Nested Learning]]