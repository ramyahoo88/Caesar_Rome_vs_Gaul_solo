# Sample game: Imperator (level 3) vs Concilium (level 3)

Both sides are bots, so every decision below follows the printed rules. Seed 38. Imperator gets +1 AP on every card play (level 3); Concilium plays the plain rules. Lines starting with a Directive show the card turned over, the two cards of the Offer (* = Event Live for the bot) and the card chosen. "AP:" lines show the mission that spent each Action Point. Moves list the leader, the number of CUs, start and end space and the operations performed. Turns 1 and 2 are shown in full; later turns list only the cards played, combat, sieges, Tribes and VP.

## How this game went

* **Turn 1.** Concilium opens with *Unrest Spreads* and removes the Roman IM at Bibrax. Caesar marches all six Legions to besiege Octodurus. *Gaul of the Long-Hairs* then removes the Roman IM in the Allobroges. When *For the Glory of Caesar* activates Caesar, PROTECT comes first, so he turns back to clear the Allobroges. He returns to Octodurus, and his third siege roll opens Caesar's Pass for 1 VP. Imperator cancels *Ties of Blood and Marriage* with #24. At Isolation two Gallic IMs are cut off and removed. Rome is ahead in Celtica (4–0) and Belgica (2–1): Governance 10, so +2 VP.
* **Turn 2.** This is Concilium's raiding turn. After *The Belgic Confederation*, Gallic bands remove Roman IMs from Andes, Cenomani, Aduatuci, Tungri, Diablintes, Metiosedum, Nemetes, Eburones and Eburovices, never next to Caesar. Caesar strikes back: he destroys the Carnutes at Metiosedum and takes the surrender of Turoni. Belgica ends 2–2, so Rome has presence there but not dominance: Governance 8, +1 VP.
* **Turn 3.** Imperator's RULE missions rebuild Rome's position: Celtica 9–1 and Belgica 3–2. Governance 10, +2 VP.
* **Turn 4.** Gaul takes Belgica 3–2, and Rome loses its last space in Aquitania: Governance 7, +1 VP.
* **Turn 5.** The Arverni and Senones arrive and Submit at once. Caesar's twelve-strength army then marches through western Celtica and forces five Gallic stacks to Submit at 3:1, Vercingetorix's army at Metiosedum among them. Elsewhere a Legate's army loses Legion XIII at Tarbelli. Celtica 11–0 and Belgica 4–3: Governance 10, +2 VP, for 9 VP with one turn left.
* **Turn 6.** Concilium needs Belgica. Its RISE mission declares a Major Uprising that brings Submitted Tribes back, and a second one late in the turn returns the Sequani and Arverni. Caesar destroys Ambiorix's army at Caleti, but Belgica ends 3–3, so Rome has no dominance there: Governance 8, +1 VP. The final score is 10 VP: −1 for Legion XIII and +1 for seven eliminated Tribes. **Rome needed 12, so Gaul wins.**

What this game shows about the bots:

* **Imperator** gains provinces with RULE and RAID. It uses Caesar's big army to force Submissions, and it sends Legates' armies only where the Gauls cannot catch them at 1.5:1.
* **Concilium** Raids wherever the Legions are not and contests the region Rome is weakest in, here Belgica. It saves its Submitted Tribes for a Major Uprising in the last turn.
* **The race is decided turn by turn in Governance.** Rome needs dominance in both Celtica and Belgica almost every turn. One region held to a tie costs a VP.

## How to read the log

* A **Directive** line shows the Directive card turned over and its missions, the Offer of two cards (* marks a card whose Event is Live for the bot) and the card chosen.
* A **plays** line gives the card and how it was used: as an Event, as a Bonus card (Event, then AP) or for AP.
* An **AP:** line names the mission that spent one Action Point (rules 2.5).
* A **move** line gives the leader, how many units moved with him, the start and end spaces, and the operations done on the way.
* A **battle** line reads *attacker BS vs defender BS: hits scored by the attacker / hits scored by the defender → winner* (A or D).
* Turns 1 and 2 are logged in full. Later turns show only the cards played, combat, sieges, Tribe arrivals and VP.

## The log



## Turn 1

