---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.332560+00:00'
sources:
- https://www.youtube.com/watch?v=pwGI527luV8
title: Video Models vs. Classical Simulation for Policy Evaluation
---

## Overview
In evaluating robotic policies, researchers can use classical simulation (physics-based models built on first principles) or video models (learned simulators trained on video data of the real world). According to Chris Paxton, while video models hold significant long-term promise, **"the actual correlation ... is not nearly as strong as what you get if you use a more classic way of simulating the environment at the moment."** This means classical simulations currently provide a more reliable measure of real-world policy performance. However, the key distinction lies in their potential: **"the upper ceiling of video model evals is much higher"** for tasks involving complex, non-rigid materials that are notoriously difficult to model with classical physics.

## Key Points & Analysis

**Current Effectiveness vs. Future Potential:** Classical simulators excel at tasks with well-understood physics (e.g., rigid object manipulation), offering strong correlation to reality. Video models, as learned simulators, currently lag in this correlation but are uniquely suited for domains where first-principles modeling fails. Paxton notes the disparity: **"if you think about what kind of tasks can you actually test ... in a classic simulator ... it's going to be a whole lot harder to ... simulate a cloth folding task ... or simulate a wiping task with some liquid in there."**

**Underlying Assumptions & Broader Implications:** This comparison assumes that the fidelity of a simulator is judged by its correlation with real-world outcomes, and that different tasks impose different modeling challenges. The implication is a pragmatic, hybrid approach: use classical simulation where possible for its reliability, but invest in video model research to unlock evaluation for a broader, more complex set of real-world tasks. This connects to a broader view in robotics that favors using the right tool for the job and betting on data-driven methods to eventually master phenomena beyond the reach of hand-coded physics.