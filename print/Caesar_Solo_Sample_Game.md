# Sample game: Imperator (level 3) vs Concilium (level 3)

Both sides are bots, so every decision below follows the printed rules. Seed 47 (bots v1.0). Imperator gets +1 AP on every card play (level 3); Concilium plays the plain rules. Lines starting with a Directive show the card turned over, the two cards of the Offer (* = Event Live for the bot) and the card chosen. "AP:" lines show the mission that spent each Action Point. Moves list the leader, the number of CUs, start and end space and the operations performed. Turns 1 and 2 are shown in full; later turns list only the cards played, combat, sieges, Tribes and VP.

## How this game went

* **Turn 1.** Labienus takes the two Legions at Vienne to Octodurus while Caesar's six Legions RAID near Bibracte. Labienus opens Caesar's Pass on his third roll (+1 VP). Caesar's army, at better than 2:1, then besieges the new Pictones Town at Pictavi. Two rolls later the Town falls and the Pictones are eliminated. Isolation strips away five cut-off Gallic IMs. Rome holds Celtica 5–0 but trails in Belgica 1–2: Governance 8, +1 VP.
* **Turn 2.** Concilium's *Druidic Influence* wipes out four Roman IMs around Vesontio. *Senate Outraged* gives it a second play in a row. Imperator's Control Table now puts Belgica, the lagging region, first. Caesar marches north with three Legions and RAIDs Durocortorum, Condrusi, Treveri and Eburones. At Aduatuci he forces a Gallic stack to Submit at 4:1. Belgica swings to 4–1: Governance 10, +2 VP.
* **Turn 3.** A siege brings down the Nervii's Fortified Town. A Gallic interception at Bratuspantium costs Rome Legion X but destroys the Remi. Celtica stands at 7–1 and Belgica at 5–0: Governance 10, +2 VP.
* **Turn 4.** Caesar is delayed in Rome this turn. Concilium's *Trumpets of War* chases a lone Roman stack across the west, and Gaul wins back three Celtic provinces (5–3). Rome still dominates both regions: Governance 10, +2 VP, for 7 VP.
* **Turn 5.** The Arverni Submit on arrival. Caesar's army sits at Samarobriva for three siege rolls until the Town falls, and the Bellovaci and Ambiorix are eliminated with it. Belgica is now 6–0: Governance 10, +2 VP, for 11 VP.
* **Turn 6.** The Leuci, Parisii and Senones all Submit on arrival. Imperator cancels *Ties of Blood and Marriage* with #24, and a last siege at Autricum eliminates the Carnutes. Rome has lost its foothold in Aquitania, so Governance is 9, but that still gives +2 VP. Add +1 for six eliminated Tribes, and **Rome wins with 13 VP.**

What this game shows about the bots:

* **Imperator** plays two games at once. Its RULE and RAID missions hold the Governance race. Caesar's big army forces Submissions and takes Fortified Towns, which it may besiege whenever it has 2:1. The Control Table always works first on the region Rome is losing.
* **Concilium** Raids wherever the Legions are not and plays its Events for big swings (*Druidic Influence*, *Trumpets of War*). It never sweeps into danger, so it fights few battles.
* **Governance decides the race, turn by turn.** Rome needs dominance in both Celtica and Belgica nearly every winter. Here it managed that in five winters out of six.

## How to read the log

* A **Directive** line shows the Directive card turned over and its missions, then the Offer of two cards (* marks a card whose Event is Live for the bot) and the card chosen.
* A **plays** line gives the card and how it was used: as an Event, as a Bonus card (Event, then AP), or for AP.
* An **AP:** line names the mission that spent one Action Point (rules 2.5).
* A **move** line gives the leader, the number of units moving with him, the start and end spaces, and the operations done on the way.
* A **battle** line reads *attacker BS vs defender BS: hits scored by the attacker / hits scored by the defender → winner* (A or D).
* A **siege** line gives the Siege Table column, the roll, the attacker's losses and the Siege Points before and after.
* Turns 1 and 2 are shown in full. From Turn 3 on, the log shows only the cards played, combat, sieges, Tribe arrivals and VP.

## The log



## Turn 1

