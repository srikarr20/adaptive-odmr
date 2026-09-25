# Experiment history

## 01–02 — Baseline and adaptive compression

An Uncut-Gem-compatible synthetic ODMR sensor established a full-sweep baseline. Reduced fixed/random sampling was compared with adaptive setting selection. The in-model result motivated further testing but was not treated as general validation.

## 03 — Deliberate model mismatch

The synthetic sensor was made structurally richer than the inference model using a secondary resonance, baseline slope, altered contrast/linewidth, and nonuniform noise. AQIE deteriorated under strong mismatch.

**Finding:** an adaptive controller can efficiently exploit the wrong model.

## 04–06 — Measurement-model awareness

Residual adequacy monitoring, governed acquisition, and hierarchical model escalation were introduced. Simulation showed that model-awareness could mitigate structured mismatch while retaining normal-operation performance.

## 07 — Independent recorded ODMR failure

The first replay against an independent 297-point experimental ODMR trace failed catastrophically: sparse initialization missed the relevant resonance region and the adaptive loop locked onto a wrong region (~148 MHz error).

**Finding:** local model adequacy cannot reveal an important response feature that was never observed.

## 08 — Discovery before exploitation

A global discovery/localization stage was added before adaptive exploitation. It removed the catastrophic lock-on, but increasing data exposed structural inadequacy of the single-Lorentzian model.

## 09 — Reduced-data model selection

A model bank was introduced. Reduced-data acquisition selected a two-resonance model and progressively converged as additional recorded settings were exposed.

## 10 — Full-trace reference

The complete 297-point trace was used only to establish the evaluation reference. Among the tested models, double Lorentzian + slope (M2S) had the best AICc. Fitted centers were approximately 2861.399 MHz and 2869.730 MHz.

Rebasing the reduced-data adaptive estimates to the full-data primary fitted center gave approximately:
- N=25: 612 kHz error
- N=30: 362 kHz
- N=40: 158 kHz
- N=50: 91.8 kHz
- N=60: 32.6 kHz
- N=80: 11.7 kHz

These results show convergence on this recorded trace. They do **not** yet establish superiority over fixed or random sampling.

## Next — frozen Experiment 11

Before execution, freeze dataset identity, reference definitions, budgets, seeds, model rules, discovery initialization, stopping rules, and metrics.

The required comparison is:

**Uniform Fixed vs Random vs AQIE vs Discovery + Model-aware AQIE.**

Experiment 11 must be committed before its outcome is known.
