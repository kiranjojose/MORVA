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

Location context matters most and still helps for vessels never seen in training (−391 m vs motion-only).
Vessel attributes help mostly for vessels already seen (−189 m) and little for unseen ones (−25 m).