- tribe Aulerci placed at Eburovices
- tribe Nervii placed at Nervii
- tribe Pictones placed at Pictavi
- Concilium Directive Raid (N): RAID > AMBUSH > AGITATE > BANK; Offer #1, #7 -> #1
- **Concilium** plays #1 Veni Vidi Vici as **ap**
    - G influence place Condrusi
    - Concilium AP: AGITATE
    - G influence place Alesia
    - Concilium AP: AGITATE
    - G influence place Gorgobina
    - Concilium AP: AGITATE
- Imperator Directive Pacify (S): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #3, #25 -> #3
- **Imperator** plays #3 Aid From Pompey as **ap**
    - siege Octodurus col2 roll5: loss 1 pts 1 -> 1
    - R move Labienus+2 Vienne->Octodurus ops=['siege']
    - Imperator AP: SIEGE
    - R influence place Vellavi
    - Imperator AP: SETTLE
    - R influence place Gergovia
    - Imperator AP: SETTLE
- Concilium Directive Agitate (E): AGITATE > RAID > AMBUSH > BANK; Offer #35*, #2 -> #2
- **Concilium** plays #2 Constant as the Northern Star as **ap**
    - G influence place Cambiovicenses
    - Concilium AP: AGITATE
    - G influence place Nemetes
    - Concilium AP: AGITATE
    - G influence place Vangiones
    - Concilium AP: AGITATE
- Imperator Directive Pacify (N): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #33*, #26 -> #33
- **Imperator** plays #33 Local Raids as **bonus**
    - IM removed: Gorgobina (G)
    - siege Octodurus col2 roll7: loss 0 pts 1 -> 2
    - R move Labienus+2 Octodurus->Octodurus ops=['siege']
    - Imperator AP: CONTINUE
    - R influence place Gorgobina
    - Imperator AP: RULE
    - IM removed: Cambiovicenses (G)
    - R move Caesar+6 Bibracte->Cambiovicenses ops=['remove_im']
    - Imperator AP: RAID
- Concilium Directive Revolt (S): RISE > RAID > AMBUSH > AGITATE; Offer #21*, #7 -> #21
- **Concilium** plays #21 Ties of Blood and Marriage as **event**
    - tribe Bellovaci placed at Samarobriva
- Imperator Directive Pacify (W): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #26, #27 -> #26
- **Imperator** plays #26 Mercenaries From Britannia and Hispania as **ap**
    - siege Octodurus col2 roll5: loss 1 pts 1 -> 3
    - stronghold Octodurus subjugated
    - VP +1 Caesar's Pass -> 1
    - R move Labienus+2 Octodurus->Octodurus ops=['siege']
    - Imperator AP: CONTINUE
    - siege Pictavi col3 roll9: loss 0 pts 2 -> 2
    - R move Caesar+6 Cambiovicenses->Pictavi ops=['siege']
    - Imperator AP: SIEGE
    - R influence place Suessiones
    - Imperator AP: SETTLE
- Concilium Directive Council (N): RISE > BANK > AGITATE > RAID; Offer #37, #31 -> #37
- **Concilium** plays #37 Motus Ubique as **ap**
    - Concilium AP: BANK
    - Concilium AP: BANK
- Imperator Directive Rule (N): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #25, #17* -> #17
- **Imperator** plays #17 Caesar's Lieutenant as **bonus**
    - siege Pictavi col3 roll10: loss 1 pts 3 -> 5
    - eliminated Pictones siege
    - Pictavi falls to R
    - R move Caesar+6 Pictavi->Pictavi ops=['siege']
    - Imperator AP: CONTINUE
    - R influence place Silvanectes
    - Imperator AP: RULE
    - R influence place Segni
    - Imperator AP: SETTLE
- Concilium Directive Revolt (N): RISE > AMBUSH > RAID > AGITATE; Offer #35*, #31 -> #35
- **Concilium** plays #35 German Migration as **bonus**
    - G influence place Durocortorum
    - Concilium AP: AGITATE
    - G influence place Catalauni
    - Concilium AP: AGITATE
