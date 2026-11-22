# Sample game: Imperator (level 3) vs Concilium (level 3)

Both sides are bots, so every decision below follows the printed rules. Seed 45 (engine and bots v1.0). Imperator gets +1 AP on every card play (level 3); Concilium plays the plain rules. Lines starting with a Directive show the card turned over, the two cards of the Offer (* = Event Live for the bot) and the card chosen. "AP:" lines show the mission that spent each Action Point. Moves list the leader, the number of CUs, start and end space and the operations performed. Turns 1 and 2 are shown in full; later turns list only the cards played, combat, sieges, Tribes and VP.

## How this game went

* **Turn 1.** Caesar marches all six Legions to Octodurus, and his third siege roll opens Caesar's Pass (+1 VP). Meanwhile Concilium raids Belgica. A Gallic band from Segni removes the Roman IMs at Bibrax, Suessiones, Meldi, Silvanectes and Lutetia, one card after another, always away from Caesar. Rome leads Celtica 7–1 but holds no Belgic province (0–1): Governance 8, +1 VP.
* **Turn 2.** Concilium cancels *Roman Rule* with #24 and brings the Germans in with *German Migration*. Caesar comes back north with four Legions. Meldi surrenders to him, and he RAIDs Silvanectes, Suessiones and Condrusi. Isolation then removes five Gallic IMs that had lost their link to Gallic forces. Celtica stands at 9–0, but Belgica is only 1–1: Governance 8, +1 VP.
* **Turn 3.** Caesar's army takes the surrender of Agedincum, Samarobriva and the Nervii's Fortified Town on three consecutive cards. Belgica is now 2–2: Governance 8, +1 VP.
* **Turn 4.** Belgica finally tips 2–1 to Rome: Governance 10, +2 VP, for 6 VP.
* **Turn 5.** Concilium moves first and AMBUSHes a two-Legion army left at Virodunum. After a drawn first battle, a second attack destroys Legions VII and VIII. Rome still dominates both regions (Governance 10, +2 VP), but the lost Legions cost 2 VP: Rome has 6 VP with one turn left.
* **Turn 6.** Concilium plays *The Belgic Confederation*, *Trumpets of War* and *Belgic Resentment*, but cannot break Rome's hold. Rome gets one Legion back as a replacement. *Local Raids* removes the last Gallic IM in Germania for +2 VP, and Governance 10 adds +2 more. The final score is 11 VP: 12, −1 for the Legion still eliminated. **Rome needed 12, so Gaul wins by a single point.**

What this game shows about the bots:

* **Imperator** gains provinces with RULE and RAID, and uses Caesar's army to take Fortified Towns that must surrender. Turn 5 shows the risk its REGROUP mission guards against: a Legate's army left in danger at the end of a turn can be caught before Rome plays again.
* **Concilium** Raids wherever the Legions are not and never sweeps into danger. It contests the region where Rome is weakest, here Belgica, and saves its ambush for a weak Roman army.
* **Governance decides the race, turn by turn.** Rome needs dominance in both Celtica and Belgica almost every turn. Every turn spent short of that costs a VP.

## How to read the log

* A **Directive** line shows the Directive card turned over and its missions, then the Offer of two cards (* marks a card whose Event is Live for the bot) and the card chosen.
* A **plays** line gives the card and how it was used: as an Event, as a Bonus card (Event, then AP), or for AP.
* An **AP:** line names the mission that spent one Action Point (rules 2.5).
* A **move** line gives the leader, the number of units that moved with him, the start and end spaces, and the operations done on the way.
* A **battle** line reads *attacker BS vs defender BS: hits scored by the attacker / hits scored by the defender → winner* (A or D).
* Turns 1 and 2 are logged in full. From Turn 3 on, the log shows only the cards played, combat, sieges, Tribe arrivals and VP.

## The log



## Turn 1

- tribe Bellovaci placed at Samarobriva
- tribe Veneti placed at Curiosolites
- tribe Remi placed at Segni
- Concilium Directive Council (W): BANK > AGITATE > RAID > AMBUSH; Offer #20, #18 -> #20
- **Concilium** plays #20 Roman Auxiliaries as **ap**
    - Concilium AP: BANK
    - Concilium AP: BANK
