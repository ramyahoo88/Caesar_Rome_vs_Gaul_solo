# Caesar: Rome vs Gaul engine audit (2E living rules 2023-1d)

Scope: `engine.py`, `events.py`, `cards.py` and `map.json` in `/home/claude/caesar/code`, which are identical to `code_v1_frozen`. I checked them against the 2E rule PDF section by section and used the counter and map art in `vmod_raw/images` for printed values. The 1E battle and siege tables and the `siege_shift` approximation are noted, not counted as defects. Known simplifications are not reported.

## Findings

| ID | Rule | Sev | Rule says | Code does | Fix |
|---|---|---|---|---|---|
| H1 | 13.3.1–13.3.2 | High | Submission at 3:1 is mandatory. 13.3.2 ends "If the odds are less than 3-1 and the Gallic Army does not Avoid Battle, continue to Battle", so the 3:1 check comes before Avoid Battle. *(Inferred, but strongly.)* | `contact()` (engine.py:932-951) offers Avoid Battle first, and the 3:1 test only runs in `battle()` (984-988). Both policies always avoid at 3:1 (bots.py:1106, policies.py:255), so Gauls escape forced submission about 42–58% of the time. | In `contact()`, when `side=='R'`, compute both Battle Strengths for `out` before the avoid step. At 3:1 or better, submit and return `'continue'`. |
| M1 | 8.3.1, 5.1.2A, 14.7.1, 16.5 | Med | Only a space that *contains* a Stronghold marker is barred to IMs and tribes. Once the stronghold is subjugated, the space is open again. A Stronghold comes back when a Gallic IM sits there in winter. | `can_place` (engine.py:559) tests the printed `STYPE`, and `legal_tribe_spaces` (1377) requires `STYPE=='town'`. A subjugated space can never take an IM or a tribe, so the 14.7.1 return path is effectively dead. Rome also cannot add IMs there, which matters for Nervii, Atrebates and Treveri control. | Test `ctype[s]=='SH'` instead of `STYPE`. |
| M2 | 9.6 | Med | A lone Roman leader in a space that Gallic CUs enter must avoid battle or shelter in a Roman WC, or else be displaced. If Caesar is displaced, Rome loses 3 IMs. | `contact()` (engine.py:920-923) returns `None` when no Roman CU is present. Lone leaders are never displaced by Gallic entry. | Handle the case `enemy=='R'` with leaders but no CUs: shelter in a Roman WC, or roll to avoid, or else `displace()`. |
| M3 | 16.2.3, 19.2.2 | Med | The Roman player picks which legions suffer winter attrition (1 step each). Each eliminated legion costs 1 VP. | engine.py:1790 sorts by `(steps, …)`, so reduced legions take the losses first and are eliminated. This is the worst possible choice, and the Roman player gets no say. | Hit full legions first, or ask the policy. |
| M4 | 15.2 | Med | A Roman control marker in a Roman province is a supply source only if it can trace supply to a *different* Roman-controlled province. A Roman WC is always a source. | engine.py:412-414 treats every Roman-controlled space in any Roman province as a source. | Add the trace check between Roman provinces. |
| M5 | 18.4 | Med | The 2023 body stops at 18.3. Only its index still lists "Fading Promises". The 2020 v1.1 book (served by the "1E" URL) halves Council IMs, rounded up, at End of Winter. | engine.py:1748-1749 always halves them. | Make it an option, off for 2023 2E, or confirm with errata. |
| M6 | 14.5.2, 14.6 | Med | Besieged units leave only by Sortie, which is voluntary and attacks the besiegers. A Sortie that loses retreats back inside. | `activate` (engine.py:680) drops besieged units, and the `sortie` argument of `battle()` (977) is never used. A besieged tribe or legion can never break out. | Add a sortie action: battle in place, and on a loss retreat inside. |
| L1 | 11.3.4/14.3.5 | Low | The -2 DRM applies to a Veneti FT "on a Port space" unless Rome has Naval Supremacy in Oceanus Atlanticus. The PAC wording is "the Veneti Port space", so this is ambiguous. | engine.py:1192 applies it only on the space named Veneti. Namnetes is also a port. | Use `PORTS[s]` for any Veneti FT. |
| L2 | 13.5.3 | Low | The Elite reroll can be used only after *both* sides have spent their leader rerolls. | engine.py:1076/1079 only checks the side's own rerolls. | Also require the opponent's count to be 0. |
| L3 | 12.2.2, 12.3 | Low | Back Up is an Avoid Battle roll. Remedies can modify it. | engine.py:893 calls `ia_roll` into `frm`, where the mover's own units always earn +1. Remedies is not offered. | Exclude the movers when testing for friendly CUs, and pass the surprise hook. |
| L4 | 12.3 | Low | The avoider may roll first and pick the destination afterwards, which lets it dodge the -2 rough modifier or take the +1. | engine.py:935-943 makes the avoider pick the destination before rolling. | Roll first, then filter destinations by the modifiers. |
| L5 | 12.2.4, 12.1.3 | Low | A stack that has just intercepted may not then avoid. All declared interceptors roll, and the successful ones combine. | Avoid is not blocked for interceptors (engine.py:932). `intercept_check` returns after the first success (872-895). This is latent, since current policies declare only one stack. | Mark interceptors as unable to avoid. Resolve every declared stack. |
| L6 | 16.3 | Low | The isolation path cannot *enter* a space with an enemy CU. A besieged fort is not a valid destination. | engine.py:1810-1824 applies `ok()` to the IM's own space, so an IM shared with an enemy CU is always removed. It also seeds besieged forts as anchors (1803). | Exempt the origin space. Drop besieged forts as anchors. |
| L7 | 14.5.4 | Low | A besieged location supplies only the units inside it. | `supplied_spaces` (engine.py:405-433) seeds besieged WCs and FTs as general sources. | Skip besieged sources. |
| L8 | 11.2.4 | Low | When an FT is removed by tribe elimination or submission, any Gallic CUs it was protecting fight an immediate battle. | The `clear_ctrl` path (engine.py:482-485, 497-499) leaves those CUs with `inside=True` and no fort. They then cannot be attacked or besieged. | Clear `inside`, then trigger a battle. |
| L9 | 17.4 | Low | General battle and retreat rules apply to the German tribe. | engine.py:1052 means the German never retreats, so it can share a space with the Roman army that beat it. | Retreat it, or eliminate it if no retreat is possible. |
| L10 | 7.5.4, cards | Low | Surprise cards don't count as a card play. Forced March (#55) gives +1 MP. Vow to Mars (#52) can be used by either side. | Picking a surprise card uses up the round (engine.py:1646-1648). `forced_march` is never passed in, so #55 does nothing. The Vow +1 siege bonus is Roman-only (1227). | Fix all three. |
| L11 | 5.4, card #4 | Low | No event that activates Caesar while he is delayed. #4 is limited to Turns 1–4. | `event_allowed` (engine.py:1330) enforces neither. Only the policies do (bots.py:157,162; smart.py:514). | Enforce both in the engine. |
| L12 | 12.1.4 | Low | The interceptor's commanding leader sets the DRM. | When Rome intercepts with `lead=None`, `army_br` (engine.py:874 calling 625) uses *every* leader in the origin space, so a Caesar who stays behind still gives +3. | Pass `[]` for the leaders. |
| L13 | 6.2, 12.1.1 | Low | Muster may not enter a space where interception is possible. Rome cannot intercept into a Gallic-controlled space. | `muster_ok` (engine.py:1566-1570) bans every space next to a Roman unit. | Allow Gallic-controlled spaces. |
| L14 | 17.1.2 | Low | Rome shifts 1 column left when attacking Portus Itius from Britannia. | Not implemented. | Add it. |
| L15 | 5.2.3 | Low | n/a | A Turn-5 legion with no legal arrival space goes to `'elim'` without being added to `elim_legions` (engine.py:1464), so it escapes the VP penalty. | Append it to `elim_legions`. |
| L16 | events | Low | #21 places per 5.1.2, Council Box included. #20 can't restore a besieged legion (14.5.3). Militia CS is the *current* count (17.6). | #21 passes `allow_council=False` (events.py:150). #20 allows besieged legions (143). Militia CS is frozen at placement (246). #13 can restore a Submitted tribe (91). #17 and #23 never offer their "OR" branch (109, 172). | Fix each as described. |