- Imperator Directive Campaign (S): RULE > SIEGE > STRIKE > RAID > SETTLE; Offer #25, #40* -> #40
- **Imperator** plays #40 Unrest Spreads as **bonus**
    - IM removed: Nemetes (G)
    - R influence place Virodunum
    - Imperator AP: SETTLE
    - R influence place Divodurum
    - Imperator AP: SETTLE
    - R influence place Nemetes
    - Imperator AP: SETTLE
- Concilium Directive Agitate (W): AGITATE > AMBUSH > RAID > BANK; Offer #31, #45* -> #31
- **Concilium** plays #31 A Friend of Rome as **ap**
    - G influence place Treveri
    - Concilium AP: AGITATE
    - G influence place Cambiovicenses
    - Concilium AP: AGITATE
- Imperator Directive Pacify (E): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #25, #43 -> #25
- **Imperator** plays #25 Mercenaries From Britannia and Hispania as **ap**
    - IM removed: Cambiovicenses (G)
    - R move Caesar+6 Pictavi->Cambiovicenses ops=['remove_im']
    - Imperator AP: RAID
    - R influence place Metiosedum
    - Imperator AP: SETTLE
    - R influence place Lutetia
    - Imperator AP: RULE
- Concilium Directive Ambush (E): AMBUSH > RAID > AGITATE > BANK; Offer #7*, #45* -> #7
- **Concilium** plays #7 Belgic Resentment as **event**
    - G influence place Meldi
- Imperator Directive Raid (E): RAID > RULE > SIEGE > SETTLE > STRIKE; Offer #43, #27 -> #43
- **Imperator** plays #43 The Aedui Switch Sides as **ap**
    - R influence place Cenabum
    - Imperator AP: SETTLE
    - R influence place Autricum
    - Imperator AP: RULE
    - R influence place Ausci
    - Imperator AP: SETTLE
- Concilium Directive Council (W): BANK > AGITATE > RAID > AMBUSH; Offer #45* -> #45
- **Concilium** plays #45 Diplomacy as **event**
- Imperator Directive Glory (N): RULE > INVADE > SIEGE > RAID > SETTLE; Offer #27 -> #27
- **Imperator** plays #27 Unrest in Provincia as **ap**
    - R influence place Sotiates
    - Imperator AP: RULE
    - R influence place Mediomatrici
    - Imperator AP: SETTLE
    - R influence place Tullum
    - Imperator AP: SETTLE
    - isolated G IM removed Durocortorum
    - isolated G IM removed Meldi
    - isolated G IM removed Catalauni
    - isolated G IM removed Alesia
    - isolated G IM removed Ambrussum
    - VP +1 governance 8 -> 2
    - governance 8

*End of Turn 1: Celtica provinces Rome 5 / Gaul 0; Belgica Rome 1 / Gaul 2; Fortified Towns 3; Provincia provinces lost: none; Roman VP 2.*

## Turn 2

- tribe Veneti placed at Curiosolites
- tribe Suessiones placed at Meldi
- tribe Santones placed at Santoni
- Concilium Directive Raid (S): RAID > AGITATE > AMBUSH > BANK; Offer #42*, #47 -> #42
- **Concilium** plays #42 Senate Outraged as **event**
- Concilium Directive Revolt (N): RISE > AMBUSH > RAID > AGITATE; Offer #18, #49 -> #18
- **Concilium** plays #18 Hostages as **ap**
    - G influence place Redones
    - Concilium AP: AGITATE
    - G influence place Durocortorum
    - Concilium AP: AGITATE
- Imperator Directive Rule (W): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #23, #29* -> #29
- **Imperator** plays #29 German Auxiliary Cavalry as **bonus**
    - R influence place Catalauni
    - Imperator AP: RULE
    - R influence place Leuci
    - Imperator AP: RULE
    - IM removed: Durocortorum (G)
    - R move Caesar+3 Vellaunodurum->Durocortorum ops=['remove_im']
    - Imperator AP: RAID
- Concilium Directive Council (N): RISE > BANK > AGITATE > RAID; Offer #12, #8* -> #8
- **Concilium** plays #8 Druidic Influence as **event**
    - IM removed: Rauraci (R)
    - IM removed: Magetobriga (R)
    - IM removed: Epomanduodurum (R)
    - IM removed: Vesontio (R)