- tribe Bituriges placed at Turoni
- tribe Nervii placed at Nervii
- tribe Atrebates placed at Portus Itius
- Concilium Directive Council (N): RISE > BANK > AGITATE > RAID; Offer #40*, #48 -> #40
- **Concilium** plays #40 Unrest Spreads as **bonus**
    - IM removed: Bibrax (R)
    - Concilium AP: BANK
    - Concilium AP: BANK
- Imperator Directive Pacify (W): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #39, #3 -> #39
- **Imperator** plays #39 Incite Through Sedition as **ap**
    - R influence place Leuci
    - Imperator AP: RULE
    - siege Octodurus col2 roll6: loss 0 pts 1 -> 1
    - R move Caesar+6 Bibracte->Octodurus ops=['siege']
    - Imperator AP: SIEGE
    - R influence place Tullum
    - Imperator AP: SETTLE
- Concilium Directive Raid (N): RAID > AMBUSH > AGITATE > BANK; Offer #18, #23* -> #23
- **Concilium** plays #23 Gaul of the Long-Hairs as **bonus**
    - IM removed: Allobroges (R)
    - G influence place Allobroges
    - Concilium AP: AGITATE
    - G influence place Condrusi
    - Concilium AP: AGITATE
- Imperator Directive Pacify (N): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #45*, #11* -> #11
- **Imperator** plays #11 For the Glory of Caesar as **event**
    - IM removed: Allobroges (G)
    - R move Caesar+6 Octodurus->Allobroges ops=['remove_im']
- Concilium Directive Revolt (N): RISE > AMBUSH > RAID > AGITATE; Offer #48, #20 -> #48
- **Concilium** plays #48 Roman Bribes as **ap**
    - G influence place Mediomatrici
    - Concilium AP: AGITATE
    - G influence place Triboci
    - Concilium AP: AGITATE
- Imperator Directive Glory (N): RULE > INVADE > SIEGE > RAID > SETTLE; Offer #3, #30* -> #30
- **Imperator** plays #30 German Auxiliary Cavalry as **bonus**
    - R influence place Allobroges
    - Imperator AP: PROTECT
    - siege Octodurus col2 roll6: loss 0 pts 1 -> 1
    - R move Caesar+6 Allobroges->Octodurus ops=['siege']
    - Imperator AP: SIEGE
    - R influence place Sotiates
    - Imperator AP: SETTLE
- Concilium Directive Agitate (W): AGITATE > AMBUSH > RAID > BANK; Offer #18, #21* -> #21
- **Concilium** plays #21 Ties of Blood and Marriage as **event**
    - R cancels #21 with #24
- Concilium Directive Ambush (E): AMBUSH > RAID > AGITATE > BANK; Offer #18, #22* -> #22
- **Concilium** plays #22 Burn the Countryside as **bonus**
    - G influence place Ausci
    - Concilium AP: AGITATE
    - G influence place Tarbelli
    - Concilium AP: AGITATE
- Imperator Directive Pacify (E): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #43, #26 -> #43
- **Imperator** plays #43 The Aedui Switch Sides as **ap**
    - siege Octodurus col2 roll8: loss 1 pts 2 -> 3
    - stronghold Octodurus subjugated
    - VP +1 Caesar's Pass -> 1
    - R move Caesar+6 Octodurus->Octodurus ops=['siege']
    - Imperator AP: CONTINUE
    - R influence place Vellavi
    - Imperator AP: SETTLE
    - R influence place Gergovia
    - Imperator AP: SETTLE
- Concilium Directive Revolt (S): RISE > RAID > AMBUSH > AGITATE; Offer #20, #31 -> #20
- **Concilium** plays #20 Roman Auxiliaries as **ap**
    - G influence place Cambiovicenses
    - Concilium AP: AGITATE
    - G influence place Gorgobina
    - Concilium AP: AGITATE
- Imperator Directive Campaign (S): RULE > SIEGE > STRIKE > RAID > SETTLE; Offer #45*, #26 -> #26
- **Imperator** plays #26 Mercenaries From Britannia and Hispania as **ap**
    - R influence place Catalauni
    - Imperator AP: SETTLE
    - R influence place Meldi
    - Imperator AP: SETTLE
    - R influence place Silvanectes
    - Imperator AP: RULE
