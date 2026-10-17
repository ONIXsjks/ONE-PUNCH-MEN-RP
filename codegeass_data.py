# ============================================================
# CODE GEASS DATA
# ============================================================

CHARACTERS_CODEGEASS = {
    "S": {
        "Lelouch Lamperouge": "Zero",
        "Suzaku Kururugi": "Knight of Zero",
        "C.C.": "Immortal Witch",
        "Charles zi Britannia": "Emperor of Britannia",
        "V.V.": "Geass Cult Leader",
        "Schneizel el Britannia": "White Prince",
        "Bismarck Waldstein": "Knight of One",
        "Marianne vi Britannia": "Flash",
        "Kallen Stadtfeld": "Ace of the Black Knights",
        "Gino Weinberg": "Knight of Three",
    },
    "A": {
        "Cecile Croomy": "Scientist",
        "Lloyd Asplund": "Earl of Pudding",
        "Shirley Fenette": "Student",
        "Milly Ashford": "Student Council President",
        "Rivalz Cardemonde": "Student",
        "Nina Einstein": "Scientist",
        "Euphemia li Britannia": "Princess",
        "Cornelia li Britannia": "Witch of Britannia",
        "Diethard Ried": "Journalist",
        "Jeremiah Gottwald": "Orange Boy",
    },
    "B": {
        "Rolo Lamperouge": "Fake Brother",
        "Villetta Nu": "Knightmare Pilot",
        "Ohgi Kaname": "Black Knights Leader",
        "Tamaki Shinichiro": "Black Knights",
        "Kallen Kozuki": "Resistance Fighter",
        "Naoto Kozuki": "Resistance Fighter",
        "Rakshata Chawla": "Scientist",
        "Viletta Nu": "Knightmare Pilot",
        "Anya Alstreim": "Knight of Six",
        "Nunnally vi Britannia": "Blind Princess",
    },
}

CHAR_PRICES_CODEGEASS = {"S": 5000000, "A": 600000, "B": 150000}