- Imperator Directive Pacify (N): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #2*, #8 -> #2
- **Imperator** plays #2 Constant as the Northern Star as **bonus**
    - siege Octodurus col2 roll5: loss 1 pts 1 -> 1
    - R move Caesar+6 Bibracte->Octodurus ops=['siege']
    - R influence place Suessiones
    - Imperator AP: SETTLE
    - R influence place Silvanectes
    - Imperator AP: RULE
    - R influence place Lutetia
    - Imperator AP: SETTLE
    - R influence place Metiosedum
    - Imperator AP: RULE
- Concilium Directive Revolt (N): RISE > AMBUSH > RAID > AGITATE; Offer #9, #3 -> #9
- **Concilium** plays #9 Destroyed Root & Branch as **ap**
    - IM removed: Bibrax (R)
    - G move stack+1 Segni->Bibrax ops=['remove_im']
    - Concilium AP: RAID
    - G influence place Redones
    - Concilium AP: AGITATE
- Imperator Directive Glory (N): RULE > INVADE > SIEGE > RAID > SETTLE; Offer #1*, #8 -> #1
- **Imperator** plays #1 Veni Vidi Vici as **bonus**
    - siege Octodurus col2 roll2: loss 1 pts 0 -> 1
    - R move Caesar+6 Octodurus->Octodurus ops=['siege']
    - R influence place Autricum
    - Imperator AP: SETTLE
    - R influence place Cenabum
    - Imperator AP: RULE
    - R influence place Sotiates
    - Imperator AP: SETTLE
    - R influence place Tarbelli
    - Imperator AP: RULE
- Concilium Directive Raid (N): RAID > AMBUSH > AGITATE > BANK; Offer #18, #53* -> #53
- **Concilium** plays #53 Trumpets of War as **event**
    - IM removed: Suessiones (R)
    - G move stack+1 Bibrax->Suessiones ops=['remove_im']
- Imperator Directive Raid (E): RAID > RULE > SIEGE > SETTLE > STRIKE; Offer #22, #31 -> #22
- **Imperator** plays #22 Burn the Countryside as **ap**
    - siege Octodurus col2 roll10: loss 0 pts 2 -> 3
    - stronghold Octodurus subjugated
    - VP +1 Caesar's Pass -> 1
    - R move Caesar+6 Octodurus->Octodurus ops=['siege']
    - Imperator AP: CONTINUE
    - R influence place Meldi
    - Imperator AP: RULE
    - R influence place Vellavi
    - Imperator AP: SETTLE
- Concilium Directive Agitate (W): AGITATE > AMBUSH > RAID > BANK; Offer #40*, #10 -> #40
- **Concilium** plays #40 Unrest Spreads as **bonus**
    - IM removed: Tarbelli (R)
    - G influence place Tarbelli
    - Concilium AP: AGITATE
    - G influence place Ausci
    - Concilium AP: AGITATE
- Imperator Directive Pacify (E): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #19*, #31 -> #19
- **Imperator** plays #19 Roman Trade as **bonus**
    - IM removed: Ausci (G)
    - R influence place Ausci
    - Imperator AP: RULE
    - R influence place Gergovia
    - Imperator AP: SETTLE
    - R influence place Gorgobina
    - Imperator AP: RULE
- Concilium Directive Council (N): RISE > BANK > AGITATE > RAID; Offer #18, #10 -> #18
- **Concilium** plays #18 Hostages as **ap**
    - Concilium AP: BANK
    - G influence place Vellaunodurum
    - G influence place Alesia
    - G influence place Agedincum
    - Concilium AP: RISE
- Imperator Directive Campaign (S): RULE > SIEGE > STRIKE > RAID > SETTLE; Offer #50, #8 -> #50
- **Imperator** plays #50 Naval Supremacy as **ap**
    - R influence place Autessiodurum
    - Imperator AP: SETTLE
    - R influence place Andematunnum
    - Imperator AP: SETTLE
    - R influence place Tricasses
    - Imperator AP: SETTLE