- Concilium Directive Agitate (E): AGITATE > RAID > AMBUSH > BANK; Offer #31, #15* -> #15
- **Concilium** plays #15 Exchange of Oaths as **bonus**
    - G influence place Alesia
    - Concilium AP: AGITATE
    - G influence place Andematunnum
    - Concilium AP: AGITATE
- Imperator Directive Rule (N): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #38, #3 -> #38
- **Imperator** plays #38 Motus Ubique as **ap**
    - R influence place Lutetia
    - Imperator AP: SETTLE
    - R influence place Metiosedum
    - Imperator AP: RULE
    - R influence place Autricum
    - Imperator AP: SETTLE
- Concilium Directive Council (W): BANK > AGITATE > RAID > AMBUSH; Offer #18, #31 -> #18
- **Concilium** plays #18 Hostages as **ap**
    - Concilium AP: BANK
    - Concilium AP: BANK
- Imperator Directive Rule (W): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #3, #45* -> #3
- **Imperator** plays #3 Aid From Pompey as **ap**
    - R influence place Cenabum
    - Imperator AP: RULE
    - R influence place Durocortorum
    - Imperator AP: SETTLE
    - R influence place Bibrax
    - Imperator AP: RULE
- Concilium Directive Raid (S): RAID > AGITATE > AMBUSH > BANK; Offer #31 -> #31
- **Concilium** plays #31 A Friend of Rome as **ap**
    - IM removed: Cenabum (R)
    - G move stack+1 Turoni->Cenabum ops=['remove_im']
    - Concilium AP: RAID
    - G influence place Cenabum
    - Concilium AP: AGITATE
- Imperator Directive Pacify (S): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #45* -> #45
- **Imperator** plays #45 Diplomacy as **event**
    - isolated G IM removed Andematunnum
    - isolated G IM removed Alesia
    - VP +2 governance 10 -> 3
    - governance 10

*End of Turn 1: Celtica provinces Rome 4 / Gaul 0; Belgica Rome 2 / Gaul 1; Fortified Towns 3; Provincia provinces lost: none; Roman VP 3.*

## Turn 2

- tribe Veneti placed at Curiosolites
- tribe Treveri placed at Vangiones
- tribe Carnutes placed at Cenabum
- Concilium Directive Ambush (E): AMBUSH > RAID > AGITATE > BANK; Offer #5*, #12 -> #5
- **Concilium** plays #5 The Belgic Confederation as **event**
- Imperator Directive Raid (E): RAID > RULE > SIEGE > SETTLE > STRIKE; Offer #13, #28 -> #13
- **Imperator** plays #13 Gallic War Council as **ap**
    - IM removed: Gorgobina (G)
    - R move Antonius+2 Vellaunodurum->Gorgobina ops=['remove_im']
    - Imperator AP: RAID
    - R influence place Divodurum
    - Imperator AP: SETTLE
    - R influence place Nemetes
    - Imperator AP: SETTLE
- Concilium Directive Agitate (E): AGITATE > RAID > AMBUSH > BANK; Offer #42*, #44* -> #44
- **Concilium** plays #44 Legate Called to Rome as **bonus**
    - G influence place Namnetes
    - Concilium AP: AGITATE
    - G influence place Treveri
    - Concilium AP: AGITATE
- Imperator Directive Rule (N): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #10*, #6 -> #10
- **Imperator** plays #10 The Reach of Rome as **event**
    - R influence place Aduatuci
    - R influence place Eburones
- Concilium Directive Council (N): RISE > BANK > AGITATE > RAID; Offer #41, #12 -> #41
- **Concilium** plays #41 A Call to Arms as **ap**
    - Concilium AP: BANK
    - G influence place Suessiones
    - G influence place Virodunum
    - G influence place Agedincum
    - Concilium AP: RISE
- Imperator Directive Rule (W): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #28, #32 -> #28
- **Imperator** plays #28 Alesia as **ap**
    - R influence place Eburovices
    - Imperator AP: SETTLE
    - R influence place Diablintes
    - Imperator AP: SETTLE
    - R influence place Andes
    - Imperator AP: RULE
