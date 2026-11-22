# Caesar: Rome vs Gaul strategy cards.
# Text summarised (paraphrased) from the 1st-edition card faces in the Vassal module.
# side: 'R' Roman-only event, 'G' Gallic-only event, 'W' either player.
# kind: 'event', 'bonus' (event + AP), 'reaction', 'surprise'.
# ap1: 1st-edition AP value.  ap2: ASSUMED 2nd-edition AP value (2E rule summary: five 3s,
# three 1s, surprises 0, rest 2); the exact 2E assignment is not public, see notes.
CARDS = {
 1: dict(title='Veni Vidi Vici', side='R', kind='bonus', ap1=3, ap2=3, text='Activate Caesar and any one Legate, then use the AP.'),
 2: dict(title='Constant as the Northern Star', side='R', kind='bonus', ap1=3, ap2=3, text='Activate Caesar, then use the AP.'),
 3: dict(title='Aid From Pompey', side='R', kind='event', ap1=3, ap2=2, text='Two replacement steps now (Legions with a Supply Path to Rome).'),
 4: dict(title='Aid From Crassus', side='R', kind='event', ap1=3, ap2=2, text='Receive 5 AP. Turns 1-4 only.'),
 5: dict(title='The Belgic Confederation', side='G', kind='event', ap1=3, ap2=3, text='Activate all Gallic Leaders and CUs in Belgica.'),
 6: dict(title='A United Gaul', side='G', kind='event', ap1=3, ap2=2, text='One Influence Action in each Gallic Province already holding a Gallic IM.'),
 7: dict(title='Belgic Resentment', side='G', kind='event', ap1=2, ap2=2, text='One Influence Action in each Belgic Province with a Roman IM or Roman CU.'),
 8: dict(title='Druidic Influence', side='G', kind='event', ap1=3, ap2=2, text='One Province in Gaul with no Roman CU: remove all Roman IMs there.'),
 9: dict(title='Destroyed Root & Branch', side='R', kind='event', ap1=2, ap2=2, text='Remove Gallic IMs in or adjacent to Caesar where no Gallic CU.'),
 10: dict(title='The Reach of Rome', side='R', kind='event', ap1=2, ap2=2, text='Place two Roman IMs ignoring adjacency.'),
 11: dict(title='For the Glory of Caesar', side='R', kind='event', ap1=3, ap2=3, text='Activate any or all Roman Leaders and Legions.'),
 12: dict(title='Roman Rule', side='R', kind='event', ap1=3, ap2=2, text='Celtica or Belgica: one Influence Action in each Province there already holding a Roman IM.'),
 13: dict(title='Gallic War Council', side='G', kind='event', ap1=2, ap2=2, text='Up to two IMs into the Council Box; restore one reduced Tribe.'),
 14: dict(title='Glory & Liberty', side='G', kind='event', ap1=3, ap2=2, text='One Influence Action in every Province with a Fortified Town.'),
 15: dict(title='Exchange of Oaths', side='G', kind='bonus', ap1=2, ap2=2, text='Place the Minor Tribe in a Gallic-controlled space in Gaul with no Roman Leader/CU, then AP.'),
 16: dict(title='Trumpets of War', side='G', kind='event', ap1=3, ap2=3, text='Activate any or all Gallic Leaders and Tribes.'),
 17: dict(title="Caesar's Lieutenant", side='R', kind='bonus', ap1=2, ap2=2, text='Labienus from cup to a Legion (return one Legate) OR activate a Legate not with Caesar, then AP.'),
 18: dict(title='Hostages', side='R', kind='bonus', ap1=2, ap2=2, text='Remove a Gallic IM in a Roman-controlled Province (no Gallic CU), then AP.'),
 19: dict(title='Roman Trade', side='R', kind='bonus', ap1=2, ap2=2, text='Remove a Gallic IM in a Province adjacent to a Roman-controlled Province (no Gallic CU), then AP.'),
 20: dict(title='Roman Auxiliaries', side='R', kind='bonus', ap1=1, ap2=2, text='Restore one reduced Legion with a Supply Path to Rome, then AP.'),
 21: dict(title='Ties of Blood and Marriage', side='G', kind='event', ap1=2, ap2=2, text='Draw a Tribe at random from the Pool and place it per 5.1.2.'),
 22: dict(title='Burn the Countryside', side='G', kind='bonus', ap1=2, ap2=2, text='Devastation in/adjacent to a Gallic CU (no enemy CU, no Walled City), then AP.'),
 23: dict(title='Gaul of the Long-Hairs', side='G', kind='bonus', ap1=2, ap2=2, text='Remove a Roman IM adjacent to a Gallic Stronghold, or one Influence Action adjacent to one, then AP.'),
 24: dict(title='You May Believe What You Wish', side='W', kind='reaction', ap1=3, ap2=2, text='Cancel the Event/Bonus Event just played; both draw a card.'),
 25: dict(title='Mercenaries From Britannia and Hispania', side='G', kind='bonus', ap1=1, ap2=2, text='Gallic Mercenary with a supplied, unbesieged Tribe/Leader/FT, then AP.'),
 26: dict(title='Mercenaries From Britannia and Hispania', side='G', kind='bonus', ap1=1, ap2=2, text='Gallic Mercenary with a supplied, unbesieged Tribe/Leader/FT, then AP.'),
 27: dict(title='Unrest in Provincia', side='G', kind='event', ap1=2, ap2=2, text='Remove up to two Roman IMs from Provincia, at most one per Province.'),
 28: dict(title='Alesia', side='G', kind='bonus', ap1=2, ap2=2, text='Upgrade one unbesieged Fortified Town to -1 DRM, then AP.'),
 29: dict(title='German Auxiliary Cavalry', side='R', kind='bonus', ap1=1, ap2=2, text='Germani Cav with a Legion that can trace supply to a German Stronghold, then AP.'),
 30: dict(title='German Auxiliary Cavalry', side='R', kind='bonus', ap1=1, ap2=2, text='Germani Cav with a Legion that can trace supply to a German Stronghold, then AP.'),
 31: dict(title='A Friend of Rome', side='R', kind='bonus', ap1=1, ap2=2, text='Convert a Gallic IM adjacent to a Roman CU, then AP.'),
 32: dict(title="Caesar's Legions", side='R', kind='bonus', ap1=2, ap2=2, text='Activate all Legions not stacked with a Legate or Caesar, then AP.'),
 33: dict(title='Local Raids', side='W', kind='bonus', ap1=1, ap2=2, text='Remove an enemy IM adjacent to a friendly unbesieged CU (no enemy CU), then AP.'),
 34: dict(title='German Migration', side='W', kind='bonus', ap1=1, ap2=2, text='Move the German Independent Tribe; remove an IM where it ends, then AP.'),
 35: dict(title='German Migration', side='W', kind='bonus', ap1=1, ap2=2, text='Move the German Independent Tribe; remove an IM where it ends, then AP.'),
 36: dict(title='Encourage the Timid', side='G', kind='event', ap1=2, ap2=2, text='One Influence Action in every Province of Gaul/Provincia with a Gallic CU.'),
 37: dict(title='Motus Ubique', side='W', kind='event', ap1=1, ap2=2, text='Activate one Leader (incl. intrinsic) in each of the six Regions.'),
 38: dict(title='Motus Ubique', side='W', kind='event', ap1=1, ap2=2, text='Activate one Leader (incl. intrinsic) in each of the six Regions.'),
 39: dict(title='Incite Through Sedition', side='W', kind='bonus', ap1=1, ap2=2, text='Remove an enemy IM in a Province holding a friendly IM (no enemy CU), then AP.'),
 40: dict(title='Unrest Spreads', side='W', kind='bonus', ap1=1, ap2=2, text='Remove one IM from a Province with a vacant space (no CU in target), then AP.'),
 41: dict(title='A Call to Arms', side='G', kind='event', ap1=2, ap2=2, text='Militia with a Tribe or unbesieged FT in Celtica or Belgica.'),
 42: dict(title='Senate Outraged', side='G', kind='event', ap1=1, ap2=1, text="Take a random card from Caesar's hand, give him this card, then play any card."),
 43: dict(title='The Aedui Switch Sides', side='G', kind='bonus', ap1=2, ap2=2, text='Aedui Tribe + FT in Aedui space free of Roman CU/IM, then AP.'),
 44: dict(title='Legate Called to Rome', side='W', kind='bonus', ap1=1, ap2=2, text='Swap one Legate on the map for a random one from the cup, then AP.'),
 45: dict(title='Diplomacy', side='W', kind='event', ap1=1, ap2=1, text='Convert an enemy IM in Gaul/Provincia free of enemy CUs.'),
 46: dict(title='Local Raids', side='W', kind='bonus', ap1=1, ap2=2, text='Remove an enemy IM adjacent to a friendly unbesieged CU (no enemy CU), then AP.'),
 47: dict(title='Winter Campaign', side='R', kind='event', ap1=1, ap2=1, text='Interrupt: Rome goes first this Strategy Phase; only one Leader activated.'),
 48: dict(title='Roman Bribes', side='R', kind='event', ap1=1, ap2=2, text='Convert a Gallic IM in Gaul/Provincia in a space with no CUs.'),
 49: dict(title='Three Days March', side='W', kind='event', ap1=1, ap2=2, text='Activate all friendly Leaders and CUs with MA 1.'),
 50: dict(title='Naval Supremacy', side='W', kind='bonus', ap1=2, ap2=2, text='Add/remove a Siege Point at a port FT/WC in a zone you dominate, then AP.'),
 51: dict(title='Stratagem & Treachery', side='W', kind='bonus', ap1=1, ap2=2, text='Add/remove a Siege Point at a besieged FT/WC, then AP.'),
 52: dict(title='A Vow to Mars', side='W', kind='surprise', ap1=0, ap2=0, text='+1 Siege DRM or 1 combat reroll; draw a replacement.'),
 53: dict(title='Trumpets of War', side='G', kind='event', ap1=2, ap2=2, text='Activate any or all Gallic Leaders and Tribes.'),
 54: dict(title='Remedies for all Contingencies', side='W', kind='surprise', ap1=0, ap2=0, text='+2/-2 to one Interception or Avoid Battle roll; draw a replacement.'),
 55: dict(title='Forced March', side='W', kind='surprise', ap1=0, ap2=0, text='+1 MP to one activated Leader/CU; draw a replacement.'),
}

def ap_value(card_id, edition=2):
    c = CARDS[card_id]
    return c['ap2'] if edition == 2 else c['ap1']

if __name__ == '__main__':
    from collections import Counter
    print('1E', Counter(c['ap1'] for c in CARDS.values()))
    print('2E', Counter(c['ap2'] for c in CARDS.values()))
