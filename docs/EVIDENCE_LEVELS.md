# Evidence levels

This project uses explicit evidence boundaries.

1. **Implemented** — code exists.
2. **Simulation-tested** — executed against synthetic sensor responses.
3. **Recorded-real-data-tested** — a controller is replayed against previously recorded experimental measurements; this is not live control.
4. **Open-hardware-compatible** — software/firmware interface is designed against the Uncut Gem acquisition path; this is not live validation.
5. **Live-hardware validated** — **not yet achieved**.
6. **Independently replicated** — **not yet achieved**.

## Claim discipline

Recorded-data replay must not be described as live adaptive sensing.

Measurement-count compression must not be equated with wall-clock acquisition-time reduction.

The independent ODMR benchmark uses both:
- the discrete observed minimum (2869.000 MHz), and
- the continuous primary resonance from the frozen full-trace reference fit (2869.729971 MHz).

Live Uncut Gem integration, timing, repeatability, drift behavior, and acquisition-time comparison are proposed validation work, not completed results.
