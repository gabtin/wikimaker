---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.316732+00:00'
sources:
- How do We Quantify Progress in Robotics?
title: The Sim-to-Real Transfer Gap
---

## Overview
The **Sim-to-Real Transfer Gap** refers to the persistent challenge of successfully applying robotic skills learned in simulation to real-world hardware. While progress is being made, as seen in projects like NVIDIA's Doorman, this gap remains significant. The core issue is that simulations are fundamentally simplified models, lacking the critical noise, complexity, and unpredictability of physical reality. As Chris Paxton notes, despite advances, "simulations are still hard to work with and an inaccurate representation of the true robotics problem."

## Key Aspects of the Gap
Paxton identifies several specific shortcomings of simulation that create this gap:
*   **Lack of Noise:** Simulations operate "without sensor and actuator noise," creating an unrealistic perception and control environment for the robot.
*   **Overly-Clean Problems:** They present "overly-clean problems," failing to capture the clutter, wear, and imperfect conditions robots encounter in the real world.
*   **Unpredictable Dynamics:** Most critically, they feature "unpredictable, often-inaccurate contact dynamics." Simulating the complex physics of physical interactions, like a gripper touching a door handle, is exceptionally difficult and a major source of transfer failure.

## Analysis & Broader Context
Paxton's framing makes a key assumption: that the "true robotics problem" is inherently defined by the messy physical world, not by a clean digital abstraction. This implies that simulation alone is insufficient; it is a tool for preliminary development, but real-world evaluation and adaptation remain indispensable. This concept connects to a broader skepticism within robotics towards purely simulated solutions, emphasizing that robust autonomy must be validated against, and ultimately learned from, physical reality. The case of Doorman, which was "sufficient to teach a robot to open a door — though note many difficulties involved in this work!" serves as a prime example: a success that nonetheless highlights the enduring hurdles of the sim-to-real gap.

## Related Concepts

- [[Constrained Environment Optimization]]
- [[Overcoming the Robotics Data Gap and Maturity of Learning Techniques]]
- [[Real-World Evaluation as Expensive and Slow]]
- [[Simulation Fidelity for Policy Correlation]]
- [[Simulation as an Interactive Benchmark]]
- [[The Compounding Error Problem]]