- Concilium Directive Raid (S): RAID > AGITATE > AMBUSH > BANK; Offer #42*, #35* -> #35
- **Concilium** plays #35 German Migration as **bonus**
    - IM removed: Epomanduodurum (R)
    - German tribe to Epomanduodurum
    - IM removed: Andes (R)
    - G move stack+1 Turoni->Andes ops=['remove_im']
    - Concilium AP: RAID
    - IM removed: Aduatuci (R)
    - G move stack+1 Nervii->Aduatuci ops=['remove_im']
    - Concilium AP: RAID
- Imperator Directive Raid (E): RAID > RULE > SIEGE > SETTLE > STRIKE; Offer #34*, #1* -> #1
- **Imperator** plays #1 Veni Vidi Vici as **bonus**
    - R influence place Cenomani
    - Imperator AP: RULE
    - R influence place Tungri
    - Imperator AP: RULE
    - R influence place Andematunnum
    - Imperator AP: SETTLE
    - R influence place Alesia
    - Imperator AP: SETTLE
- Concilium Directive Revolt (S): RISE > RAID > AMBUSH > AGITATE; Offer #12, #17 -> #12
- **Concilium** plays #12 Roman Rule as **ap**
    - IM removed: Cenomani (R)
    - G move stack+1 Andes->Cenomani ops=['remove_im']
    - Concilium AP: RAID
    - IM removed: Tungri (R)
    - G move stack+1 Aduatuci->Tungri ops=['remove_im']
    - Concilium AP: RAID
- Imperator Directive Glory (N): RULE > INVADE > SIEGE > RAID > SETTLE; Offer #34*, #6 -> #34
- **Imperator** plays #34 German Migration as **bonus**
    - IM removed: Mediomatrici (G)
    - German tribe to Mediomatrici
    - R influence place Tricasses
    - Imperator AP: RULE
    - R influence place Andes
    - Imperator AP: RULE
    - R influence place Aduatuci
    - Imperator AP: RULE
- Concilium Directive Council (W): BANK > AGITATE > RAID > AMBUSH; Offer #42*, #53* -> #53
- **Concilium** plays #53 Trumpets of War as **event**
    - IM removed: Diablintes (R)
    - G move stack+1 Cenomani->Diablintes ops=['remove_im']
    - IM removed: Aduatuci (R)
    - G move stack+1 Tungri->Aduatuci ops=['remove_im']
    - IM removed: Metiosedum (R)
    - G move stack+1 Cenabum->Metiosedum ops=['remove_im']
    - IM removed: Nemetes (R)
    - G move stack+1 Vangiones->Nemetes ops=['remove_im']
- Imperator Directive Pacify (W): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #16, #6 -> #16
- **Imperator** plays #16 Trumpets of War as **ap**
    - R influence place Cenomani
    - Imperator AP: RULE
    - R influence place Tungri
    - Imperator AP: RULE
    - IM removed: Agedincum (G)
    - R move P. Crassus+2 Gorgobina->Agedincum ops=['remove_im']
    - Imperator AP: RAID
    - R influence place Abrincatui
    - Imperator AP: SETTLE
- Concilium Directive Raid (N): RAID > AMBUSH > AGITATE > BANK; Offer #42*, #17 -> #17
- **Concilium** plays #17 Caesar's Lieutenant as **ap**
    - IM removed: Eburones (R)
    - G move stack+1 Aduatuci->Eburones ops=['remove_im']
    - Concilium AP: RAID
    - IM removed: Eburovices (R)
    - G move stack+1 Diablintes->Eburovices ops=['remove_im']
    - Concilium AP: RAID
- Imperator Directive Campaign (S): RULE > SIEGE > STRIKE > RAID > SETTLE; Offer #6, #32 -> #6
- **Imperator** plays #6 A United Gaul as **ap**
    - R influence place Diablintes
    - Imperator AP: RULE
    - R influence place Aduatuci
    - Imperator AP: RULE
    - battle Metiosedum R8 vs G4: hits 2/0 -> A
    - eliminated Carnutes loss
    - R move Caesar+4 Allobroges->Metiosedum ops=[]
    - Imperator AP: STRIKE
- Concilium Directive Agitate (W): AGITATE > AMBUSH > RAID > BANK; Offer #42 -> #42
- **Concilium** plays #42 Senate Outraged as **ap**
    - G influence place Cenabum
    - Concilium AP: AGITATE