- Imperator Directive Glory (N): RULE > INVADE > SIEGE > RAID > SETTLE; Offer #16, #48* -> #16
- **Imperator** plays #16 Trumpets of War as **ap**
    - IM removed: Condrusi (G)
    - R move Caesar+3 Durocortorum->Condrusi ops=['remove_im']
    - Imperator AP: RAID
    - R influence place Condrusi
    - Imperator AP: SETTLE
    - R influence place Bagacum
    - Imperator AP: SETTLE
    - R influence place Viromandui
    - Imperator AP: SETTLE
- Concilium Directive Revolt (S): RISE > RAID > AMBUSH > AGITATE; Offer #49, #47 -> #49
- **Concilium** plays #49 Three Days March as **ap**
    - G influence place Durocortorum
    - Concilium AP: AGITATE
    - G influence place Bratuspantium
    - Concilium AP: AGITATE
- Imperator Directive Pacify (E): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #34*, #48* -> #34
- **Imperator** plays #34 German Migration as **bonus**
    - IM removed: Vangiones (G)
    - German tribe to Vangiones
    - IM removed: Treveri (G)
    - R move Caesar+3 Condrusi->Treveri ops=['remove_im']
    - Imperator AP: RAID
    - R influence place Treveri
    - Imperator AP: RULE
    - R influence place Tungri
    - Imperator AP: SETTLE
- Concilium Directive Raid (S): RAID > AGITATE > AMBUSH > BANK; Offer #20, #47 -> #20
- **Concilium** plays #20 Roman Auxiliaries as **ap**
    - G influence place Eburones
    - Concilium AP: AGITATE
    - G influence place Aduatuci
    - Concilium AP: AGITATE
- Imperator Directive Pacify (S): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #42, #48* -> #48
- **Imperator** plays #48 Roman Bribes as **event**
- Concilium Directive Agitate (E): AGITATE > RAID > AMBUSH > BANK; Offer #12, #47 -> #12
- **Concilium** plays #12 Roman Rule as **ap**
    - G influence place Namnetes
    - Concilium AP: AGITATE
    - G influence place Agedincum
    - Concilium AP: AGITATE
- Imperator Directive Campaign (S): RULE > SIEGE > STRIKE > RAID > SETTLE; Offer #23, #42 -> #23
- **Imperator** plays #23 Gaul of the Long-Hairs as **ap**
    - IM removed: Eburones (G)
    - R move Caesar+3 Treveri->Eburones ops=['remove_im']
    - Imperator AP: RAID
    - R influence place Eburones
    - Imperator AP: RULE
    - R influence place Cubi
    - Imperator AP: SETTLE
- Concilium Directive Raid (N): RAID > AMBUSH > AGITATE > BANK; Offer #47, #15* -> #15
- **Concilium** plays #15 Exchange of Oaths as **bonus**
    - IM removed: Redones (R)
    - G move stack+1 Curiosolites->Redones ops=['remove_im']
    - Concilium AP: RAID
    - IM removed: Silvanectes (R)
    - G move stack+1 Meldi->Silvanectes ops=['remove_im']
    - Concilium AP: RAID
- Imperator Directive Raid (E): RAID > RULE > SIEGE > SETTLE > STRIKE; Offer #42, #28 -> #28
- **Imperator** plays #28 Alesia as **ap**
    - Gauls at Aduatuci submit to Caesar (8:2)
    - R move Caesar+3 Eburones->Aduatuci ops=[]
    - Imperator AP: SUBMIT
    - R influence convert Aduatuci
    - Imperator AP: RULE
    - R influence place Avaricum
    - Imperator AP: SETTLE
- Concilium Directive Ambush (E): AMBUSH > RAID > AGITATE > BANK; Offer #47 -> #47
- **Concilium** plays #47 Winter Campaign as **ap**
    - G influence place Silvanectes
    - Concilium AP: AGITATE
- Imperator Directive Pacify (W): RULE > SIEGE > RAID > SETTLE > STRIKE; Offer #42 -> #42
- **Imperator** plays #42 Senate Outraged as **ap**
    - R influence place Turoni
    - Imperator AP: RULE
    - R influence place Lexovii
    - Imperator AP: SETTLE
