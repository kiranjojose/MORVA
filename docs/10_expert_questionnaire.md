# 10 — Expert input: questionnaires

**Is expert input needed?** Not for V1 results: the data and protocol stand on their own. It is valuable for three
things: (1) grounding the regime definition and anomaly types in practice, (2) interpreting failure cases, and
(3) the interview, where "I validated my assumptions with navigators and class surveyors" is a strong signal of
research maturity. Aim for 3–6 short responses this week. Even informal answers count, if documented.

**Ground rules (put these in the message you send):**
- About 10 minutes, informal, for an independent research project (not for any employer).
- Do not share confidential company, vessel or client information. General experience only.
- Answers are summarised anonymously (role + years of experience only), unless they ask to be credited.
- Store answers in `docs/expert_input/` (git-ignored if anyone asks for privacy) with date, role, years.

---

## Q1: Navigators / deck officers / pilots (most important)

*Context: I'm studying how ships move in Danish straits (Great Belt, Øresund) using historical AIS data. The goal is
to predict a ship's position 5–20 minutes ahead and to flag unusual behaviour.*

1. Role and years at sea? Ship types you have sailed on?
2. In a strait like the Great Belt, how long does a typical course alteration take, from starting the turn to
   steady on the new course? Does it differ between a large tanker and a ferry?
3. When you see another ship start to turn, how do you judge whether it will keep turning or straighten out?
   What information do you use (chart, the fairway, its type, VTS, AIS destination)?
4. Roughly what rate of turn do you consider normal for a course alteration at sea speed? And for harbour
   manoeuvring?
5. Which AIS fields do you trust least in practice (heading, COG at low speed, draught, destination, ship type)?
6. What behaviour in AIS would make you think "something is unusual" here? (For example, slowing in the fairway, a
   sudden course change, drifting, stopping outside an anchorage.) Which of these are actually *normal* in practice?
7. Where in Danish waters do ships behave least predictably, and why?
8. If a tool showed you a predicted position for another ship 10 minutes ahead, what accuracy would make it
   useful? What would make you distrust it?

## Q2: Naval architects (design / production)

1. Role, years, ship types designed or built?
2. Which ship particulars most strongly govern manoeuvring behaviour (L, B, T, block coefficient, rudder area,
   propulsion type)? Which of these could plausibly be approximated from AIS length, beam and draught?
3. IMO manoeuvring standards (MSC.137(76)) give limits such as tactical diameter < 5 L. In your experience, how
   close do real ships operate to these limits in normal service turns?
4. How much does loading condition (draught, trim) change turning and stopping behaviour? Is AIS draught (entered
   manually by the crew) good enough to capture that?
5. Would grouping ships by type and length (e.g. < 100 m, 100–200 m, > 200 m) capture the main manoeuvring
   differences, or is something else more important (twin screw, azimuth thrusters on ferries)?
6. Which simple physical constraints would you expect a credible prediction model to respect (maximum rate of
   turn vs speed and length, maximum deceleration)?

## Q3: Classification society surveyors

1. Role, years, which surveys (newbuilding, in-service, flag)?
2. Which data about vessel operation do owners, class or authorities actually use today? Is AIS used in any survey,
   incident or risk process you know of?
3. How reliable is AIS static data (type, dimensions, draught) in your experience? Common errors?
4. Which unusual operating patterns would matter for safety or class (e.g. operating outside the design envelope,
   repeated heavy manoeuvring, groundings or near-groundings in specific areas)?
5. Where could a validated behaviour model add value in class or flag work, and where would you consider it
   inappropriate or overreaching?
6. What would make you trust, or reject, a data-driven indicator of abnormal vessel behaviour?

## Q4: Commercial / sales (optional, for the long-term startup question only)

1. Who in a shipping company, port or authority would care about short-term traffic prediction or behaviour
   anomalies? Who owns that budget?
2. Which existing products do they use (MarineTraffic/Kpler, Windward, Spire, VTS systems)? What is missing?
3. Would a regional, physics-aware behaviour model be interesting, or is AIS analytics seen as a commodity?
4. Which data would customers be willing to share (engine, fuel, voyage plans), and under what conditions?

---

## How the answers get used
| Answer | Used in |
|---|---|
| Q1.2–Q1.4, Q2.3 | Regime thresholds and the turn-persistence interpretation (`04_methods.md`) |
| Q1.5, Q3.3 | Data card: field reliability (`03_data_card.md`) |
| Q1.6, Q3.4 | Anomaly types for the synthetic benchmark (E5) |
| Q2.2, Q2.5, Q2.6 | Vessel context grouping; plausibility constraints (V2/V3 physics-informed work) |
| Q1.8, Q3.5–3.6 | Discussion section and interview narrative |
| Q4 | Startup notes only, not the research report |
