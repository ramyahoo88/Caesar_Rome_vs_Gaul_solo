# Caesar: Rome vs. Gaul — Solo Bots

## Imperator (Rome) and Concilium (Gaul) · version 1.0

Two card-driven paper opponents for *Caesar: Rome vs. Gaul*, 2nd edition (GMT Games). You play one side; the bot plays the other with the same cards, units, dice and rules as a human. Its hand stays face down. It never looks at yours. It rolls only the dice the game rolls.

**You need:** the game; this booklet; the reference sheet; the 9 Directive cards for the bot you face (Imperator or Concilium), cut out and shuffled face down; this booklet's Event Guide.

Unofficial fan variant, not a GMT publication. Rule numbers (5.1.2, 13.3 and so on) refer to the 2nd-edition rulebook.

---

## 1. Setup and the bot's hand

1.1 **Setup.** Use normal setup (3.0). If the bot is Rome, Caesar's army starts in **Bibracte**. Draw the Legates normally.

1.2 **Deal.** Deal the bot its cards face down. Do not look at them. Shuffle them before every bot card play.

1.3 **Reserve.** Surprise cards (#52, #54, #55) and the Reaction card (#24) never enter the Offer (2.2). When you reveal one, put it face up beside the bot as its **Reserve** and reveal another card instead. Reserve cards still count as part of the bot's hand. The bot uses them as follows:

| Card | The bot uses it |
|---|---|
| #24 You May Believe What You Wish | To cancel your Event or Bonus Event if the card is on its Cancel list (5.4, 6.4). It is played for AP only if it is the bot's last card. |
| #52 A Vow to Mars | In its next battle where the two Battle Strengths differ by 3 or less (one extra reroll). If Rome, on its next siege roll if no such battle comes first (+1). |
| #54 Remedies for all Contingencies | +2 to its own next Avoid Battle or Interception roll. |
| #55 Forced March | Discarded at the start of the bot's next card play; it draws a replacement. |

When the bot has only Reserve Surprise cards left, it discards them and draws replacements (7.5.4). At the end of the Strategy Phase, discard what is left.

---

## 2. The bot's card play

Each time it is the bot's turn to play a card:

2.1 **Directive.** Turn over the top card of the bot's Directive deck. It gives a **mission order** and a **compass** (N, S, E or W). When the deck runs out, reshuffle all nine.

2.2 **Offer.** Shuffle the bot's hand (not the Reserve) and reveal two cards. This is the **Offer**. If it has one card, that card is the Offer.

2.3 **Choose the card.** Take the first that applies:

1. A card whose Event is **★** in the bot's Event Guide **and Live**. If both are, go on to the next step with those two.
2. The card with the higher AP value.
3. If still tied, the card whose Event is Live.
4. Otherwise, the first card revealed.

Return the other card face down.

2.4 **Event or AP.** If the chosen card's Event is **Live** for the bot (Event Guide), play it as the Event. A Bonus card gives its Event and then its AP. Otherwise, play the card for its Action Points.

2.5 **Spend each AP.** For each Action Point, work down the list below. Do the first mission that *can* be done. It costs 1 AP; a Major Uprising costs 2. If nothing can be done, the remaining AP are lost.

* **Imperator:** CONTINUE, PROTECT, SUBMIT, REGROUP, then the Directive's missions in order, then GATHER, then CONTROL.
* **Concilium:** the Directive's missions in order, then AGITATE.

The bot never takes its Event and AP from the same card except for Bonus cards (7.5).

---

## 3. Words used by both bots

**Army.** The bot forms its armies afresh for each mission, from units that have not moved this card play:

* **Imperator:** each Roman leader (Caesar first, then Legates by Battle Rating, highest first) with up to his Command Rating of CUs from his space, strongest first; then each other Legion stack (up to 2 Legions).
* **Concilium:** each Gallic leader (Vercingetorix, then Ambiorix) with up to his Command Rating of CUs from his space, strongest first (Ambiorix: Belgic Tribes and Mercenaries only); then each other Tribe or the Minor Tribe, with the strongest other Tribe or Mercenary in its space. A Gallic leader's own CS counts in his army's BS.

**Ties between armies.** If two armies could carry out a mission against the same target equally well, the stronger army goes; if they are equally strong, the one listed first above goes.

**Reach.** Spaces an army can enter this activation with its MA, paying 1 MP per path and 2 per rough path or Channel crossing, +1 per space if it carries more CUs than its Command Rating (9.3). A space with enemy CUs outside a fortification ends the move.

**Battle Strength (BS).** Combat Strength plus Local Support (13.2). When a bot sizes up an attack on enemy CUs standing outside, it counts *every* enemy CU in that space, including any inside a fortification, because they may come out to fight.

**Odds.** Attacking BS ÷ defending BS. For a siege, the attacker is every Roman CU in the space (the army plus any already there), and the defender is the Garrison plus every Gallic CU in the space, inside or out (14.3.2).

**Compass.** When choices tie, take the one farthest in the Directive's direction (N = nearest the top edge of the map).

**Path.** An army always moves by the cheapest route. If two routes tie, use the compass.

**Danger.** Whether a space is safe to end a move in:
* **Imperator:** a Roman army is *in danger* in a space if a Gallic army (formed as Concilium forms its armies) could reach that space on its next activation with a BS at least 1.5× the BS of all Roman CUs there, the army included. A space with a Roman Walled City is never dangerous. Caesar's army ignores danger.
* **Concilium:** a Gallic army is *in danger* in a space if a Roman army (formed as Imperator forms its armies) could reach that space on its next activation with a BS at least equal to the BS of all Gallic CUs there, the army included. A space with a Gallic Fortified Town is never dangerous.

**Removing an IM** costs 2 MP in the space (8.3.3). **A siege roll** costs 2 MP (10.4.2). No location takes more than one siege roll per card (14.3.4).

---

## 4. Reactions (both bots)

4.1 **Inside or outside.** When an enemy army enters a space where the bot's units can shelter in its own Fortified Town or Walled City, they go **inside** if the enemy's BS is at least theirs. Otherwise they stay outside and fight.

4.2 **Avoid Battle.** The bot tries to avoid when the enemy's BS is at least 1.5 times its own. It moves to the adjacent space that is friendly-controlled, then one with its own CUs, then by compass.

4.3 **Interception.** Imperator intercepts if its stack plus any Roman CUs already in the target space have at least 2× the mover's BS. Concilium needs 1.5×, or 2× if Caesar is moving. Only one stack tries: the strongest. Units inside a fortification neither intercept nor count.

4.4 **Backing up.** When intercepted, the bot tries to back up (12.2.2) if its army's strength is less than the enemy's in the space.

4.5 **Rerolls.** When it is the bot's turn to reroll (13.5): it rerolls its own lower die if that die shows 3 or less (Rome's 1s and 2s already count as 3). Otherwise, it makes you reroll your higher die if that shows 5 or 6. Otherwise, it passes.