ABILITIES_CODEGEASS = {
    # ============ S RANK ============
    "Lelouch Lamperouge": {
        "ability_1": {"name": "Geass Command", "mult": 3},
        "ability_2": {"name": "Chess Strategy", "mult": 5},
        "ability_3": {"name": "Zero Requiem", "mult": 10, "once": True},
    },
    "Suzaku Kururugi": {
        "ability_1": {"name": "Spinzaku Kick", "mult": 3},
        "ability_2": {"name": "Lancelot Charge", "mult": 5},
        "ability_3": {"name": "Live Geass Command", "mult": 10, "once": True},
    },
    "C.C.": {
        "ability_1": {"name": "Immortal Slash", "mult": 3},
        "ability_2": {"name": "Code Awakening", "mult": 5},
        "ability_3": {"name": "Witch's Curse", "mult": 10, "once": True},
    },
    "Charles zi Britannia": {
        "ability_1": {"name": "Emperor's Command", "mult": 3},
        "ability_2": {"name": "Geass Canceler", "mult": 5},
        "ability_3": {"name": "Ragnarok Connection", "mult": 10, "once": True},
    },
    "V.V.": {
        "ability_1": {"name": "Geass Cult Strike", "mult": 3},
        "ability_2": {"name": "Immortal Curse", "mult": 5},
        "ability_3": {"name": "Code VV", "mult": 10, "once": True},
    },
    "Schneizel el Britannia": {
        "ability_1": {"name": "Tactical Command", "mult": 3},
        "ability_2": {"name": "Damocles Strike", "mult": 5},
        "ability_3": {"name": "White Prince Full", "mult": 10, "once": True},
    },
    "Bismarck Waldstein": {
        "ability_1": {"name": "Knight Sword", "mult": 3},
        "ability_2": {"name": "Geass Slash", "mult": 5},
        "ability_3": {"name": "Knight of One Full", "mult": 10, "once": True},
    },
    "Marianne vi Britannia": {
        "ability_1": {"name": "Flash Step", "mult": 3},
        "ability_2": {"name": "Knightmare Slash", "mult": 5},
        "ability_3": {"name": "Marianne Full Power", "mult": 10, "once": True},
    },
    "Kallen Stadtfeld": {
        "ability_1": {"name": "Guren Slash", "mult": 3},
        "ability_2": {"name": "Radiant Wave", "mult": 5},
        "ability_3": {"name": "Guren Seiten", "mult": 10, "once": True},
    },
    "Gino Weinberg": {
        "ability_1": {"name": "Tristan Slash", "mult": 3},
        "ability_2": {"name": "Knightmare Rush", "mult": 5},
        "ability_3": {"name": "Knight of Three Full", "mult": 10, "once": True},
    },

    # ============ A RANK ============
    "Cecile Croomy": {
        "ability_1": {"name": "Tech Strike", "mult": 3},
        "ability_2": {"name": "Data Burst", "mult": 5},
        "ability_3": {"name": "Scientist Full", "mult": 10, "once": True},
    },
    "Lloyd Asplund": {
        "ability_1": {"name": "Tech Slash", "mult": 3},
        "ability_2": {"name": "Knightmare Boost", "mult": 5},
        "ability_3": {"name": "Earl's Wrath", "mult": 10, "once": True},
    },
    "Shirley Fenette": {
        "ability_1": {"name": "Student Strike", "mult": 3},
        "ability_2": {"name": "Swim Rush", "mult": 5},
        "ability_3": {"name": "Shirley's Resolve", "mult": 10, "once": True},
    },
    "Milly Ashford": {
        "ability_1": {"name": "President Slap", "mult": 3},
        "ability_2": {"name": "Student Council Rush", "mult": 5},
        "ability_3": {"name": "Milly's Power", "mult": 10, "once": True},
    },
    "Rivalz Cardemonde": {
        "ability_1": {"name": "Motorcycle Rush", "mult": 3},
        "ability_2": {"name": "Sidecar Strike", "mult": 5},
        "ability_3": {"name": "Rivalz Full", "mult": 10, "once": True},
    },
    "Nina Einstein": {
        "ability_1": {"name": "Science Strike", "mult": 3},
        "ability_2": {"name": "FLEIJA Bomb", "mult": 5},
        "ability_3": {"name": "Nina's Wrath", "mult": 10, "once": True},
    },
    "Euphemia li Britannia": {
        "ability_1": {"name": "Royal Command", "mult": 3},
        "ability_2": {"name": "Princess Strike", "mult": 5},
        "ability_3": {"name": "Euphemia's Will", "mult": 10, "once": True},
    },
    "Cornelia li Britannia": {
        "ability_1": {"name": "Witch Slash", "mult": 3},
        "ability_2": {"name": "Knightmare Rush", "mult": 5},
        "ability_3": {"name": "Cornelia Full", "mult": 10, "once": True},
    },
    "Diethard Ried": {
        "ability_1": {"name": "Journalist Strike", "mult": 3},
        "ability_2": {"name": "Media Blast", "mult": 5},
        "ability_3": {"name": "Diethard Full", "mult": 10, "once": True},
    },
    "Jeremiah Gottwald": {
        "ability_1": {"name": "Orange Punch", "mult": 3},
        "ability_2": {"name": "Siegfried Rush", "mult": 5},
        "ability_3": {"name": "Orange Boy Full", "mult": 10, "once": True},
    },

    # ============ B RANK ============
    "Rolo Lamperouge": {
        "ability_1": {"name": "Assassin Strike", "mult": 3},
        "ability_2": {"name": "Time Stop", "mult": 5},
        "ability_3": {"name": "Rolo's Resolve", "mult": 10, "once": True},
    },
    "Villetta Nu": {
        "ability_1": {"name": "Knightmare Slash", "mult": 3},
        "ability_2": {"name": "Pilot Rush", "mult": 5},
        "ability_3": {"name": "Villetta Full", "mult": 10, "once": True},
    },
    "Ohgi Kaname": {
        "ability_1": {"name": "Resistance Strike", "mult": 3},
        "ability_2": {"name": "Black Knights Rush", "mult": 5},
        "ability_3": {"name": "Ohgi Full", "mult": 10, "once": True},
    },
    "Tamaki Shinichiro": {
        "ability_1": {"name": "Resistance Punch", "mult": 3},
        "ability_2": {"name": "Loud Rush", "mult": 5},
        "ability_3": {"name": "Tamaki Full", "mult": 10, "once": True},
    },
    "Kallen Kozuki": {
        "ability_1": {"name": "Resistance Slash", "mult": 3},
        "ability_2": {"name": "Knightmare Rush", "mult": 5},
        "ability_3": {"name": "Kallen Full", "mult": 10, "once": True},
    },
    "Naoto Kozuki": {
        "ability_1": {"name": "Resistance Strike", "mult": 3},
        "ability_2": {"name": "Black Knights Rush", "mult": 5},
        "ability_3": {"name": "Naoto Full", "mult": 10, "once": True},
    },
    "Rakshata Chawla": {
        "ability_1": {"name": "Tech Strike", "mult": 3},
        "ability_2": {"name": "Knightmare Boost", "mult": 5},
        "ability_3": {"name": "Rakshata Full", "mult": 10, "once": True},
    },
    "Viletta Nu": {
        "ability_1": {"name": "Knightmare Slash", "mult": 3},
        "ability_2": {"name": "Pilot Rush", "mult": 5},
        "ability_3": {"name": "Viletta Full", "mult": 10, "once": True},
    },
    "Anya Alstreim": {
        "ability_1": {"name": "Knightmare Slash", "mult": 3},
        "ability_2": {"name": "Mordred Rush", "mult": 5},
        "ability_3": {"name": "Knight of Six Full", "mult": 10, "once": True},
    },
    "Nunnally vi Britannia": {
        "ability_1": {"name": "Royal Command", "mult": 3},
        "ability_2": {"name": "Princess Strike", "mult": 5},
        "ability_3": {"name": "Nunnally's Will", "mult": 10, "once": True},
    },
}