- Concilium Directive Council (W): BANK > AGITATE > RAID > AMBUSH; Offer #11 -> #11
- **Concilium** plays #11 For the Glory of Caesar as **ap**
    - Concilium AP: BANK
    - Concilium AP: BANK
    - Concilium AP: BANK
- Imperator Directive Rule (N): RULE > RAID > SIEGE > SETTLE > STRIKE; Offer #38* -> #38
- **Imperator** plays #38 Motus Ubique as **event**
    - VP +2 governance 10 -> 4
    - governance 10

*End of Turn 2: Celtica provinces Rome 5 / Gaul 1; Belgica Rome 4 / Gaul 1; Fortified Towns 6; Provincia provinces lost: none; Roman VP 4.*

## Turn 3

- tribe Remi placed at Durocortorum
- tribe Aquitani placed at Tarbelli
- **Concilium** plays #53 Trumpets of War as **event**
- **Imperator** plays #5 The Belgic Confederation as **ap**
    - siege Nervii col3 roll10: loss 1 pts 3 -> 3
    - eliminated Nervii fort fell
    - Nervii falls to R
    - R move Caesar+2 Turnacum->Nervii ops=['siege']
- **Concilium** plays #13 Gallic War Council as **event**
- **Imperator** plays #32 Caesar's Legions as **bonus**
- **Concilium** plays #14 Glory & Liberty as **event**
- **Imperator** plays #6 A United Gaul as **ap**
- **Concilium** plays #10 The Reach of Rome as **ap**
- **Imperator** plays #46 Local Raids as **bonus**
    - G intercepts into Bratuspantium from Suessiones
    - battle Bratuspantium R3 vs G7: hits 2/1 -> A
    - eliminated Remi loss
    - eliminated X loss
- **Concilium** plays #41 A Call to Arms as **ap**
- **Imperator** plays #30 German Auxiliary Cavalry as **bonus**
- **Concilium** plays #36 Encourage the Timid as **event**
- **Imperator** plays #19 Roman Trade as **bonus**
- **Concilium** plays #9 Destroyed Root & Branch as **ap**
- **Imperator** plays #39 Incite Through Sedition as **bonus**
- **Concilium** plays #24 You May Believe What You Wish as **ap**
- **Imperator** plays #44 Legate Called to Rome as **ap**
    - VP +2 governance 10 -> 6
    - governance 10

*End of Turn 3: Celtica provinces Rome 7 / Gaul 1; Belgica Rome 5 / Gaul 0; Fortified Towns 6; Provincia provinces lost: none; Roman VP 5.*

## Turn 4

- tribe Cadurci placed at Carantomagus
- tribe Atrebates placed at Portus Itius
- tribe Armorici placed at Venelli
- Caesar delayed
- **Concilium** plays #18 Hostages as **ap**
- **Imperator** plays #16 Trumpets of War as **ap**
- **Concilium** plays #53 Trumpets of War as **event**
    - R avoids battle Esubii->Abrincatui
    - R avoids battle Abrincatui->Diablintes
    - R avoids battle Diablintes->Andes
    - R avoids battle Andes->Turoni
    - R avoids battle Turoni->Cenabum
- **Imperator** plays #4 Aid From Crassus as **event**
- **Concilium** plays #10 The Reach of Rome as **ap**
- **Imperator** plays #35 German Migration as **bonus**
- **Concilium** plays #37 Motus Ubique as **event**
- **Imperator** plays #20 Roman Auxiliaries as **ap**
- **Concilium** plays #6 A United Gaul as **event**
- **Imperator** plays #32 Caesar's Legions as **bonus**
- **Concilium** plays #38 Motus Ubique as **event**
- **Imperator** plays #40 Unrest Spreads as **ap**
- **Concilium** plays #50 Naval Supremacy as **ap**
- **Imperator** plays #36 Encourage the Timid as **ap**
- **Concilium** plays #42 Senate Outraged as **ap**
    - tribe Bituriges placed at Turoni
- **Imperator** plays #47 Winter Campaign as **ap**
    - VP +2 governance 10 -> 8
    - governance 10

*End of Turn 4: Celtica provinces Rome 5 / Gaul 3; Belgica Rome 5 / Gaul 1; Fortified Towns 10; Provincia provinces lost: none; Roman VP 7.*

