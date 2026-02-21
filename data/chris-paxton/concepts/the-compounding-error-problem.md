---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.307071+00:00'
sources:
- How do We Quantify Progress in Robotics?
title: The Compounding Error Problem
---

## Overview

The Compounding Error Problem is a fundamental critique of using purely offline datasets to train robotic policies. As articulated by Chris Paxton, the core issue is that robotic actions are executed in a sequential, real-world trajectory where small prediction errors are not independent. Instead, they accumulate, or compound, driving the robot into states not represented in the static dataset. Since the policy was never tested or trained to recover from these novel, often failing, states offline, it lacks the robustness to succeed in practice. Paxton frames this as a primary reason offline learning fails: **"Offline datasets do not work because robots never do exactly the same thing, these errors compound, and all robot tasks are too multimodal for this to be meaningful."**

## Key Points & Analysis

**The Mechanism of Failure:** A policy trained offline learns to predict actions from a dataset of (state, action) pairs. However, when deployed, any slight deviation in its first action puts the robot in a state slightly different from what was in the dataset. The policy, now querying this novel state, is more likely to make another small error. This cycle repeats, causing the robot to rapidly diverge from the demonstrated trajectory into uncharted and often catastrophic state space.

**Underlying Assumptions:** This argument assumes that 1) the real-world state-action space is vast and highly sensitive to initial conditions, 2) perfect imitation is impossible, making some error inevitable, and 3) successful robotic operation requires the ability to recover from self-induced errors, not just follow a perfect script.

**Implications & Broader Context:** This problem directly motivates Paxton's advocacy for online learning, simulation, and real-world testing where policies can experience and learn from their own compounding mistakes. It connects to his broader view that robotics must embrace closed-loop interaction, where the system learns not just a single path, but a *strategy* for navigating the complex, multimodal reality of physical tasks. The compounding error problem highlights why robotics is not merely a "big data" challenge, but one requiring adaptive, reactive policies.

## Related Concepts

- [[Inadequacy of Offline Datasets for Robotics]]
- [[Key Technical Challenges: Environmental Interaction and World Models]]
- [[Reinforcement Learning for Superhuman Performance]]
- [[Solution: Cross-Platform Models & Many Robots]]
- [[The Sim-to-Real Transfer Gap]]