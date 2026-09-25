# Experiment 11 — Frozen independent real-data benchmark

**Status: frozen before execution.**

This protocol exists to prevent post-hoc changes based on whether the result favors the proposed method.

## Question

On the independent 297-point recorded ODMR trace, how do four reduced-setting strategies compare at identical measurement budgets?

1. Uniform fixed
2. Random
3. Single-model AQIE
4. Discovery + model-aware AQIE

## Frozen references

Two references must always be reported:

- Discrete deepest recorded setting: **2869.000000 MHz**
- Continuous full-trace fitted primary resonance: **2869.729971034267 MHz**

The continuous reference comes from Experiment 10, where M2S was preferred among the tested full-trace model set. The discrete reference remains visible to avoid silently changing the success metric.

## Budgets

20, 30, 40, 50, 60, 80 exposed recorded settings.

## Random baseline

100 subsets per budget, RNG seed **20260925**.

## Fixed baseline

Evenly spaced indices over the complete recorded grid.

## Single-model AQIE

M1 only. Fifteen global discovery/seed points. No model escalation. No periodic global exploration.

This baseline is intentionally brittle: it represents model-directed adaptive exploitation without the model-aware architecture.

## Discovery + model-aware AQIE

- 15 evenly spaced discovery settings
- up to 6 localization settings around the lowest discovery observation
- model bank: M1, M1S, M2, M2S
- AICc model selection
- information-directed next-setting selection
- one global exploratory setting every 6 adaptive steps

## Metrics

For every strategy/budget report error against both frozen references.

For repeated random trials report median, IQR, and 90th percentile.

A **catastrophic lock-on** is frozen as >10 MHz absolute error versus the continuous full-trace primary reference.

## Restrictions

- No synthetic noise is added to the recorded trace.
- A strategy may access a recorded value only after selecting that index.
- Full-trace values are used only for the already-frozen evaluation reference, not for adaptive decisions.
- Do not change initialization, references, budgets, model bank, random seed, exploration cadence, or failure threshold after viewing the benchmark result.
- If implementation defects are discovered, document the defect and create a new benchmark version rather than silently changing this protocol.

## Evidence boundary

This benchmark tests decision/inference logic by replaying recorded measurements. It does not reproduce PLL settling, serial latency, repeated-measurement variance, thermal/laser drift, or live hardware control.
