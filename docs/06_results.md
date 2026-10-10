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
