# Response to the engine rules audit

The audit ([engine_audit.md](engine_audit.md)) compared the simulation engine with the 2nd-edition living rules (2023). It was done by a separate agent that had not written the engine. This table lists every finding and what was done about it. All fixes were made before the final simulation study.

| ID | Finding | Action |
|---|---|---|
| H1 | Submission at 3:1 was tested after Avoid Battle, so Gauls could escape a forced Submission | **Fixed.** `contact()` now checks 3:1 first (13.3). This matters most for Imperator's SUBMIT mission. |
| M1 | A subjugated Stronghold space could never take an IM or a Tribe | **Fixed.** Placement now checks the marker, not the printed space type. |
| M2 | A lone Roman leader was never displaced when Gauls entered his space | **Fixed (simplified).** He is displaced unless a Roman Walled City shelters him. He does not get an Avoid Battle roll. |
| M3 | Winter attrition hit reduced Legions first, eliminating them | **Fixed.** Full-strength Legions now take the step first, as a Roman player would choose. |
| M4 | Roman supply sources ignored the "trace to a different Roman province" condition | **Fixed.** |
| M5 | "Fading Promises" (Council IMs halved each winter) is in the 2020 rulebook and the 2nd-edition index, but not in the 2023 rulebook body | **Kept**, as in the 2020 rules and the player aid. It is an engine option if errata settle it the other way. The bots' play does not depend on it. |
| M6 | Sorties from a besieged location are not implemented | **Not fixed** (documented simplification). No bot rule calls for a sortie. |
| L1 | Veneti −2 siege modifier applied only on the Veneti space | **Fixed.** It now applies on any port. |
| L2 | Elite reroll timing | Not fixed (rare). |
| L3 | Back-up roll counts the mover's own units for +1 | Not fixed (rare). |
| L4 | Avoider picks its destination before rolling | Not fixed. The bot rule (4.2) picks the destination by fixed priorities, so the order makes no difference to the bots. |
| L5 | Multiple interceptors | Not reachable: both bots declare one stack (4.3). |
| L6 | Isolation: origin space and besieged forts | **Fixed.** |
| L7 | Besieged forts supplied everyone | **Fixed.** |
| L8 | Units left "inside" when their fort was removed | **Fixed** (they are now in the open). The immediate battle is not resolved. |
| L9 | The German tribe never retreats | Not fixed (rare). |
| L10 | Discarding a Surprise used up the card play; Forced March unusable | **First part fixed.** The bots discard Forced March (rules 1.3). |
| L11 | #4 turn limit and Caesar-delayed events enforced only by policies | **Fixed** in the engine. |
| L12 | An intercepting Roman stack used every leader's rating | **Fixed.** |
| L13 | Spring Muster banned Gallic-controlled spaces next to Romans | **Fixed.** |
| L14 | Column shift when attacking Portus Itius from Britannia | Not fixed (rare). |
| L15 | Turn-5 Legion with no arrival space escaped the VP penalty | **Fixed.** |
| L16 | Event details (#13, #17, #20, #21, #23, #41) | #20 (no besieged Legion) and #21 (Council Box allowed) **fixed**. The card text of #13 allows the Submitted box, so it is unchanged. The #17 and #23 "OR" branches follow the bot rules (5.5, 6.5). Militia CS is still fixed at placement. |
