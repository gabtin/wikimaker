---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.244273+00:00'
sources:
- How to Fake A Robotics Result
title: Selective Comparison Testing
---

Selective Comparison Testing is a controlled evaluation strategy advocated by Chris Paxton for machine learning models. It involves rigorously managing who is permitted to test a model and under what specific conditions, ensuring assessments occur only in scenarios where the model is expected to perform well. This approach prioritizes controlled, favorable evaluations over open, unrestricted benchmarking.

## Key Principles
> "If you have to let other people run comparisons, choose the people carefully. Make sure they’re only happening in the right circumstances, ones your model supports as roughly in-distribution."

*   **Curated Testers**: Access is granted selectively to trusted parties, preventing potentially biased or adversarial testing.
*   **In-Distribution Focus**: Tests are confined to "right circumstances"—data and conditions similar to the model's training domain, where its performance is optimized.
*   **Contrast with Open Benchmarking**: Unlike public benchmarks that stress-test models in diverse, uncontrolled environments, this method restricts evaluation to showcase the model under ideal, supported use cases.

## Analysis
**Underlying Assumptions**: This concept assumes models have inherent limitations and are only reliable within their trained distribution. It presumes developers can and should gatekeep evaluation to prevent misleading "out-of-distribution" results that may not reflect intended usage.

**Implications**: While it protects a model's reputation by avoiding unfair edge-case failures, it reduces transparency and may obscure real-world limitations. This can foster trust among selected users but hinder independent validation.

**Broader Connection**: This tactic aligns with Paxton's pragmatic, deployment-focused mindset. It emphasizes preserving confidence in a model's core capabilities over subjecting it to potentially flawed open competition, reflecting a cautious philosophy where context-aware assessment trumps universal benchmarking.

## Related Concepts

- [[Cherry-picking Benchmarks]]
- [[Comparison Against Best Methods]]