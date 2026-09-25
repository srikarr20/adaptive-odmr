# Legacy experiment chain: 01–10

This directory documents the exploratory evidence chain that led to the current Adaptive ODMR project.

The original experiments were executed interactively during development. Some generated numerical artifacts were retained, while not every interactive experiment was saved as a standalone source file.

## Provenance rule

We do **not** reconstruct code later and label it as the original experiment.

Reusable implementations will live under `adaptive_odmr/` and will be explicitly treated as refactored/reconstructed implementations derived from the documented experiment logic.

The historical value of Experiments 01–10 is the sequence of failures and architectural corrections:

simulation baseline → adaptive compression → deliberate mismatch → adequacy monitoring → governed adaptation → hierarchical escalation → independent real-data failure → discovery → real-data model selection → full-trace reference.

See `docs/EXPERIMENT_HISTORY.md`.
