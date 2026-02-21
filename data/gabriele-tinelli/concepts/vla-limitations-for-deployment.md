---
author: gabriele-tinelli
last_updated: '2026-02-16T14:51:25.935512+00:00'
sources:
- https://gabtin.github.io/thoughts/robotics-foundation-models/
title: VLA Limitations for Deployment
---

## Overview
In robotics and industrial automation, **VLA Limitations for Deployment** refer to the practical challenges hindering the real-world application of Vision-Language-Action (VLA) models. As discussed by roboticist Gabriele Tinelli, these multimodal AI models, which process visual and linguistic inputs to generate physical actions, face significant barriers in industrial settings due to their inherent non-determinism. Tinelli argues that this makes them unreliable and difficult to integrate into professional workflows where predictability, interpretability, and trust are paramount.

## Lack of Interpretability
A core limitation identified by Tinelli is the lack of interpretability in VLA decision-making. In industrial operations, such as construction, maintenance, or manufacturing, technicians and project managers require clear visibility into a machine's state and progress. VLAs, functioning as "black boxes," do not provide this necessary transparency.

> "non-deterministic approaches like VLM/VLAs are currently hard to deploy on the field because they lack the interpretability that allows tracking of workflow completion."

Without the ability to track the logical steps a model is taking toward a goal, operators cannot easily verify correct operation, diagnose errors, or ensure procedural compliance, which is critical for safety and quality control.

## Absence of a Deterministic Feedback Loop
Closely related is the absence of a deterministic feedback loop. Traditional industrial robotics relies on predictable, repeatable actions with well-defined cause-and-effect relationships. VLAs, by contrast, may generate different outputs for similar inputs due to their probabilistic nature. This non-determinism prevents the establishment of a reliable feedback loop where an operator can issue a corrective command with confidence in a specific, repeatable outcome. This unpredictability complicates debugging, validation, and iterative refinement of tasks.

## Implications for Industrial Adoption
Tinelli posits that these technical limitations create a fundamental mismatch with the needs of industrial users. For professionals in trades and project-based industries, effective tools are extensions of their skill, offering reliability and control. VLAs, in their current state, fail to meet this criterion.

> "they violate the concept that, in project-industry users (construction, trades, maintenance etc.) robotics needs to feel like new tooling, rather than an obscure new machine that we need to worry about the uptime of."

Consequently, instead of being perceived as a productivity-enhancing tool, a VLA-based system is seen as an "obscure machine" that introduces uncertainty and operational risk, undermining user trust and complicating maintenance and uptime guarantees. Tinelli's analysis suggests that until VLAs can offer greater transparency and behavioral consistency, their deployment in high-stakes, real-world industrial environments will remain limited.

## Related Concepts

- [[Language as Interface, Not Foundation]]
- [[Practical Functional Robots]]