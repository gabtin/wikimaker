---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.222015+00:00'
sources:
- How do We Quantify Progress in Robotics?
title: Real-World Evaluation as Expensive and Slow
---

## Overview
Chris Paxton identifies a fundamental bottleneck in robotics and embodied AI: **real-world evaluation is inherently slow and prohibitively expensive** to run at the necessary scale. This creates a stark contrast with other AI domains, crippling the ability to quantify progress rapidly. As Paxton frames it, the physical world imposes a hard constraint that data-centric fields do not face, making iterative development and large-scale benchmarking exceptionally difficult.

## Key Points & Analysis
> "Real-world evaluation is slow and horribly expensive to run, and can’t match the expectations of other AI fields like language or image understanding in terms of speed."

**Why it's Expensive and Slow:** Physical testing requires specialized hardware, dedicated lab or operational space, and significant human oversight for safety and resetting conditions. Each trial (or "rollout") takes real clock time—seconds, minutes, or hours—unlike a language model inference that completes in milliseconds. This drastically limits the number of experiments that can be run, creating a severe **data throughput problem**.

**Underlying Assumptions and Implications:**
Paxton's argument assumes that robust, generalizable intelligence for physical tasks requires extensive evaluation in the real world, which is the ultimate proving ground. This highlights a core divergence in AI: progress in NLP or computer vision is driven by **sample efficiency** (learning from massive static datasets), while robotics progress is throttled by **time efficiency** and **capital cost**. The implication is that the field cannot directly adopt the "train fast, evaluate often" paradigm of software-only AI, forcing a reliance on simulators (which introduce a **sim-to-real gap**) and making definitive benchmarking a major logistical challenge. It connects to his broader focus on creating practical, deployable robotic systems where the cost of validation becomes a primary constraint on innovation.

## Related Concepts

- [[Benchmarking for Zero-Shot Generalization in Robotics]]
- [[The Sim-to-Real Transfer Gap]]
- [[Tournament-Style Real-World Evaluation]]