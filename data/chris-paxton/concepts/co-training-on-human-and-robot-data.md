---
author: chris-paxton
last_updated: '2026-02-16T16:29:12.904737+00:00'
sources:
- How Human Should Your Humanoid Be?
tags:
- machine learning
- representation learning
- robotics
- transfer learning
title: Co-training on Human and Robot Data
---

## Overview
Co-training on human and robot data is an approach in robot learning where models are trained simultaneously on datasets from both human demonstrations (often video) and physical robot executions. The core idea is that through this joint training, the model naturally learns a **shared embedding space**—a common internal representation—for tasks that bridges the different embodiments. This enables **human to robot transfer**, allowing robots, including non-humanoid ones, to leverage the vast amounts of available human video data to acquire skills, without requiring the robot to have a human-like form or kinematics.

## Key Points & Analysis

> "But your robot might not need to be human to take advantage of video data. Take a look at the recent 'Emergence of Human to Robot Transfer in VLAs,'... they show how just by co-training on human and robot data, the models naturally learn a similar embedding space for tasks which is shared across the different embodiments."

*   **Shared Embedding Space:** This is a latent representation where semantically similar actions or task stages from human videos and robot sensorimotor data are mapped close together, despite the difference in "hardware." For example, the concept of "picking up a cup" would activate a similar region in this space, whether from a human hand or a robot gripper.
*   **Key Assumption:** The method assumes that while embodiments differ, there is enough underlying **task structure** and intent common to both human and robot demonstrations for a useful shared representation to emerge. It relies on the model's ability to abstract away low-level physical differences.
*   **Implications:** This drastically broadens the potential for using internet-scale human video data to teach robots, moving beyond the limitation of requiring perfectly aligned, robot-specific demonstrations. It suggests a path toward more data-efficient and generalizable robot learning.
*   **Connection to Broader Thinking:** This concept aligns with Chris Paxton's focus on **practical robot learning** and **transfer**. It reframes the problem from one of embodiment alignment to one of representation learning, seeking common ground in the *semantics* of action rather than the *kinematics*. It underscores a shift toward leveraging diverse, imperfect data sources to build more capable and adaptable robotic systems.

## Related Concepts

- [[Inadequacy of Offline Datasets for Robotics]]
- [[Overcoming the Robotics Data Gap and Maturity of Learning Techniques]]