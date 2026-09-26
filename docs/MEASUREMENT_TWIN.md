# ODMR Measurement Twin

This is a thin abstraction over the existing Adaptive ODMR implementation. It
does **not** introduce a second algorithm or a new evidence claim.

The existing modules already implement the pieces:

- sensor backends -> observed or simulated measurement
- ODMR model bank -> expected response
- residual diagnostics -> model/measurement reconciliation
- adaptive selector -> next informative setting
- controller -> closed measurement loop

The twin layer makes that state explicit:

**MODEL -> MEASURE -> RECONCILE -> ASSESS -> SELECT NEXT MEASUREMENT**

## Current instantiated hierarchy

1. Physical/sensor response: NV ODMR trace or simulated Uncut Gem response
2. Sensor/response model: Lorentzian model bank
3. Acquisition interface: indexed `measure(index)`
4. Processing/inference: nonlinear fitting + AICc model selection
5. Adequacy: prediction residual diagnostics
6. Decision: information-directed next-setting selection

This is the first concrete instantiation of the broader Hierarchical
Measurement-System Twin concept.

## Evidence boundary

The abstraction reuses existing evidence. It does not convert recorded-data
replay into live-hardware validation. Live instrument state, timing, drift,
latency, calibration changes and repeated-acquisition noise remain future
hardware-validation concerns.