- Concilium Directive Revolt (S): RISE > RAID > AMBUSH > AGITATE; Offer #3, #42* -> #3
- **Concilium** plays #3 Aid From Pompey as **ap**
    - IM removed: Meldi (R)
    - G move stack+1 Suessiones->Meldi ops=['remove_im']
    - Concilium AP: RAID
    - G influence place Meldi
    - Concilium AP: AGITATE
- Imperator Directive Pacify (S): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #5, #31 -> #5
- **Imperator** plays #5 The Belgic Confederation as **ap**
    - R influence place Suessiones
    - Imperator AP: RULE
    - R influence place Avaricum
    - Imperator AP: SETTLE
    - R influence place Cubi
    - Imperator AP: SETTLE
    - R influence place Bituriges
    - Imperator AP: RULE
- Concilium Directive Raid (S): RAID > AGITATE > AMBUSH > BANK; Offer #10, #42* -> #10
- **Concilium** plays #10 The Reach of Rome as **ap**
    - IM removed: Silvanectes (R)
    - G move stack+1 Meldi->Silvanectes ops=['remove_im']
    - Concilium AP: RAID
    - G influence place Silvanectes
    - Concilium AP: AGITATE
- Imperator Directive Rule (N): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #31, #8 -> #31
- **Imperator** plays #31 A Friend of Rome as **ap**
    - R influence place Lexovii
    - Imperator AP: SETTLE
    - R influence place Esubii
    - Imperator AP: SETTLE
    - R influence place Venelli
    - Imperator AP: RULE
- Concilium Directive Ambush (E): AMBUSH > RAID > AGITATE > BANK; Offer #42 -> #42
- **Concilium** plays #42 Senate Outraged as **ap**
    - IM removed: Lutetia (R)
    - G move stack+1 Silvanectes->Lutetia ops=['remove_im']
    - Concilium AP: RAID
- Imperator Directive Pacify (W): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #8 -> #8
- **Imperator** plays #8 Druidic Influence as **ap**
    - R influence place Eburovices
    - Imperator AP: SETTLE
    - R influence place Diablintes
    - Imperator AP: SETTLE
    - R influence place Andes
    - Imperator AP: RULE
    - isolated G IM removed Alesia
    - VP +1 governance 8 -> 2
    - governance 8

*End of Turn 1: Celtica provinces Rome 7 / Gaul 1; Belgica Rome 0 / Gaul 1; Fortified Towns 3; Provincia provinces lost: none; Roman VP 2.*

## Turn 2

- tribe Senones placed at Agedincum
- tribe Nervii placed at Nervii
- tribe Suessiones placed at Meldi
- Concilium Directive Agitate (E): AGITATE > RAID > AMBUSH > BANK; Offer #34*, #11 -> #11
- **Concilium** plays #11 For the Glory of Caesar as **ap**
    - G influence place Condrusi
    - Concilium AP: AGITATE
    - G influence place Lutetia
    - Concilium AP: AGITATE
    - G influence place Turoni
    - Concilium AP: AGITATE
- Imperator Directive Rule (W): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #12*, #43 -> #12
- **Imperator** plays #12 Roman Rule as **event**
    - G cancels #12 with #24
- Imperator Directive Glory (N): RULE > INVADE > SIEGE > RAID > SETTLE; Offer #44, #51 -> #44
- **Imperator** plays #44 Legate Called to Rome as **ap**
    - R influence place Tullum
    - Imperator AP: SETTLE
    - R influence place Mediomatrici
    - Imperator AP: SETTLE
    - R influence place Triboci
    - Imperator AP: RULE
- Concilium Directive Agitate (W): AGITATE > AMBUSH > RAID > BANK; Offer #34*, #33* -> #34
- **Concilium** plays #34 German Migration as **bonus**
    - IM removed: Tullum (R)
    - German tribe to Tullum
    - G influence place Leuci
    - Concilium AP: AGITATE
    - G influence place Abrincatui
    - Concilium AP: AGITATE
