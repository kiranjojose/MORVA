# 09 — Open questions for Kiran (research decisions)

Answer briefly, in your own words. Bullet points are fine. Each answer goes into the methods or protocol, and you
should be able to defend it in an interview.

## A. Must answer before Mon 12 Oct

> **A1 answered 11 Oct** (see `docs/04_methods.md`). RQs and draft hypotheses are in `docs/05_protocol.md`; the
> reading questions are in `docs/02_literature.md` (they supersede the reading guide below).

**A1. Manoeuvring regimes.** Using `results/figures/regime_*.png`, define 2–4 regimes from PAST data only.
Suggested starting point: *straight* (net turn < 1°/min and |ΔSOG| < 1 kn over the last 10 min), *turning*
(net turn ≥ 1°/min), *speed-changing* (|ΔSOG| ≥ 2 kn, e.g. port departure or arrival).
- Do you agree with the 1°/min cut-off (10° in 10 min)? Why, from a ship-handling point of view?
- Should *slow* (< 5 kn, where COG is unreliable) be its own regime?
- Should port proximity be a regime (needs a port list, e.g. World Port Index), or wait for V2?

**A2. Ship-type groups.** DMA has about 20 types. For the context model, group them into about 5 classes. Proposal:
Cargo, Tanker, Passenger (incl. ferries and HSC), Service (tug, pilot, SAR, dredging), Other (fishing, pleasure,
military, unknown). Would you group them differently? (For example, should high-speed craft be their own class?)

**A3. Which context matters most, in your judgment?** Rank before seeing results: vessel type, length, draught,
location, time of day. This is your prior, written down before the experiment, and it makes a good interview story
whichever way the results go.

## B. Hypotheses (freeze by Wed 14 Oct, `docs/05_protocol.md`)

Draft these from the results so far. Keep each one testable and allow for it to be rejected.
- **H1 (learned vs kinematic):** a learned model improves FDE@20 min over CV on validation by at least __ m. What
  improvement would you call *meaningful* operationally? 100 m? 10%? Decide this before seeing the result.
- **H2 (vessel context):** adding type and size improves on motion-only, mainly in the ____ regime.
- **H3 (spatial context):** adding location improves turning-regime error more than straight-regime error.

## C. Application framing (by Thu 15 Oct)
- One sentence: why YOU (naval architecture + CS + industry) for this PhD topic?
- Which result would you lead with in the cover letter?
- Repo public on 15 Oct. Remove the proposal PDF/DOCX from history first (yes/no)?

---

# Reading guide for R1–R4

For each paper, fill one row of `references/literature_matrix.csv` (20–30 min per paper: abstract, data/method
section, results tables, limitations). Extract:

| Column | What to look for | Why it matters for VesselMind |
|---|---|---|
| dataset | Which AIS source and region? **Danish waters?** How many days and vessels? | Comparability; reviewers will ask |
| sampling | Resampling interval, how gaps are handled | Our 1-min / 180 s rule |
| baseline | **Do they compare against constant velocity at all?** Kalman? CTRV? | If not, our CV finding is a contribution |
| split | Random points, by trajectory, or by time? | Random splits leak; ours is time-block |
| horizon / metrics | Horizon in minutes, ADE/FDE in metres or another unit | Can we put our numbers next to theirs? |
| features | Motion only? Ship type, size, location? | Our context ablation |
| regime | Do they separate straight vs turning? | Our regime breakdown |
| limitations | What do they admit doesn't work? | Gaps we can address |

Three questions to answer in your own words after reading all four:
1. What is the *standard* way people evaluate AIS trajectory prediction, and what is wrong with it?
2. Is "constant velocity is hard to beat at short horizons" known, and is it ever shown by regime?
3. Where does ship-type or ship-size context appear in the literature, and does it help?
