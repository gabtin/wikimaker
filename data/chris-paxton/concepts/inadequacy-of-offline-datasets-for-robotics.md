---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.144047+00:00'
sources:
- How do We Quantify Progress in Robotics?
title: Inadequacy of Offline Datasets for Robotics
---

Chris Paxton contends that the use of offline datasets for evaluating robot performance is fundamentally flawed, as robotics is an inherently interactive domain. Small errors in action prediction accumulate over time, leading to divergent outcomes, and effective policies must recover from partial failures—a dynamic process impossible to assess without interaction.

## Key Arguments
Paxton emphasizes that interaction is central to robotics. He states:  
> "However, robotics is an inherently interactive domain; small errors in action prediction accumulate over time, and lead to different outcomes. Good policies compensate for these, and recover from partial task failures."  
Offline datasets, which consist of pre-recorded data, cannot simulate the real-time feedback loops necessary for evaluation. Consequently,  
> "Without an interactive environment to evaluate in, we can’t compute task success rates, and we can’t determine whether a policy would be useful at deployment time."  
For example, a policy trained on static data might perform well on historical trajectories but fail when slight deviations require recovery maneuvers.

## Analysis
This argument assumes that robotics success is defined by robust, closed-loop performance in unpredictable environments. It implies that evaluation methodologies must shift towards interactive simulations or physical testing to measure true utility. Connecting to broader thinking, Paxton likely advocates for robotics research that prioritizes adaptive control and online learning, challenging overreliance on offline benchmarks that misrepresent deployment challenges.

## Related Concepts

- [[Co-training on Human and Robot Data]]
- [[Open and Diverse Datasets for Training and Testing]]
- [[Overcoming the Robotics Data Gap and Maturity of Learning Techniques]]
- [[Simulation as an Interactive Benchmark]]
- [[The Compounding Error Problem]]