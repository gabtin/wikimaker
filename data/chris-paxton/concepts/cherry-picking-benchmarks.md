---
author: chris-paxton
last_updated: '2026-02-16T16:28:19.195336+00:00'
sources:
- How to Fake A Robotics Result
- How do We Quantify Progress in Robotics?
tags:
- benchmarking
- methodology
- research-ethics
- transparency
title: Cherry-picking Benchmarks
---

## Overview

The concept of "cherry-picking benchmarks" is presented as a strategic, if cynical, tactic for showcasing a robotics model's performance. The core argument is that the proliferation of robotics benchmarks, while seeming to offer objective comparisons, actually enables selective reporting. This problem is exacerbated by the parallel proliferation of niche simulators, each with their own subtleties. Because each benchmark tests "subtly different things," a researcher can choose to report results only from those benchmarks—and within those specific simulator environments—most favorable to their approach. The tactic's effectiveness hinges on the fact that the meaningful differences between benchmarks are opaque to most of the audience. As Chris Paxton notes:

> "On the same note: cherry-pick your benchmarks. There are a ton of robotics benchmarks out there, and they all test subtly different things. Importantly, these differences are not obvious to people who are not familiar with the benchmarks involved."

This dynamic directly undermines the foundational purpose of benchmarking. As the new source argues, when researchers can easily “choose your own” subset of benchmarks upon which their model will perform the best, it "renders moot the whole point of even having benchmarks in the first place!" for fair comparison.

## Analysis of the Concept

**Underlying Assumptions:** This advice assumes a landscape where benchmarks and their accompanying simulators are numerous, highly specialized, and poorly understood outside niche circles. It presumes that readers—including reviewers and even researchers in adjacent fields—lack the deep, contextual knowledge to discern whether a chosen benchmark genuinely tests broad capability or just a narrow, favorable slice of it. The benchmark itself is treated not as a neutral tool, but as a rhetorical device. The new source extends this by implicating the ecosystem of simulators themselves, suggesting their variety in physics, rendering, and task specification creates a large menu of options for favorable selection rather than a unified ground for evaluation.

**Implications & Connection to Broader Thinking:** The implication is that benchmarking in robotics can often be a game of perception rather than a true measure of progress. This connects to a broader skepticism about whether common evaluation practices genuinely capture robust, generalizable robotic intelligence, or merely reward overfitting to specific, isolated task specifications within a chosen simulator. The concept critiques a research culture where the strategic presentation of results can be as important as the technical work itself, potentially obscuring a model's true weaknesses and inflating claims of its generality. The new source reinforces this by highlighting the ultimate consequence: when cherry-picking is facilitated by ecosystem fragmentation, the entire comparative framework of the field is weakened, making it difficult to quantify genuine progress.

## Related Concepts

- [[Argument from Setup Differences]]
- [[Choosing Weak Baselines]]
- [[Low Robotics Benchmarking Standards]]
- [[Selective Comparison Testing]]
- [[Tricks vs. Invalid Results]]