- Imperator Directive Campaign (S): RULE > SIEGE > STRIKE > RAID > SETTLE; Offer #4*, #43 -> #4
- **Imperator** plays #4 Aid From Crassus as **event**
    - R influence place Cadurci
    - Imperator AP: SETTLE
    - R influence place Sotium
    - Imperator AP: SETTLE
    - R influence place Uxellodunum
    - Imperator AP: SETTLE
    - R influence place Carantomagus
    - Imperator AP: RULE
    - R influence place Santoni
    - Imperator AP: SETTLE
- Concilium Directive Revolt (S): RISE > RAID > AMBUSH > AGITATE; Offer #33*, #32 -> #33
- **Concilium** plays #33 Local Raids as **bonus**
    - IM removed: Autessiodurum (R)
    - IM removed: Suessiones (R)
    - G move stack+1 Meldi->Suessiones ops=['remove_im']
    - Concilium AP: RAID
    - G influence place Autessiodurum
    - Concilium AP: AGITATE
- Imperator Directive Rule (N): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #14, #45* -> #14
- **Imperator** plays #14 Glory & Liberty as **ap**
    - IM removed: Vellaunodurum (G)
    - R move Caesar+4 Allobroges->Vellaunodurum ops=['remove_im']
    - Imperator AP: RAID
    - R influence place Vellaunodurum
    - Imperator AP: SETTLE
    - R influence place Pictavi
    - Imperator AP: SETTLE
- Concilium Directive Council (W): BANK > AGITATE > RAID > AMBUSH; Offer #25*, #39* -> #25
- **Concilium** plays #25 Mercenaries From Britannia and Hispania as **bonus**
    - Concilium AP: BANK
    - Concilium AP: BANK
- Imperator Directive Pacify (E): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #45*, #43 -> #43
- **Imperator** plays #43 The Aedui Switch Sides as **ap**
    - Meldi surrenders to R
    - R move Caesar+4 Vellaunodurum->Meldi ops=['siege']
    - Imperator AP: SIEGE
    - R influence place Meldi
    - Imperator AP: SETTLE
    - R influence place Suessiones
    - Imperator AP: RULE
- Concilium Directive Agitate (E): AGITATE > RAID > AMBUSH > BANK; Offer #39*, #46* -> #39
- **Concilium** plays #39 Incite Through Sedition as **bonus**
    - IM removed: Suessiones (R)
    - G influence place Suessiones
    - Concilium AP: AGITATE
    - G influence place Limonum
    - Concilium AP: AGITATE
- Imperator Directive Pacify (W): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #28, #45* -> #28
- **Imperator** plays #28 Alesia as **ap**
    - IM removed: Silvanectes (G)
    - R move Caesar+4 Meldi->Silvanectes ops=['remove_im']
    - Imperator AP: RAID
    - R influence place Silvanectes
    - Imperator AP: RULE
    - R influence place Anagnutes
    - Imperator AP: SETTLE
- Concilium Directive Raid (N): RAID > AMBUSH > AGITATE > BANK; Offer #46*, #32 -> #46
- **Concilium** plays #46 Local Raids as **bonus**
    - IM removed: Meldi (R)
    - G influence place Meldi
    - Concilium AP: AGITATE
    - G influence place Brigiosum
    - Concilium AP: AGITATE
- Imperator Directive Pacify (N): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #27, #51 -> #27
- **Imperator** plays #27 Unrest in Provincia as **ap**
    - R influence place Lemovices
    - Imperator AP: RULE
    - IM removed: Suessiones (G)
    - R move Caesar+4 Silvanectes->Suessiones ops=['remove_im']
    - Imperator AP: RAID
    - R influence place Suessiones
    - Imperator AP: RULE
- Concilium Directive Revolt (N): RISE > AMBUSH > RAID > AGITATE; Offer #32 -> #32
- **Concilium** plays #32 Caesar's Legions as **ap**
    - G influence place Cenomani
    - Concilium AP: AGITATE
    - G influence place Petrocorii
    - Concilium AP: AGITATE
- Imperator Directive Rule (W): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #51, #45* -> #51
- **Imperator** plays #51 Stratagem & Treachery as **ap**
    - IM removed: Condrusi (G)
    - R move Caesar+4 Suessiones->Condrusi ops=['remove_im']
    - Imperator AP: RAID
    - IM removed: Limonum (G)
    - R move Antonius+2 Cambiovicenses->Limonum ops=['remove_im']
    - Imperator AP: RAID
    - R influence place Viromandui
    - Imperator AP: SETTLE