- Imperator Directive Pacify (S): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #32 -> #32
- **Imperator** plays #32 Caesar's Legions as **ap**
    - R influence place Metiosedum
    - Imperator AP: RULE
    - Turoni surrenders to R
    - R move Caesar+4 Metiosedum->Turoni ops=['siege']
    - Imperator AP: SIEGE
    - IM removed: Cenabum (G)
    - R move P. Crassus+2 Agedincum->Cenabum ops=['remove_im']
    - Imperator AP: RAID
    - isolated R IM removed Aduatuci
    - isolated R IM removed Tungri
    - VP +1 governance 8 -> 4
    - governance 8

*End of Turn 2: Celtica provinces Rome 7 / Gaul 1; Belgica Rome 2 / Gaul 2; Fortified Towns 4; Provincia provinces lost: none; Roman VP 4.*

## Turn 3

- tribe Aulerci placed at Eburovices
- tribe Aquitani placed at Tarbelli
- tribe Armorici placed at Venelli
- **Concilium** plays #33 Local Raids as **bonus**
- **Imperator** plays #51 Stratagem & Treachery as **ap**
- **Concilium** plays #36 Encourage the Timid as **event**
- **Imperator** plays #4 Aid From Crassus as **event**
- **Concilium** plays #27 Unrest in Provincia as **event**
- **Imperator** plays #2 Constant as the Northern Star as **bonus**
- **Concilium** plays #37 Motus Ubique as **event**
- **Imperator** plays #50 Naval Supremacy as **ap**
- **Concilium** plays #7 Belgic Resentment as **event**
- **Imperator** plays #9 Destroyed Root & Branch as **ap**
- **Concilium** plays #8 Druidic Influence as **event**
- **Imperator** plays #25 Mercenaries From Britannia and Hispania as **ap**
- **Concilium** plays #29 German Auxiliary Cavalry as **ap**
- **Imperator** plays #46 Local Raids as **ap**
- **Concilium** plays #49 Three Days March as **ap**
- **Imperator** plays #47 Winter Campaign as **ap**
    - VP +2 governance 10 -> 6
    - governance 10

*End of Turn 3: Celtica provinces Rome 9 / Gaul 1; Belgica Rome 3 / Gaul 2; Fortified Towns 7; Provincia provinces lost: none; Roman VP 6.*

## Turn 4

- tribe Bellovaci placed at Iuliobona
- tribe Santones placed at Santoni
- tribe Eburones placed at Aduatuci
- **Concilium** plays #16 Trumpets of War as **event**
    - R avoids battle Cenomani->Diablintes
- **Imperator** plays #12 Roman Rule as **event**
- **Concilium** plays #11 For the Glory of Caesar as **ap**
- **Imperator** plays #38 Motus Ubique as **ap**
- **Concilium** plays #5 The Belgic Confederation as **event**
- **Imperator** plays #46 Local Raids as **bonus**
- **Concilium** plays #14 Glory & Liberty as **event**
- **Imperator** plays #18 Hostages as **bonus**
- **Concilium** plays #2 Constant as the Northern Star as **ap**
- **Imperator** plays #37 Motus Ubique as **ap**
- **Concilium** plays #49 Three Days March as **ap**
- **Imperator** plays #40 Unrest Spreads as **bonus**
- **Concilium** plays #20 Roman Auxiliaries as **ap**
- **Imperator** plays #21 Ties of Blood and Marriage as **ap**
- **Concilium** plays #43 The Aedui Switch Sides as **ap**
- **Imperator** plays #7 Belgic Resentment as **ap**
    - G avoids battle Petrocorii->Iculisma
    - VP +1 governance 7 -> 7
    - governance 7

*End of Turn 4: Celtica provinces Rome 7 / Gaul 0; Belgica Rome 2 / Gaul 3; Fortified Towns 10; Provincia provinces lost: none; Roman VP 7.*

## Turn 5

- tribe Arverni submits on arrival
- tribe Senones submits on arrival
- **Concilium** plays #27 Unrest in Provincia as **event**
    - R cancels #27 with #24