4.6 **Losses.** First, flip full-strength Legions or Tribes (non-elite first, weakest first). Then lose Mercenaries. Then lose reduced units, weakest first. Lose a Gallic leader only if nothing else is left.

4.7 **Retreats.** Retreat into its own fortification in the space if it can. Otherwise, go to the adjacent space that has no enemy CUs, then one that is friendly-controlled, then one with its own CUs, and never across the Channel if another space is open.

---

## 5. Imperator (the Roman bot)

### 5.1 Missions

Each mission says which army acts. *Target order* lists the tie-breaks in turn; the last tie-break is always the compass.

**CONTINUE.** A leader's army already in a space whose Fortified Town (or Stronghold) has at least 1 Siege Point, with no Gallic CUs outside, rolls on the Siege Table again. It needs odds of at least 1:2 (a Stronghold: CS 2+), and the location must not have been rolled against yet this card.

**PROTECT.** Only if a Provincia province is not Roman-controlled, or Gallic CUs stand outside in Provincia:
1. An army that can reach Gallic CUs in Provincia with at least equal BS attacks them. *Target order:* a 3:1 attack; the largest Gallic BS; the nearest.
2. Otherwise, if a Provincia province is lost, an army SWEEPs Gallic IMs in the lost provinces (5.3).
3. Otherwise, if a Provincia province is lost, it places an IM in a Provincia province Rome does not control, Narbonensis first (Control Table line 2). PROTECT never places an IM during an Activation Event (5.5).

