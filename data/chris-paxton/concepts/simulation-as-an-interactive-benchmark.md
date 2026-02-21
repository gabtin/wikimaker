---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.253864+00:00'
sources:
- How do We Quantify Progress in Robotics?
title: Simulation as an Interactive Benchmark
---

## Overview
Chris Paxton frames simulation as an increasingly necessary but fundamentally flawed **interactive benchmark** for robotics. He argues that because many core robotics challenges require real-time interaction with an environment, traditional static datasets are insufficient for evaluation. While noting that "simulations are getting more powerful, more interesting, and more diverse all the time," he presents them as a pragmatic, if imperfect, solution for creating standardized, repeatable interactive tests. The central tension he identifies is between the growing utility of simulation for development and benchmarking and its persistent failure to accurately encapsulate the messy reality of the physical world.

## Key Points & Analysis
> "If we need interactivity, perhaps the best benchmark, then, will be in simulation."

This statement establishes Paxton's core reasoning: **interactivity is a prerequisite** for meaningful evaluation of robotic agents. Benchmarks must test closed-loop perception, decision-making, and control. Simulations uniquely offer this at scale, supporting rapid iteration and comparison.

**Assumptions & Limitations:** Paxton’s argument assumes that progress in robotics is bottlenecked by the lack of standardized interactive tests. He is deeply skeptical of simulation's fidelity, however, stating:
> "Fundamentally, though, simulations are still hard to work with and an inaccurate representation of the true robotics problem, without sensor and actuator noise, with overly-clean problems, and with unpredictable, often-inaccurate contact dynamics."

The implied assumption is that the "true robotics problem" is defined by physical noise and complexity. Therefore, a simulation benchmark is inherently a **compromise**. Its value depends entirely on **sim-to-real transfer**—the ability of skills learned or evaluated in simulation to function on a physical robot.

**Implications & Broader Context:** This concept connects to Paxton’s broader view that robotics advancement requires honest accounting of technical gaps. Pushing for simulation benchmarks is a pragmatic step toward better evaluation, but it carries the risk of creating a field that over-optimizes for "clean" synthetic performance. The ultimate goal remains solving the real-world problem, making the improvement of physical realism and sim-to-real techniques not just an engineering detail, but the critical factor determining the benchmark's long-term relevance.

## Related Concepts

- [[ImageNet as a Controlled, Non-Interactive Benchmark]]
- [[Inadequacy of Offline Datasets for Robotics]]
- [[The Need for a Unified Simulator]]
- [[The Sim-to-Real Transfer Gap]]