## Turn 5

- tribe Carnutes placed at Autricum
- tribe Arverni submits on arrival
- **Concilium** plays #25 Mercenaries From Britannia and Hispania as **bonus**
- **Imperator** plays #23 Gaul of the Long-Hairs as **ap**
- **Concilium** plays #49 Three Days March as **ap**
- **Imperator** plays #46 Local Raids as **bonus**
    - siege Samarobriva col1 roll8: loss 0 pts 1 -> 1
    - R move Caesar+6 Lexovii->Samarobriva ops=['siege']
- **Concilium** plays #5 The Belgic Confederation as **event**
- **Imperator** plays #34 German Migration as **bonus**
    - siege Samarobriva col1 roll2: loss 1 pts 0 -> 1
    - R move Caesar+6 Samarobriva->Samarobriva ops=['siege']
- **Concilium** plays #28 Alesia as **bonus**
- **Imperator** plays #8 Druidic Influence as **ap**
    - siege Samarobriva col1 roll11: loss 0 pts 2 -> 3
    - eliminated Bellovaci siege
    - eliminated Ambiorix siege
    - Samarobriva falls to R
    - R move Caesar+6 Samarobriva->Samarobriva ops=['siege']
- **Concilium** plays #19 Roman Trade as **ap**
- **Imperator** plays #30 German Auxiliary Cavalry as **bonus**
- **Concilium** plays #3 Aid From Pompey as **ap**
- **Imperator** plays #27 Unrest in Provincia as **ap**
- **Concilium** plays #51 Stratagem & Treachery as **ap**
- **Imperator** plays #22 Burn the Countryside as **ap**
- **Concilium** plays #17 Caesar's Lieutenant as **ap**
- **Imperator** plays #43 The Aedui Switch Sides as **ap**
    - VP +2 governance 10 -> 10
    - governance 10

*End of Turn 5: Celtica provinces Rome 5 / Gaul 3; Belgica Rome 6 / Gaul 0; Fortified Towns 10; Provincia provinces lost: none; Roman VP 11.*

## Turn 6

- tribe Leuci submits on arrival
- tribe Parisii submits on arrival
- tribe Senones submits on arrival
- **Concilium** plays #9 Destroyed Root & Branch as **ap**
- **Imperator** plays #1 Veni Vidi Vici as **bonus**
- **Concilium** plays #7 Belgic Resentment as **event**
- **Imperator** plays #13 Gallic War Council as **ap**
- **Concilium** plays #21 Ties of Blood and Marriage as **event**
    - R cancels #21 with #24
- **Concilium** plays #26 Mercenaries From Britannia and Hispania as **bonus**
- **Imperator** plays #39 Incite Through Sedition as **bonus**
    - R move Caesar+5 Iuliobona->Meldi ops=['siege']
- **Concilium** plays #44 Legate Called to Rome as **bonus**
- **Imperator** plays #33 Local Raids as **ap**
- **Concilium** plays #12 Roman Rule as **ap**
- **Imperator** plays #11 For the Glory of Caesar as **event**
- **Concilium** plays #2 Constant as the Northern Star as **ap**
- **Imperator** plays #14 Glory & Liberty as **ap**
- **Concilium** plays #48 Roman Bribes as **ap**
- **Imperator** plays #29 German Auxiliary Cavalry as **bonus**
    - siege Autricum col3 roll10: loss 1 pts 3 -> 3
    - eliminated Carnutes siege
    - Autricum falls to R
    - R move Caesar+6 Meldi->Autricum ops=['siege']
- **Concilium** plays #31 A Friend of Rome as **ap**
- **Imperator** plays #15 Exchange of Oaths as **ap**
    - VP +2 governance 9 -> 12
    - governance 9

*End of Turn 6: Celtica provinces Rome 6 / Gaul 4; Belgica Rome 6 / Gaul 0; Fortified Towns 9; Provincia provinces lost: none; Roman VP 13.*

**Result:** Rome wins (end VP 13). Battles 1, siege rolls 10, Tribes eliminated 6, Legions still eliminated at the end 0 (Legion X was rebuilt).