**REGROUP.** Only if a Roman army other than Caesar's is in danger where it stands. It moves to a space it can reach, with no Gallic CUs outside, where it is not in danger: Caesar's space first; then the space with the most Roman BS; then the nearest. If several armies are in danger, the one facing the highest ratio of Gallic BS to its own goes first.

**SUBMIT.** An army that can reach Gallic CUs (outside) with at least **3×** their BS attacks them, so they must Submit (13.3). *Target order:* the largest Gallic BS; the nearest. If a Gallic Fortified Town is in that space and MP remain, roll a siege as well.

**SIEGE.** An army that can reach a Gallic Fortified Town with at least 2 MP left marches there and rolls. Only these targets count:
* a Town that must **surrender** (odds 3:1 or more); any army may go, and a leaderless Legion stack may take a third Legion over its Command Rating for this;
* a Town with **2 or more Siege Points** where the odds are at least 1:1 (leader's army);
* any Town where **Caesar's army** has odds of at least 2:1.

If Gallic CUs stand outside the Town and it will not surrender, leave it to STRIKE. Until Caesar's Pass is opened, a leader's army with CS 2+ may also subjugate **Octodurus**, after all Town targets.
Skip any location already rolled against this card.
*Target order:* a surrender; a Town in or next to a space with a Roman control marker; most Siege Points; in Celtica; best Siege Table column; nearest.

**STRIKE.** An army attacks Gallic CUs (outside) it can reach with at least 2× their BS (Caesar's army: 1.5×). *Target order:* a 3:1 attack; the largest Gallic BS; the nearest. If a Gallic Fortified Town is in that space and MP remain, roll a siege as well.

**RAID.** An army SWEEPs (5.3) Gallic IMs with these weights:
* 4: in a Gallic-controlled province in Celtica, or in Provincia;
* 3: in a Gallic-controlled province elsewhere;
* 2: in a province with no Fortified Town where Rome is one IM short of control or already has control;
* not at all: anything else, including Germania and Britannia.

**INVADE.** From Turn 3, if Caesar has not moved and his six strongest CUs have CS 12 or more: if Caesar can reach a Gallic IM in Britannia or Germania with 2 MP left, he takes those six there and removes it. Otherwise, he marches toward the nearest such IM, but only if he ends closer.

**GATHER.** A leaderless Legion stack that can reach a space with a Roman leader moves there (the nearest).

**RULE.** Lines 0–3 of the Control Table.

**SETTLE / CONTROL.** The whole Control Table.

### 5.2 Control Table (Imperator)

Take the first line that gives a legal Place or Convert (8.3). Among spaces on that line, take the **lagging region** first, then the other of Celtica and Belgica, then Aquitania, Provincia, Germania and Britannia, then the compass.

**Lagging region:** of Celtica and Belgica, the one where Rome does *not* control more provinces than Gaul. If that is true of both, take the one where Gaul's lead (Gallic minus Roman provinces) is smaller. If it is true of neither, or there is still a tie, take Celtica.

0. **Presence.** If Rome has no space in Aquitania, Belgica or Celtica (checked in that order), convert a Gallic IM there; else place there.
1. **Convert** a Gallic IM in a space with a Roman CU. Prefer Gallic-controlled provinces.
2. **Provincia.** Place an IM in a Provincia province Rome does not control. Narbonensis comes first.
3. **Gain.** Place an IM that gives Rome control of a province of Gaul: one IM short, no Fortified Town, not already Roman.
4. **Deny.** Place an IM in an uncontrolled province of Gaul where Gaul is one marker short of control.
5. **Advance.** Place an IM in a province of Gaul with no Fortified Town that Rome does not control; the province needing the fewest more IMs comes first, then the region order.
6. Place anywhere in Gaul, next to the most Roman control markers; then anywhere legal.

### 5.3 SWEEP

Pick the **target and the army** together: the highest-weight IM, with no enemy CU in its space, that some army can reach with at least 2 MP left. Judge all weights at the start of the mission. Among equal weights, take the IM an army reaches for the fewest MP; then the army with the most MP left over; then the stronger army; then the compass (for the IM).

That army moves there and removes the IM. **Danger:** an Imperator army other than Caesar's, and every Concilium army, never sweeps into a space where it would be in danger (3). While it has MP, it steps to an adjacent space with a wanted IM (highest weight, then compass) and removes that one too. Each step costs the path cost plus 2.

### 5.4 Event Guide (Imperator)

★ = priority Event (2.3). *Live* = the condition that makes the bot play the Event. A target that does not exist means the Event is not Live. Gallic-only Events are never Live for Imperator.

| # | Card | Live when | ★ |
|---|---|---|---|
| 1, 2 | Veni Vidi Vici; Constant as the Northern Star | Caesar is on the map | ★ |
| 3 | Aid From Pompey | at least 2 steps can be restored (reduced Legions with a path to Rome; an eliminated Legion counts 2) | ★ |
| 4 | Aid From Crassus | Turns 1–4 | ★ |
| 9 | Destroyed Root & Branch | it would remove 2+ Gallic IMs | |
| 10 | The Reach of Rome | always | ★ |
| 11 | For the Glory of Caesar | always | ★ |
| 12 | Roman Rule | Celtica or Belgica has 3+ provinces with a Roman IM | |
| 17 | Caesar's Lieutenant (Bonus) | always | |
| 18, 19 | Hostages; Roman Trade (Bonus) | a target exists | |
| 20 | Roman Auxiliaries (Bonus) | a reduced Legion has a path to Rome | |
| 29, 30 | German Auxiliary Cavalry (Bonus) | a Germani Cav is available and a Legion qualifies | |
| 31 | A Friend of Rome (Bonus) | a target exists | |
| 32 | Caesar's Legions (Bonus) | a Legion stack has no leader | |
| 33, 46 | Local Raids (Bonus) | a target exists | |
| 34, 35 | German Migration (Bonus) | always (the Germans move only as in 5.5) | |
| 37, 38 | Motus Ubique | Roman units in 3+ Regions | |
| 39, 40 | Incite Through Sedition; Unrest Spreads (Bonus) | a target exists | |
| 44 | Legate Called to Rome (Bonus) | a Legate with Battle Rating 0 is on the map | |
| 45, 48 | Diplomacy; Roman Bribes | a target exists | |
| 50 | Naval Supremacy | Rome is besieging a port location and has Naval Supremacy in one of its sea zones | |
| 51 | Stratagem & Treachery (Bonus) | Rome is besieging a location | |
| 47 | Winter Campaign | never: Imperator never interrupts; the card is 1 AP | |
| 49 | Three Days March | never | |

**Cancel list (#24):** Gallic #5, 6, 8, 14, 16, 21, 27, 36, 43, 53.

### 5.5 Event choices (Imperator)

* **Influence actions** in Events (#10, #12 and others): use the Control Table, limited to the spaces the Event allows. For #12, choose the Region with more Roman IMs.
* **Remove or convert a Gallic IM:** take the highest RAID weight (5.1), counting any other IM as 1.
* **Activation Events.** When one leader is activated (#1, #2, #17), his army does the first of PROTECT, SUBMIT, CONTINUE, SIEGE, STRIKE, INVADE (Caesar only), RAID that it can. When several armies are activated (#11, #32, #37, #38), repeat this: find the first mission in the list PROTECT, SUBMIT, CONTINUE, SIEGE, STRIKE, INVADE, RAID, GATHER that *any* activated army that has not yet acted can do, and do it (the mission picks the army). Stop when none can act. #32 activates only Legion stacks in spaces with no leader. #37 and #38 activate at most one army per Region. #1 then activates the Legate with the largest stack (then the highest Battle Rating).
* **#17:** if Labienus is in the cup, place him with the largest Legion stack that has no leader (if there is none, with Caesar) and return the lowest-rated other Legate. Otherwise, activate the Legate not with Caesar who has the largest stack (then the highest Battle Rating).
* **#20:** restore the reduced Legion with Caesar first, then the one in the largest stack.
* **#29, #30:** put the Cavalry with Caesar if possible, otherwise with the largest qualifying Legion stack.
* **#34, #35:** bring the Germans in only through an entry space holding a Gallic IM. Move them to a space within 3 MP that holds a Gallic IM (highest RAID weight). If there is none, they do not move.
* **#44:** swap the Legate with Battle Rating 0.
* **#50, #51:** add a Siege Point where Rome has the most points.

### 5.6 Imperator between card plays

* **Replacements** (5.2): restore a reduced Legion with Caesar first, then in the largest stack; then rebuild an eliminated Legion with Caesar. Imperator never takes Emergency replacements.
* **Turn 5 Legions:** they go with Caesar if he qualifies, otherwise with the largest qualifying stack.
* **Caesar** (5.3): place him with the largest Legion stack in a friendly space with a path to Rome.
* **Legates** (5.4): each goes to the largest Legion stack without a leader, otherwise with Caesar.
* **Winter camp** (16.2.2): legions move one at a time, full-strength first. Each goes, within 3 MP, to the first of these with room under its forage level (16.2.4); room counts only the Legions already moved there this Winter:
  1. a neutral space in Gaul next to a Roman control marker;
  2. a Roman IM space in a Roman province;
  3. a Roman Walled City;
  4. another Roman IM space;
  5. any neutral space in Gaul.
  Take the nearest, then the most northern.
* **Kept Legate** (5.4.2): keep the Legate with the highest Battle Rating if it is 2 or more (ties: the higher Command Rating).
* **Caesar displaced:** remove Roman IMs outside Provincia first; among those, IMs outside Roman-controlled provinces first. Caesar then goes to the space with the most Legions.

---

## 6. Concilium (the Gallic bot)

### 6.1 Missions

**RISE.**
* From Turn 4, with 2+ AP left and at least two Submitted Tribes that have a legal space, declare a **Major Uprising** (2 AP, 7.7.3). Place every returning Tribe (6.3). Then each Council IM removes a Roman IM in Gaul, Roman-controlled provinces first. Then any Council Tribes come out.
* Otherwise, if a Council Tribe may come out and has a space, or there are 3+ Council IMs (any number if this is the bot's last card), **take everything out** of the Council Box (1 AP). Place the Tribes (6.3) and the IMs by the Agitate Table.

**BANK.** On Turns 1–5, put an IM in the Council Box if it has fewer than 6.

**AMBUSH.** An army attacks Roman CUs (outside) it can reach with at least 1.5× their BS. Against Caesar's army it needs 2.1×. *Target order:* Caesar's army; the largest Roman BS; the nearest.

**RAID.** An army SWEEPs (5.3) Roman IMs with these weights:
* 4: Narbonensis;
* 3: a Roman-controlled province;
* 2: elsewhere in Provincia;
* 1: anything else.

It never targets a space in or next to Caesar's space, and never sweeps into danger (3).

**AGITATE.** One Agitate Table action.

### 6.2 Agitate Table (Concilium)

Take the first line that gives a legal action:

1. **Convert** a Roman IM in a space with Gallic CUs. Prefer Roman-controlled provinces.
2. **Provincia.** Place an IM in Provincia (8.3.1 adjacency). Narbonensis comes first.
3. **Gain.** Place an IM that gives Gaul control of a province: one marker short. Celtica comes first.
4. **Deny.** Place an IM in a province with no Fortified Town where one more Roman IM would give Rome control.
5. **Cut.** Place an IM in a vacant space next to 2+ Roman IMs. Take the space with the most adjacent Roman markers.
6. Place an IM in the province of Gaul, not yet Gallic-controlled, that Gaul is nearest to controlling; then in a Gallic-controlled province of Gaul; then anywhere.

Ties go to the compass.

### 6.3 Tribes and leaders

* **Reinforcements** (5.1): keep the three strongest drawn Tribes that have a legal space. Return the weakest.
* **Placement:** place each Tribe in the legal space farthest from any Legion (count up to 4 spaces). If that ties, take the space next to the fewest Roman markers, then the most northern.
* **Council Box:** a Tribe goes there only when it has no legal space.
* **Displaced IM:** if a Tribe is placed on a Gallic IM, move that IM to a vacant Town in the same province, the one farthest in the compass direction.
* **Ambiorix and Vercingetorix:** on arrival and in winter, each goes to the Gallic-controlled space in his Region with the most Gallic CS, a Fortified Town first.
* **Spring Muster:** Concilium does not move.

### 6.4 Event Guide (Concilium)

| # | Card | Live when | ★ |
|---|---|---|---|
| 5 | The Belgic Confederation | 2+ Tribes or leaders in Belgica | ★ |
| 6 | A United Gaul | 3+ provinces of Gaul with a Gallic IM | ★ |
| 7 | Belgic Resentment | 2+ Belgic provinces with a Roman IM or Roman CU | |
| 8 | Druidic Influence | a province of Gaul with no Roman CU has 2+ Roman IMs | |
| 13 | Gallic War Council | always | |
| 14 | Glory & Liberty | Fortified Towns in 3+ provinces | ★ |
| 15 | Exchange of Oaths (Bonus) | the Minor Tribe is available | |
| 16, 53 | Trumpets of War | 3+ Tribes or leaders on the map | ★ |
| 21 | Ties of Blood and Marriage | the Pool is not empty | ★ |
| 22, 23, 28 | Burn the Countryside; Gaul of the Long-Hairs; Alesia (Bonus) | always | |
| 25, 26 | Mercenaries (Bonus) | a Mercenary is available | |
| 27 | Unrest in Provincia | a Roman IM is in Provincia | ★ |
| 33, 46 | Local Raids (Bonus) | a target exists | |
| 34, 35 | German Migration (Bonus) | always | |
| 36 | Encourage the Timid | Gallic CUs in 3+ provinces | |
| 37, 38 | Motus Ubique | Gallic units in 3+ Regions | |
| 39, 40 | Incite; Unrest Spreads (Bonus) | a target exists | |
| 41 | A Call to Arms | the Militia is available and Gaul controls 2+ Celtic provinces | |
| 42 | Senate Outraged | Rome holds 2+ cards | |
| 43 | The Aedui Switch Sides (Bonus) | the Aedui are in their box and an Aedui space is free of Roman IMs and CUs | ★ |
| 44 | Legate Called to Rome (Bonus) | a Legate with Battle Rating 2+ is on the map | |
| 45 | Diplomacy | a target exists | |
| 50 | Naval Supremacy | Gaul is besieging a port Walled City and has Naval Supremacy in one of its sea zones | |
| 51 | Stratagem (Bonus) | Gaul is besieging a Walled City | |
| 49 | Three Days March | never | |

**Cancel list (#24):** Roman #1, 2, 3, 4, 10, 11, 12.

### 6.5 Event choices (Concilium)

* **Influence actions** in Events: use the Agitate Table, limited to the spaces the Event allows.
* **Remove or convert a Roman IM:** take the highest RAID weight (6.1).
* **Activation Events** (#5, #16, #37, #38, #53): repeat this: if any activated army that has not yet acted can AMBUSH, it does; otherwise one RAIDs. Stop when none can act. #5 activates only armies in Belgica. #37 and #38 activate at most one army per Region.
* **#8:** choose the province with the most Roman IMs; Roman-controlled provinces come first.
* **#13:** restore the strongest reduced Tribe.
* **#15, #25, #26, #41:** place the unit in the eligible space nearest a Legion.
* **#22:** devastate a Roman IM space, choosing the one next to the most Legions. If there is no Roman IM space, place nothing.
* **#28:** upgrade the Fortified Town nearest a Legion.
* **#34, #35:** move the Germans as in 5.5, aiming at Roman IMs.
* **#42:** after taking your card, Concilium plays again at once: a new Directive and a new Offer from its whole hand (2.1–2.4).
* **#23:** remove a Roman IM next to a Gallic Stronghold if there is one; otherwise take one Agitate action next to a Stronghold.
* **#43:** use the eligible Aedui space nearest the compass.
* **#50, #51:** use the location with the most Siege Points.
* **#44:** swap the Legate with the highest Battle Rating.

---

## 7. Levels

| Level | Imperator (you play Gaul) | Concilium (you play Rome) |
|---|---|---|
| 1 | Rules only | You win with 9+ VP |
| 2 | +1 AP on each of its first 4 card plays each turn | You win with 10+ VP |
| 3 (start here) | +1 AP on every card play | You win with 11+ VP |
| 4 | +1 AP on every card play; Rome wins with 10+ VP | Rules only (12 VP) |
| 5 | +1 AP on every card play; Rome wins with 9+ VP | Concilium +1 AP on each of its first 4 card plays each turn |

Start at level 3 against either bot, then move up or down one level after each game you win or lose. The bonus AP is added to cards played for AP and to Bonus cards. Card #4 still gives exactly 5. The Gallic automatic victory (19.1.1) and the Roman automatic victory (19.1.2) are unchanged.

---

## 8. Notes

* **Editions.** The deck in the public Vassal module is the 1st edition. The 2nd-edition cards have "minor text changes", and most are now worth 2 AP. The bots read the AP value printed on your card. If a 2nd-edition card's text differs from the summary in the Event Guide, follow the card, and use the Event Guide's Live condition as the bot's test.
* **Results.** The Simulation Report gives win rates against computer opponents. These are model results, not tabletop results. Please record your games on the Record Sheet.

---

## Appendix: the Directive decks

Each bot has nine Directive cards (printed separately). The missions on a card are tried in the order shown (2.5).

**Imperator**

| Card | Name | Mission order | Compass |
|---|---|---|---|
| I-1 | Pacify | RULE, SIEGE, RAID, SETTLE, STRIKE | N |
| I-2 | Pacify | RULE, SIEGE, RAID, SETTLE, STRIKE | S |
| I-3 | Pacify | RULE, SIEGE, RAID, SETTLE, STRIKE | E |
| I-4 | Pacify | RULE, SIEGE, RAID, SETTLE, STRIKE | W |
| I-5 | Rule | RULE, RAID, SIEGE, SETTLE, STRIKE | N |
| I-6 | Rule | RULE, RAID, SIEGE, SETTLE, STRIKE | W |
| I-7 | Raid | RAID, RULE, SIEGE, SETTLE, STRIKE | E |
| I-8 | Campaign | RULE, SIEGE, STRIKE, RAID, SETTLE | S |
| I-9 | Glory | RULE, INVADE, SIEGE, RAID, SETTLE | N |

Before the card's missions Imperator always tries CONTINUE, PROTECT and SUBMIT; after them, GATHER and CONTROL.

**Concilium**

| Card | Name | Mission order | Compass |
|---|---|---|---|
| C-1 | Revolt | RISE, AMBUSH, RAID, AGITATE | N |
| C-2 | Revolt | RISE, RAID, AMBUSH, AGITATE | S |
| C-3 | Agitate | AGITATE, RAID, AMBUSH, BANK | E |
| C-4 | Agitate | AGITATE, AMBUSH, RAID, BANK | W |
| C-5 | Raid | RAID, AGITATE, AMBUSH, BANK | S |
| C-6 | Raid | RAID, AMBUSH, AGITATE, BANK | N |
| C-7 | Ambush | AMBUSH, RAID, AGITATE, BANK | E |
| C-8 | Council | BANK, AGITATE, RAID, AMBUSH | W |
| C-9 | Council | RISE, BANK, AGITATE, RAID | N |

After the card's missions Concilium always tries AGITATE.
