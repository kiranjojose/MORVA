# 06 — Results

> All numbers below are **validation (1–3 Oct 2026), preliminary**. The test split (4–6 Oct) is locked until the
> hypotheses are frozen. Source: `results/tables/baselines_val.md`, `results/tables/gbm_ablation_val.md`.

## E2: Kinematic baselines (62,982 windows, 692 vessels)
| Model | ADE (m) | FDE@20 min (m) |
|---|---|---|
| Persistence | 2,899 | 5,413 |
| Constant velocity (CV) | **640** | **1,574** |
| CTRV | 837 | 2,042 |
| Damped CTRV (τ tuned on train) | 643 | 1,578 |

Extrapolating the current turn rate makes predictions worse (+468 m FDE vs CV). Turns in this area rarely persist
over 20 minutes.

## E3/E4: Learned residual model and context ablation
| Model | Features | FDE@20 min (m) | vs CV |
|---|---|---|---|
| A | motion | 1,273 | −19% |
| B | + vessel (type group, length, beam, draught) | 1,131 | −28% |
| C | + location (position, course) | 864 | −45% |
| D | all | **827** | **−47%** |

Stable across seeds 0–2 (sd ≤ 5.3 m).

## Generalisation: vessel-held-out evaluation
Training without any validation vessel (109,866 train windows), compared with a random training subset of the same size:

| FDE@20 min (m) | Full training | Same-size random subset | **Vessel-held-out** |
|---|---|---|---|
| CV | 1,574 | 1,574 | 1,574 |
| A motion | 1,272 | 1,295 | 1,452 |
| B + vessel | 1,130 | 1,157 | 1,435 |
| C + location | 865 | 904 | 1,171 |
| D all | 823 | 861 | **1,163 (−26% vs CV)** |

- **Location context generalises to vessels never seen in training** (−281 m vs motion-only, 95% CI −312 to −252).
- **Vessel attributes do not measurably help new vessels** (−17 m, CI −35 to +1). Their gain in the standard setup comes
  from recognising known vessels.
- Cargo and tanker gains are unchanged under held-out (D: 553 / 642 m); passenger-vessel gains mostly disappear (944 →
  2,162 m). Ferry prediction relies on having seen the same route operator.

## E2–E4 by past-only manoeuvring regime (`results/tables/regimes_val.md`)
Regime shares (val): steady 52%, turning 23%, low-speed 16%, combined 7%, speed-changing 2%.

| FDE@20 min (m) | Low-speed | Steady | Turning | Speed-changing | Combined |
|---|---|---|---|---|---|
| CV | 1,587 | 1,190 | 1,836 | 2,734 | 3,104 |
| CTRV | 1,788 | 1,301 | **3,257** | 2,971 | 3,800 |
| A motion | 1,072 | 1,105 | 1,501 | 2,028 | 1,959 |
| D all | 871 | 656 | 927 | 1,449 | 1,448 |

- **H1-direction:** motion-only learning helps most outside steady transit (A − CV: steady −85 m; combined −1,145 m).
- **Location (C − A)** improves every regime (−170 to −511 m), largest when turning. Holds in **50/50** regime ×
  threshold-sensitivity cells (95% CI excluding zero).
- **Vessel-held-out:** location still helps strongly for steady (−358 m) and turning (−362 m), less for combined
  (−135 m), and **not at low speed** (+24 m, CI 0 to +48). Harbour and low-speed behaviour seems to be vessel- or
  route-specific. Vessel attributes help little for unseen vessels and **hurt at low speed** (+66 m).