- Concilium Directive Council (N): RISE > BANK > AGITATE > RAID; Offer #26* -> #26
- **Concilium** plays #26 Mercenaries From Britannia and Hispania as **bonus**
    - G influence place Bagacum
    - G influence place Bratuspantium
    - Concilium AP: RISE
    - Concilium AP: BANK
- Imperator Directive Raid (E): RAID > RULE > SIEGE > SETTLE > STRIKE; Offer #45* -> #45
- **Imperator** plays #45 Diplomacy as **event**
    - attrition Condrusi R
    - isolated G IM removed Leuci
    - isolated G IM removed Cenomani
    - isolated G IM removed Turoni
    - isolated G IM removed Brigiosum
    - isolated G IM removed Petrocorii
    - VP +1 governance 8 -> 3
    - governance 8

*End of Turn 2: Celtica provinces Rome 9 / Gaul 0; Belgica Rome 1 / Gaul 1; Fortified Towns 5; Provincia provinces lost: none; Roman VP 3.*

## Turn 3

- tribe Cadurci placed at Petrocorii
- tribe Leuci placed at Leuci
- tribe Pictones placed at Brigiosum
- **Concilium** plays #23 Gaul of the Long-Hairs as **bonus**
    - R avoids battle Nemetocenna->Viromandui
    - R avoids battle Viromandui->Bibrax
- **Imperator** plays #17 Caesar's Lieutenant as **bonus**
- **Concilium** plays #36 Encourage the Timid as **event**
- **Imperator** plays #48 Roman Bribes as **event**
- **Concilium** plays #49 Three Days March as **ap**
- **Imperator** plays #35 German Migration as **bonus**
    - German tribe to Alesia
- **Concilium** plays #37 Motus Ubique as **ap**
- **Imperator** plays #13 Gallic War Council as **ap**
- **Concilium** plays #29 German Auxiliary Cavalry as **ap**
- **Imperator** plays #30 German Auxiliary Cavalry as **bonus**
    - Agedincum surrenders to R
    - R move Caesar+3 Matisco->Agedincum ops=['siege']
- **Concilium** plays #15 Exchange of Oaths as **bonus**
- **Imperator** plays #38 Motus Ubique as **ap**
    - Samarobriva surrenders to R
    - R move Caesar+3 Agedincum->Samarobriva ops=['siege']
- **Concilium** plays #41 A Call to Arms as **ap**
- **Imperator** plays #6 A United Gaul as **ap**
    - Nervii surrenders to R
    - R move Caesar+3 Samarobriva->Nervii ops=['siege']
- **Concilium** plays #47 Winter Campaign as **ap**
    - R avoids battle Nervii->Aduatuci
- **Imperator** plays #21 Ties of Blood and Marriage as **ap**
    - G intercepts into Bagacum from Nervii
    - VP +1 governance 8 -> 4
    - governance 8

*End of Turn 3: Celtica provinces Rome 9 / Gaul 1; Belgica Rome 2 / Gaul 2; Fortified Towns 5; Provincia provinces lost: none; Roman VP 4.*

## Turn 4

- tribe Atrebates placed at Portus Itius
- tribe Treveri placed at Treveri
- tribe Bituriges placed at Turoni
- Caesar delayed
- **Concilium** plays #38 Motus Ubique as **ap**
    - tribe Bellovaci placed at Iuliobona
    - tribe Nervii placed at Nervii
- **Imperator** plays #26 Mercenaries From Britannia and Hispania as **ap**
- **Concilium** plays #3 Aid From Pompey as **ap**
- **Imperator** plays #1 Veni Vidi Vici as **bonus**
- **Concilium** plays #4 Aid From Crassus as **ap**
- **Imperator** plays #27 Unrest in Provincia as **ap**
- **Concilium** plays #41 A Call to Arms as **ap**
- **Imperator** plays #35 German Migration as **bonus**
    - German tribe to Durocortorum
