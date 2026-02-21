---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.200568+00:00'
sources:
- How to Fake A Robotics Result
title: Outsider Misunderstanding of Benchmarking Difficulty
---

## Overview
The concept of **Outsider Misunderstanding of Benchmarking Difficulty** describes a recurring pattern in robotics and machine learning research, as identified by Chris Paxton. He argues that researchers from other ML subfields frequently underestimate the immense complexity and effort required to create meaningful benchmarks in robotics. Their typical response—to circumvent existing hardware and real-world challenges by constructing new, often simulated, benchmarks—fails to advance the field. Instead, these new benchmarks lack useful insight and, critically, expand the toolkit for cherry-picking results, thereby diluting progress.

## Core Argument and Key Points
Paxton's critique centers on a disconnect in expertise and a consequent problematic solution. The core of his argument is captured in his direct statement:
> "On the same note: lots of machine learning researchers from other fields don’t understand how hard robotics benchmarking is. They will often insist on building their own, usually simulated, benchmarks, which invariably don’t tell us anything and just add more options for #6."

From this, several key points emerge:
1.  **The Central Misunderstanding:** The difficulty is not merely in training a model but in designing a benchmark that yields **actionable, generalizable insight** about real-world robotic performance. This involves grappling with hardware variability, environment uncertainty, safety, and defining meaningful success metrics.
2.  **The Problematic Response:** The outsider's solution is to retreat to simulation, building a new benchmark tailored to their method. Paxton asserts these benchmarks "invariably don’t tell us anything" because they often oversimplify reality, lack robust validation, or are designed in a way that highlights a specific algorithm's strengths while hiding its weaknesses.
3.  **The Consequence:** This proliferation of easy-to-game benchmarks creates "more options for cherry-picking" (#6 in Paxton's list of issues), allowing researchers to selectively report results on benchmarks where their method excels, obscuring true overall capability and robustness.

## Analysis and Implications
**Underlying Assumptions:** Paxton assumes that meaningful progress in robotics requires engaging with its physical, messy reality. He views benchmarking not as an abstract ML task but as an **engineering discipline** integral to the scientific process. The assumption is that simulation, while useful, is insufficient unless it is meticulously grounded and validated against real-world performance.

**Implications for the Field:** This dynamic fragments the research landscape, making it harder to compare methods and identify genuine advancements. It incentivizes "benchmark-hacking" over solving core robotic challenges, potentially steering the field toward toy problems that are academically publishable but robotically irrelevant.

**Connection to Broader Thinking:** This concept is a direct extension of Paxton's broader critique of contemporary robotics research, which he sees as plagued by low-quality evidence, cherry-picking, and a neglect of rigorous experimental design. The outsider misunderstanding exacerbates these systemic issues by introducing more noise into the evaluation ecosystem, further distancing published research from practical robotic capability.

## Related Concepts

- [[Difficulty of Authoring Simulation Tasks]]
- [[Low Robotics Benchmarking Standards]]