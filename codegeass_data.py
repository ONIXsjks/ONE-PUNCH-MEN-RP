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
# ============================================================
# CODE GEASS STATS - آمار کاراکترهای کد گیاس
# ============================================================

CODEGEASS_STATS = {
    # ============ S RANK ============
    "Lelouch Lamperouge": {
        "hp": 2500, "atk": 540, "def": 220, "dodge": 40,
        "price": 5000000,
    },
    "Suzaku Kururugi": {
        "hp": 2500, "atk": 530, "def": 225, "dodge": 42,
        "price": 5000000,
    },
    "C.C.": {
        "hp": 2500, "atk": 520, "def": 230, "dodge": 38,
        "price": 4800000,
    },
    "Charles zi Britannia": {
        "hp": 2500, "atk": 550, "def": 230, "dodge": 35,
        "price": 5000000,
    },
    "V.V.": {
        "hp": 2450, "atk": 520, "def": 220, "dodge": 38,
        "price": 4500000,
    },
    "Schneizel el Britannia": {
        "hp": 2500, "atk": 540, "def": 230, "dodge": 38,
        "price": 4800000,
    },
    "Bismarck Waldstein": {
        "hp": 2500, "atk": 540, "def": 230, "dodge": 40,
        "price": 4800000,
    },
    "Marianne vi Britannia": {
        "hp": 2450, "atk": 525, "def": 220, "dodge": 42,
        "price": 4500000,
    },
    "Kallen Stadtfeld": {
        "hp": 2450, "atk": 530, "def": 220, "dodge": 40,
        "price": 4500000,
    },
    "Gino Weinberg": {
        "hp": 2400, "atk": 515, "def": 215, "dodge": 40,
        "price": 4200000,
    },

    # ============ A RANK ============
    "Cecile Croomy": {
        "hp": 1080, "atk": 220, "def": 78, "dodge": 24,
        "price": 580000,
    },
    "Lloyd Asplund": {
        "hp": 1050, "atk": 215, "def": 75, "dodge": 24,
        "price": 560000,
    },
    "Shirley Fenette": {
        "hp": 1050, "atk": 215, "def": 75, "dodge": 26,
        "price": 560000,
    },
    "Milly Ashford": {
        "hp": 1080, "atk": 220, "def": 78, "dodge": 25,
        "price": 580000,
    },
    "Rivalz Cardemonde": {
        "hp": 1080, "atk": 215, "def": 78, "dodge": 24,
        "price": 570000,
    },
    "Nina Einstein": {
        "hp": 1050, "atk": 220, "def": 75, "dodge": 25,
        "price": 570000,
    },
    "Euphemia li Britannia": {
        "hp": 1100, "atk": 225, "def": 80, "dodge": 26,
        "price": 600000,
    },
    "Cornelia li Britannia": {
        "hp": 1100, "atk": 225, "def": 82, "dodge": 24,
        "price": 600000,
    },
    "Diethard Ried": {
        "hp": 1080, "atk": 220, "def": 78, "dodge": 24,
        "price": 580000,
    },
    "Jeremiah Gottwald": {
        "hp": 1100, "atk": 225, "def": 82, "dodge": 22,
        "price": 590000,
    },

    # ============ B RANK ============
    "Rolo Lamperouge": {
        "hp": 700, "atk": 122, "def": 40, "dodge": 18,
        "price": 155000,
    },
    "Villetta Nu": {
        "hp": 700, "atk": 120, "def": 40, "dodge": 17,
        "price": 150000,
    },
    "Ohgi Kaname": {
        "hp": 700, "atk": 120, "def": 40, "dodge": 16,
        "price": 150000,
    },
    "Tamaki Shinichiro": {
        "hp": 680, "atk": 118, "def": 38, "dodge": 17,
        "price": 148000,
    },
    "Kallen Kozuki": {
        "hp": 720, "atk": 125, "def": 42, "dodge": 18,
        "price": 160000,
    },
    "Naoto Kozuki": {
        "hp": 700, "atk": 120, "def": 40, "dodge": 17,
        "price": 155000,
    },
    "Rakshata Chawla": {
        "hp": 680, "atk": 118, "def": 38, "dodge": 16,
        "price": 150000,
    },
    "Viletta Nu": {
        "hp": 700, "atk": 120, "def": 40, "dodge": 17,
        "price": 150000,
    },
    "Anya Alstreim": {
        "hp": 700, "atk": 122, "def": 40, "dodge": 17,
        "price": 155000,
    },
    "Nunnally vi Britannia": {
        "hp": 680, "atk": 115, "def": 38, "dodge": 16,
        "price": 148000,
    },
}