- **Concilium** plays #42 Senate Outraged as **event**
- **Concilium** plays #15 Exchange of Oaths as **bonus**
- **Imperator** plays #53 Trumpets of War as **ap**
- **Concilium** plays #46 Local Raids as **bonus**
- **Imperator** plays #34 German Migration as **bonus**
    - German tribe to Bibrax
- **Concilium** plays #30 German Auxiliary Cavalry as **ap**
- **Imperator** plays #44 Legate Called to Rome as **ap**
- **Concilium** plays #47 Winter Campaign as **ap**
- **Imperator** plays #42 Senate Outraged as **ap**
    - VP +2 governance 10 -> 6
    - governance 10

*End of Turn 4: Celtica provinces Rome 8 / Gaul 1; Belgica Rome 2 / Gaul 1; Fortified Towns 10; Provincia provinces lost: none; Roman VP 6.*

## Turn 5

- tribe Aquitani placed at Tarbelli
- tribe Arverni submits on arrival
- **Concilium** plays #17 Caesar's Lieutenant as **ap**
    - battle Virodunum G7 vs R4: hits 2/2 -> draw
    - eliminated Remi loss
    - battle Virodunum G5 vs R2: hits 2/1 -> A
    - eliminated VII loss
    - eliminated VIII loss
    - eliminated Treveri loss
- **Imperator** plays #40 Unrest Spreads as **bonus**
- **Concilium** plays #39 Incite Through Sedition as **bonus**
- **Imperator** plays #19 Roman Trade as **bonus**
- **Concilium** plays #11 For the Glory of Caesar as **ap**
- **Imperator** plays #43 The Aedui Switch Sides as **ap**
- **Concilium** plays #23 Gaul of the Long-Hairs as **bonus**
- **Imperator** plays #36 Encourage the Timid as **ap**
- **Concilium** plays #13 Gallic War Council as **event**
- **Imperator** plays #37 Motus Ubique as **ap**
- **Concilium** plays #48 Roman Bribes as **ap**
- **Imperator** plays #6 A United Gaul as **ap**
- **Concilium** plays #32 Caesar's Legions as **ap**
- **Imperator** plays #45 Diplomacy as **event**
- **Concilium** plays #2 Constant as the Northern Star as **ap**
- **Imperator** plays #24 You May Believe What You Wish as **ap**
    - VP +2 governance 10 -> 8
    - governance 10

*End of Turn 5: Celtica provinces Rome 7 / Gaul 1; Belgica Rome 4 / Gaul 0; Fortified Towns 9; Provincia provinces lost: none; Roman VP 6.*

## Turn 6

- tribe Aulerci placed at Diablintes
- tribe Armorici placed at Venelli
- tribe Santones placed at Iculisma
- **Concilium** plays #5 The Belgic Confederation as **event**
- **Imperator** plays #25 Mercenaries From Britannia and Hispania as **ap**
- **Concilium** plays #51 Stratagem & Treachery as **ap**
- **Imperator** plays #20 Roman Auxiliaries as **bonus**
- **Concilium** plays #16 Trumpets of War as **event**
- **Imperator** plays #22 Burn the Countryside as **ap**
- **Concilium** plays #7 Belgic Resentment as **event**
- **Imperator** plays #29 German Auxiliary Cavalry as **bonus**
- **Concilium** plays #50 Naval Supremacy as **ap**
- **Imperator** plays #33 Local Raids as **bonus**
    - VP +2 Germania -> 10
- **Concilium** plays #12 Roman Rule as **ap**
- **Imperator** plays #8 Druidic Influence as **ap**
- **Concilium** plays #18 Hostages as **ap**
- **Imperator** plays #28 Alesia as **ap**
- **Concilium** plays #9 Destroyed Root & Branch as **ap**
- **Imperator** plays #14 Glory & Liberty as **ap**
    - VP +2 governance 10 -> 12
    - governance 10

*End of Turn 6: Celtica provinces Rome 6 / Gaul 4; Belgica Rome 4 / Gaul 1; Fortified Towns 12; Provincia provinces lost: none; Roman VP 11.*

**Result:** Gaul wins (end VP 11). Battles 2, siege rolls 7, Tribes eliminated 2, Legions still eliminated at the end 1.