- **Concilium** plays #44 Legate Called to Rome as **bonus**
- **Imperator** plays #35 German Migration as **bonus**
    - German tribe to Nemetes
- **Concilium** plays #13 Gallic War Council as **event**
- **Imperator** plays #31 A Friend of Rome as **bonus**
    - Gauls at Metiosedum submit to Caesar (12:4)
    - eliminated Aulerci submit
    - eliminated Vercingetorix submit
- **Concilium** plays #19 Roman Trade as **ap**
- **Imperator** plays #8 Druidic Influence as **ap**
    - R move Caesar+6 Metiosedum->Portus Itius ops=['siege']
- **Concilium** plays #53 Trumpets of War as **event**
- **Imperator** plays #4 Aid From Crassus as **ap**
    - Gauls at Veliocasses submit to Caesar (12:4)
    - eliminated Bellovaci submit
- **Concilium** plays #50 Naval Supremacy as **ap**
- **Imperator** plays #17 Caesar's Lieutenant as **bonus**
    - Gauls at Abrincatui submit to Caesar (12:4)
- **Concilium** plays #9 Destroyed Root & Branch as **ap**
- **Imperator** plays #30 German Auxiliary Cavalry as **ap**
    - Gauls at Brigiosum submit to Caesar (12:4)
- **Concilium** plays #26 Mercenaries From Britannia and Hispania as **bonus**
- **Imperator** plays #28 Alesia as **ap**
    - Gauls at Lemovices submit to Caesar (12:4)
- **Concilium** plays #45 Diplomacy as **event**
- **Imperator** plays #32 Caesar's Legions as **bonus**
    - battle Tarbelli R4 vs G2: hits 1/2 -> D
    - eliminated Mercenaries 1 loss
    - eliminated XIII loss
    - G avoids battle Autricum->Lexovii
    - VP +2 governance 10 -> 9
    - governance 10

*End of Turn 5: Celtica provinces Rome 11 / Gaul 0; Belgica Rome 4 / Gaul 3; Fortified Towns 5; Provincia provinces lost: none; Roman VP 9.*

## Turn 6

- tribe Remi placed at Segni
- tribe Leuci placed at Triboci
- tribe Cadurci placed at Petrocorii
- **Concilium** plays #22 Burn the Countryside as **bonus**
    - tribe Armorici placed at Lexovii
    - tribe Santones placed at Iculisma
- **Imperator** plays #39 Incite Through Sedition as **bonus**
- **Concilium** plays #6 A United Gaul as **event**
- **Imperator** plays #47 Winter Campaign as **ap**
- **Concilium** plays #36 Encourage the Timid as **event**
- **Imperator** plays #1 Veni Vidi Vici as **bonus**
- **Concilium** plays #33 Local Raids as **bonus**
    - R intercepts into Lutetia from Autricum
    - battle Lutetia G2 vs R6: hits 0/3 -> D
    - eliminated Armorici loss
- **Imperator** plays #34 German Migration as **bonus**
    - German tribe to Eburones
- **Concilium** plays #23 Gaul of the Long-Hairs as **bonus**
- **Imperator** plays #29 German Auxiliary Cavalry as **bonus**
    - Curiosolites surrenders to R
    - R move Caesar+5 Turoni->Curiosolites ops=['siege']
- **Concilium** plays #25 Mercenaries From Britannia and Hispania as **bonus**
- **Imperator** plays #51 Stratagem & Treachery as **ap**
- **Concilium** plays #3 Aid From Pompey as **ap**
- **Imperator** plays #41 A Call to Arms as **ap**
    - battle Caleti R12 vs G8: hits 3/3 -> A
    - eliminated Mercenaries 1 loss
    - eliminated Atrebates loss
    - eliminated Ambiorix loss
- **Concilium** plays #48 Roman Bribes as **ap**
- **Imperator** plays #42 Senate Outraged as **ap**
    - VP +1 governance 8 -> 10
    - governance 8

*End of Turn 6: Celtica provinces Rome 10 / Gaul 0; Belgica Rome 3 / Gaul 3; Fortified Towns 7; Provincia provinces lost: none; Roman VP 10.*

**Result:** Gaul wins (end VP 10). Battles 4, siege rolls 5, Tribes eliminated 7, Legions still eliminated at the end 1 (XIII).
