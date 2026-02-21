---
author: chris-paxton
last_updated: '2026-02-16T16:08:06.173749+00:00'
sources:
- 'Paper Notes: Nested Learning'
title: 'Naive Solution: Retraining on All Data'
---

In continual learning, a primary challenge is **[[Catastrophic Forgetting]]**, where a model trained on new tasks loses proficiency on earlier ones. As articulated by Chris Paxton, the straightforward and most common countermeasure is the **"Naive Solution: Retraining on All Data."** This approach involves continuously sampling from every dataset the model has ever seen during training, thereby interleaving old and new knowledge to mitigate forgetting.

> "The naive solution here — the most common and usually best solution — will be to just sample from all of the different datasets so I’m always retraining on a little bit of everything, according to my other constraints."

However, Paxton immediately notes the severe practical limitations of this method.

**Key Issues and Underlying Assumptions**
This solution rests on the assumption that all past data can and should be perpetually preserved and utilized. Paxton identifies three critical problems:
1.  **Infinite Storage Requirement:** It necessitates archiving all data indefinitely, which is often infeasible.
    > "But that’s an awkward solution that requires you to store infinite data forever..."
2.  **Model Capacity and Efficiency:** As data accumulates, the model must either have sufficient spare capacity to absorb all knowledge or face performance degradation. Furthermore, training time grows with data volume, and inference speed can slow down as models become more complex to handle the expanded scope.

**Implications and Broader Context**
This critique reveals Paxton’s focus on **scalability and real-world constraints**. Highlighting the "naive solution" frames [[Catastrophic Forgetting]] not just as a technical flaw, but as a systems engineering problem involving data logistics, compute resources, and deployment practicality. It establishes a baseline against which more elegant algorithms—which seek to approximate this retraining without its overhead—are measured. The concept underscores a central tension in continual learning: the trade-off between preserving past knowledge and maintaining a lean, efficient learning system.

## Related Concepts

- [[Catastrophic Forgetting]]