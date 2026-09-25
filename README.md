# Adaptive ODMR

**Model-aware measurement control for open NV-center ODMR quantum sensors.**

This repository develops an open discovery-to-adaptive-control layer for ODMR sensing:

**DISCOVER → MODEL → CHECK ADEQUACY → ADAPT → re-discover/escalate when needed**

The project grew from earlier AQIE work after deliberately testing failure under model mismatch and then replaying the controller against an independent recorded experimental ODMR trace.

## Current evidence

- Core controller and sensor abstractions: **implemented**
- Synthetic ODMR tests: **simulation-tested**
- Independent 297-point ODMR trace: **recorded-real-data-tested**
- Uncut Gem indexed-control concept: **open-hardware-compatible design**
- Live Uncut Gem control: **not yet validated**
- Wall-clock acquisition savings: **not yet demonstrated**
- Superiority over fixed/random sampling on the independent trace: **not yet established**

See `docs/EVIDENCE_LEVELS.md` and `docs/EXPERIMENT_HISTORY.md`.

## Prior work

The project builds on the AQIE research repository:
https://github.com/srikarr20/aqie

## Package layout

- `adaptive_odmr/sensors/` — simulated, recorded-data, and serial hardware backends
- `adaptive_odmr/models.py` — ODMR response models and AICc selection
- `adaptive_odmr/discovery.py` — discovery/exploration policies
- `adaptive_odmr/adequacy.py` — model-residual diagnostics
- `adaptive_odmr/selection.py` — information-directed next-setting selection
- `adaptive_odmr/controller.py` — discovery-to-adaptive orchestration
- `legacy_experiments/` — provenance record for exploratory Experiments 01–10
- `benchmarks/` — frozen benchmarks committed before execution

## Scientific caution

Recorded-data replay is not live adaptive sensing. Measurement-count reduction is not automatically acquisition-time reduction. Live hardware validation is proposed future work.