## Map sanity (map.json)

- The graph has 117 spaces and 275 edges (258 path, 16 rough, 1 channel). It is connected, with no duplicate edges, and every province is contiguous.
- `need` was computed as `len//2+1` (work/build_map.py:78). All 26 values still match the superscripts printed on the map image.
- The degree-1 spaces, Germania's rough links, the German entry arrows and Brigantium as the "To Rome" link all match the map. WC garrisons match the Massilia and Narbo counters.
- Cosmetic: the space stored as "Treveri" is printed "Treves".

## Events spot-checked against cards.py (21)

These matched: #1, #3, #6, #7, #8, #9, #10, #12, #14, #18, #19, #22, #27, #28, #31, #39, #43, #44, #45, #48 and #50. The deviations in #4, #13, #17, #20, #21, #23 and #41 are listed above. Note that cards.py's `ap2` distribution (44×2, 5×3, 3×1, 3×0) matches the 2E change note. Which particular cards carry the 3s and 1s is still an assumption.

## Verified correct

- **Setup (3.x):** all of it, including the 2E extra Roman IM at Bibrax.
- **Counter values:** all match the counter art. The upgraded FT really is garrison 3 with -1, and a Roman WC has -1.
- **Tables:** battle and siege tables match the PAC cell for cell.
- **Battle:** Roman dice minimum of 3, asterisk tie-break, attacker retreats on a tie, 13.6.1 excess-hit reduction, 13.7 retreats and penalties, and 13.8 continue-moving.
- **Interception and avoid:** 9+, leader BR, +1 friendly (2E), -2 rough, channel and besieged exclusions, and avoid-destination limits.
- **Siege and subjugation:** odds columns, 3:1 submit or surrender, one roll per card, 2 MP, Caesar +1, siege lifting, 1.5-1 column with CS 2 minimum and 3 SP, and the Caesar's Pass VP.
- **Control and influence:** province control, adjacency, conversion, 2-MP removal, and Local Support.
- **Reinforcements:** draw 4 keep 3, Council displacement, Arverni release, replacements and emergency steps, Turn-5 legions, Caesar's single delay, and legates.
- **Supply and winter:** supply attrition rules, forage levels, Isolation order, governance table and VP, end-of-winter IMs and Strongholds.
- **Victory:** auto-victory, and the 12-VP formula.
- **Naval Supremacy:** port majority, with Sinus Gallicus always Roman.
- **Germania and Britannia:** native attacks (CS 9/7), Storms at Sea, and the 2+2 VP.
