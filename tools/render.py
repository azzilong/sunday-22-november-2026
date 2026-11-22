#!/usr/bin/env python3
"""Render the Sunday 22 November 2026 front page (1024x1024 PNG).

Draws the whole image in code with Pillow: flat vector illustrations, no
photos, no copied art. Deterministic: no randomness, no clock, no network.
Run:  python3 tools/render.py [out.png]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
RED = (164, 31, 31)
RED_DARK = (138, 31, 31)
GREY = (90, 88, 80)
RULE = (120, 110, 92)
SEA = (178, 205, 219)
LAND = (232, 222, 190)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# (num, kicker, location, headline, deck, source, scene, region)
LEADS = [
    (1, "COP31: FINAL DEAL", "ANTALYA, TÜRKIYE · CLIMATE",
     "COP31 nears a final deal on Sunday",
     "A new package goes to nearly 200 nations; objections due 03:00 GMT, "
     "approval at 06:00 GMT. Fossil fuels and finance are the sticking points.",
     "Reuters, AP", "table", "EUROPE"),
    (2, "BAHRAIN: STRUCK", "MANAMA, BAHRAIN · IRAN WAR",
     "Iran strikes US bases in Bahrain",
     "Two waves of drones and missiles hit US bases on Saturday night; an "
     "industrial site burns, no injuries. Bahrain says defences intercepted it.",
     "Al Jazeera, Reuters", "flames", "MIDDLE EAST"),
    (3, "PERU: QUAKE", "JUNÍN, PERU · EARTHQUAKE",
     "Magnitude 6.7 quake shakes Peru's Andes",
     "A 6.7 quake shook central Peru, felt in Lima; no deaths or major "
     "damage reported. First reported 21 Nov 00:09 UTC.",
     "AP, USGS", "quake", "AMERICAS"),
]

MIDS = [
    (4, "SHIP ABLAZE", "GULF OF FINLAND · WAR AT SEA",
     "Russian cargo ship ablaze after drone strike",
     "The sanctioned Sparta II, hit by suspected Ukrainian drones, burns on; "
     "all 16 crew were evacuated.",
     "Reuters, Finnish Defence Forces", "ship", "EUROPE"),
    (5, "400+ DRONES", "KYIV, UKRAINE · WAR",
     "Russia fires 400 drones and 110 missiles",
     "One of the war's largest overnight attacks; at least seven people are "
     "killed in Kyiv.",
     "Al Jazeera", "drones", "EUROPE"),
    (6, "CARTEL BOSS HELD", "SINALOA, MEXICO · CRIME",
     "Mexico captures cartel boss 'El Chapo Isidro'",
     "FBI top-ten fugitive Fausto Isidro Meza Flores held after a "
     "Friday-night raid; 11 killed after.",
     "Reuters, AP", "desert", "AMERICAS"),
    (7, "2 DEAD, 60 HURT", "KRYVYI RIH · WAR",
     "Strike hits Zelenskyy's home city",
     "A Russian missile hits the central Ukrainian city; a boy of 7 and a "
     "paramedic are among the dead.",
     "AP, Al Jazeera", "missile", "EUROPE"),
    (8, "TANKERS HIT", "OFF OMAN · SHIPPING",
     "Two tankers hit off Oman within an hour",
     "Unknown projectiles strike ships near Khasab; one crew member missing. "
     "Iran says a third hit a mine.",
     "UKMTO, BBC", "tankers", "MIDDLE EAST"),
    (9, "POWER CUTS", "TEHRAN, IRAN · ENERGY",
     "Iran to ration electricity from Sunday",
     "Cuts of up to two hours a day as war damage hits the energy network; "
     "rolling blackouts begin.",
     "Straits Times", "pylon", "MIDDLE EAST"),
    (10, "3 KILLED", "GAZA CITY · CEASEFIRE",
     "Strike hits food aid vehicle",
     "Three Palestinians die in an air attack; the army says it targeted "
     "Islamic Jihad members.",
     "Al Jazeera, Reuters", "truck", "MIDDLE EAST"),
    (11, "5,700 VOTERS", "HONG KONG · POLITICS",
     "Hong Kong goes to the polls",
     "About 5,700 voters pick members of the 1,500-seat body that chooses "
     "the city's leader.",
     "AFP", "ballot", "ASIA"),
    (12, "POLE", "LAS VEGAS · FORMULA 1",
     "Verstappen on pole as Vegas races under the lights",
     "Antonelli fastest but drops five places; lights out 04:00 GMT. Norris "
     "leads the title by 30.",
     "F1, Reuters", "race", "AMERICAS"),
    (13, "FIRST TRIP", "NEW DELHI · DIPLOMACY",
     "Nepal's new PM heads to India first",
     "Flood aid and energy top Balendra Shah's talks with Modi on a two-day "
     "state visit.",
     "Reuters", "plane", "ASIA"),
]

# briefs: (num, place, text, source, region)
BRIEFS = [
    (14, "Jerusalem", "Eisenkot invites Likud", "Straits Times", "MIDDLE EAST"),
    (15, "Basra", "Power-station fire kills four, 35 hurt", "Reuters", "MIDDLE EAST"),
    (16, "Bayelsa", "Boat carrying mourners capsizes, 24 dead", "DW", "AFRICA"),
    (17, "Tallinn", "Estonia to close Russia border", "AFP", "EUROPE"),
    (18, "Patna", "Modi opens Nitish Setu bridge, 19.7 km", "PTI", "ASIA"),
    (19, "Twickenham", "England thrash All Blacks 37-12", "BBC", "EUROPE"),
    (20, "Ranchi", "Cyclone Akvan cancels 14 flights", "IMD", "ASIA"),
    (21, "Washington", "Nvidia faces accounting probe", "Straits Times", "AMERICAS"),
    (22, "Brasília", "Bolsonaro in intensive care, stable", "Reuters", "AMERICAS"),
    (23, "Canberra", "Marles rejects US report on AUKUS subs", "ABC", "OCEANIA"),
    (24, "Washington", "FBI probes hack of crime database", "BBC", "AMERICAS"),
    (25, "Copenhagen", "Denmark expels Russian attaché", "Guardian", "EUROPE"),
    (26, "Paris", "France seeks UN action on Myanmar", "AFP", "EUROPE"),
    (27, "Tokyo", "Japan to train live-fire in India, a first", "Kyodo", "ASIA"),
    (28, "US courts", "Roundup $7.25bn settlement approved", "Reuters", "AMERICAS"),
    (29, "Markets", "Bitcoin climbs back above $60,000", "Reuters", "GLOBAL"),
    (30, "Brussels", "EU–Indonesia trade deal signed", "DW", "EUROPE"),
    (31, "New York", "Gupta jailed 19 years over Pannun plot", "AP", "AMERICAS"),
    (32, "Riyadh", "Saudi downs Houthi missile", "Investing.com", "MIDDLE EAST"),
    (33, "Warsaw", "Rutte: NATO will defend “every inch”", "Reuters", "EUROPE"),
    (34, "Turin", "Zverev meets Alcaraz for ATP title", "ATP", "EUROPE"),
    (35, "W. Kordofan", "RSF gunmen kill 3 civilians", "Darfur24", "AFRICA"),
]

REGIONS = [  # (name, count, colour)
    ("EUROPE", 11, (31, 58, 110)),
    ("MIDDLE EAST", 7, (164, 31, 31)),
    ("ASIA", 5, (192, 122, 18)),
    ("AMERICAS", 8, (46, 107, 52)),
    ("AFRICA", 2, (14, 124, 123)),
    ("OCEANIA", 1, (107, 74, 138)),
    ("GLOBAL", 1, (85, 95, 107)),
]

STATS = [  # (big, caption)
    ("~200", "nations at the COP31 talks"),
    ("03:00", "GMT, objections due"),
    ("400+", "drones fired at Ukraine"),
    ("2", "US bases hit in Bahrain"),
    ("6.7", "magnitude of the Peru quake"),
    ("11", "killed after the Sinaloa raid"),
]

DATE_CHECK = (
    "Left out as earlier news: the Shenzhen summit (19 Nov) · the Kerch Bridge strikes "
    "(earlier this week) · Russian missiles landing in Poland (19 Nov) · BepiColombo’s "
    "Mercury capture (18–21 Nov) · Voyager 1 at one light-day (18 Nov) · Wall Street’s "
    "slide into correction (20 Nov) · the EU–UK deal (20 Nov) · the ICJ Myanmar ruling "
    "(19 Nov) · the Kyiv bridge strikes (19 Nov). Not confirmed when drawn: the final "
    "COP31 text (vote 06:00 GMT) · the Gulf casualty toll · the Las Vegas GP result. "
    "Dating: the Bahrain strikes began Saturday night, Sparta II was hit Saturday "
    "morning and still burns, the Peru quake was first reported 21 Nov 00:09 UTC."
)

FOOTER = (
    "Every story here happened, or was first reported, on Sunday 22 November 2026."
)
FOOTER_R = "Sources named beside each story · original drawings"


# ---------------------------------------------------------------- helpers
def wrap(text, font, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, font, fill=INK, anchor="la"):
    draw.text(xy, s, font=font, fill=fill, anchor=anchor)


def centred(draw, cx, y, s, font, fill=INK):
    draw.text((cx, y), s, font=font, fill=fill, anchor="ma")


def rule(draw, x0, x1, y, fill=RULE, w=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def flame(draw, cx, base, h, w, col):
    """A simple flame: triangle with a curved belly, apex at base-h."""
    draw.polygon([(cx - w / 2, base), (cx, base - h), (cx + w / 2, base)],
                 fill=col)
    draw.ellipse([cx - w / 4, base - h * 0.55, cx + w / 4, base - h * 0.15],
                 fill=(255, 214, 90))


# ---------------------------------------------------------------- scenes
def scene_table(d, x, y, w, h):
    """COP31: conference table, flags, globe, clock."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 205, 205))
    d.ellipse([x + 8, y + 8, x + 58, y + 58], fill=(46, 120, 170))
    d.ellipse([x + 20, y + 18, x + 46, y + 48], fill=(110, 190, 110))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(120, 82, 52))
    for i, c in enumerate([(164, 31, 31), (31, 58, 110), (46, 107, 52),
                           (192, 122, 18), (107, 74, 138)]):
        fx = x + 20 + i * (w - 40) // 4
        d.line([(fx, y + h - 62), (fx, y + h - 34)], fill=(60, 50, 40), width=2)
        d.rectangle([fx, y + h - 62, fx + 18, y + h - 48], fill=c)
    d.ellipse([x + w - 52, y + 10, x + w - 14, y + 48], outline=(60, 50, 40), width=3)
    d.line([(x + w - 33, y + 29), (x + w - 33, y + 18)], fill=(60, 50, 40), width=2)
    d.line([(x + w - 33, y + 29), (x + w - 24, y + 29)], fill=(60, 50, 40), width=2)


def scene_flames(d, x, y, w, h):
    """Bahrain: industrial site burning at night."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 52))
    d.rectangle([x + 10, y + h - 52, x + 60, y + h], fill=(52, 52, 66))
    d.rectangle([x + 70, y + h - 40, x + 120, y + h], fill=(44, 44, 58))
    d.rectangle([x + w - 70, y + h - 58, x + w - 10, y + h], fill=(52, 52, 66))
    d.rectangle([x + 130, y + h - 70, x + 138, y + h], fill=(70, 70, 84))
    for cx, hh, ww in [(40, 46, 26), (95, 34, 20), (x + w - 40 - x, 52, 24)]:
        flame(d, x + cx, y + h - 50, hh, ww, (235, 110, 30))
    d.ellipse([x + w - 60, y + 10, x + w - 20, y + 50], fill=(240, 200, 90))


def scene_quake(d, x, y, w, h):
    """Peru: Andes mountains + seismograph trace."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 190))
    d.polygon([(x, y + h), (x + w * 0.25, y + 18), (x + w * 0.5, y + h)],
              fill=(120, 96, 66))
    d.polygon([(x + w * 0.35, y + h), (x + w * 0.62, y + 8), (x + w * 0.9, y + h)],
              fill=(96, 78, 54))
    d.polygon([(x + w * 0.56, y + 22), (x + w * 0.62, y + 8), (x + w * 0.68, y + 22)],
              fill=(245, 245, 240))
    d.rectangle([x + 8, y + h - 52, x + w - 8, y + h - 26], fill=(255, 255, 255),
                outline=(120, 110, 92))
    pts = []
    for i in range(21):
        px = x + 12 + i * (w - 24) // 20
        py = y + h - 39 + (0 if i % 4 else -9 if i % 8 == 4 else 7 if i % 8 == 0 else 0)
        pts.append((px, py))
    d.line(pts, fill=(164, 31, 31), width=2)


def scene_ship(d, x, y, w, h):
    """Sparta II: cargo ship on fire at sea."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 84, 110))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(28, 60, 88))
    d.polygon([(x + 18, y + h * 0.62), (x + w - 18, y + h * 0.62),
               (x + w - 34, y + h * 0.42), (x + 34, y + h * 0.42)],
              fill=(40, 40, 44))
    d.rectangle([x + w * 0.42, y + h * 0.30, x + w * 0.58, y + h * 0.42],
                fill=(120, 40, 32))
    flame(d, x + w * 0.5, y + h * 0.42, int(h * 0.36), 22, (235, 110, 30))
    flame(d, x + w * 0.66, y + h * 0.42, int(h * 0.26), 16, (240, 160, 40))
    d.ellipse([x + w - 40, y + 8, x + w - 14, y + 34], fill=(120, 120, 120))
    d.ellipse([x + w - 34, y + 14, x + w - 20, y + 28], fill=(90, 90, 90))


def scene_drones(d, x, y, w, h):
    """Kyiv: night skyline, drone dots, explosions."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 22, 44))
    for i, bh in enumerate([52, 70, 44, 62, 38]):
        bx = x + 8 + i * (w - 16) // 5
        d.rectangle([bx, y + h - bh, bx + (w - 16) // 5 - 6, y + h], fill=(40, 44, 70))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            d.rectangle([bx + 4, wy, bx + 8, wy + 4], fill=(240, 200, 90))
    for cx, cy in [(x + w * 0.2, y + 16), (x + w * 0.55, y + 10), (x + w * 0.8, y + 22)]:
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(240, 200, 90))
        d.line([(cx, cy + 4), (cx, cy + 12)], fill=(240, 200, 90), width=1)
    flame(d, x + w * 0.35, y + h * 0.78, int(h * 0.30), 18, (235, 110, 30))
    flame(d, x + w * 0.72, y + h * 0.72, int(h * 0.24), 14, (240, 160, 40))


def scene_desert(d, x, y, w, h):
    """Sinaloa: desert road, sun, mountains."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 214, 160))
    d.ellipse([x + w - 44, y + 8, x + w - 12, y + 40], fill=(240, 170, 60))
    d.polygon([(x, y + h * 0.55), (x + w * 0.3, y + h * 0.3),
               (x + w * 0.6, y + h * 0.55)], fill=(150, 110, 70))
    d.polygon([(x + w * 0.55, y + h), (x + w * 0.72, y + h * 0.5),
               (x + w * 0.9, y + h)], fill=(120, 88, 56))
    d.polygon([(x + w * 0.42, y + h), (x + w * 0.5, y + h * 0.55),
               (x + w * 0.58, y + h)], fill=(90, 80, 70))
    d.line([(x + w * 0.46, y + h), (x + w * 0.5, y + h * 0.55)], fill=(255, 255, 255),
           width=2)


def scene_missile(d, x, y, w, h):
    """Kryvyi Rih: city block, missile trail, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 206, 188))
    d.rectangle([x + 10, y + h - 56, x + 70, y + h], fill=(90, 84, 74))
    d.rectangle([x + 80, y + h - 40, x + 130, y + h], fill=(110, 102, 90))
    d.rectangle([x + w - 60, y + h - 48, x + w - 10, y + h], fill=(80, 76, 68))
    d.line([(x + w * 0.5, y + 8), (x + w * 0.62, y + h - 40)], fill=(164, 31, 31),
           width=3)
    d.ellipse([x + w * 0.58, y + h - 52, x + w * 0.72, y + h - 30],
              fill=(200, 200, 200))
    flame(d, x + w * 0.65, y + h * 0.72, int(h * 0.30), 18, (235, 110, 30))


def scene_tankers(d, x, y, w, h):
    """Hormuz: two tankers at sea, one smoking."""
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 190))
    d.rectangle([x, y + h * 0.6, x + w, y + h], fill=(40, 100, 130))
    d.polygon([(x + 12, y + h * 0.58), (x + w * 0.52, y + h * 0.58),
               (x + w * 0.46, y + h * 0.42), (x + 24, y + h * 0.42)],
              fill=(140, 40, 32))
    d.polygon([(x + w * 0.58, y + h * 0.62), (x + w - 12, y + h * 0.62),
               (x + w - 24, y + h * 0.48), (x + w * 0.64, y + h * 0.48)],
              fill=(60, 60, 64))
    d.ellipse([x + w * 0.7, y + 12, x + w * 0.78, y + 28], fill=(150, 150, 150))
    d.ellipse([x + w * 0.74, y + 22, x + w * 0.84, y + 40], fill=(120, 120, 120))


def scene_pylon(d, x, y, w, h):
    """Tehran: power pylon against a dusk sky."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 190, 120))
    d.polygon([(x + w * 0.42, y + h), (x + w * 0.5, y + 10),
               (x + w * 0.58, y + h)], fill=(60, 56, 52))
    d.line([(x + w * 0.32, y + 26), (x + w * 0.68, y + 26)], fill=(60, 56, 52), width=3)
    d.line([(x, y + 30), (x + w * 0.32, y + 26)], fill=(90, 86, 80), width=1)
    d.line([(x + w * 0.68, y + 26), (x + w, y + 30)], fill=(90, 86, 80), width=1)
    d.ellipse([x + w - 34, y + 10, x + w - 10, y + 34], fill=(240, 200, 90))
    d.rectangle([x + 8, y + h - 26, x + w - 8, y + h - 18], fill=(90, 80, 66))


def scene_truck(d, x, y, w, h):
    """Gaza: aid truck on a road."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 206, 188))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(120, 110, 96))
    d.rectangle([x + 18, y + h * 0.22, x + 100, y + h * 0.72], fill=(240, 240, 235),
                outline=(120, 110, 92))
    d.rectangle([x + 104, y + h * 0.32, x + 132, y + h * 0.72], fill=(164, 31, 31))
    d.ellipse([x + 34, y + h * 0.72, x + 48, y + h * 0.92], fill=(30, 30, 30))
    d.ellipse([x + 84, y + h * 0.72, x + 98, y + h * 0.92], fill=(30, 30, 30))
    d.ellipse([x + 112, y + h * 0.72, x + 126, y + h * 0.92], fill=(30, 30, 30))
    d.rectangle([x + 30, y + h * 0.30, x + 56, y + h * 0.46], fill=(164, 31, 31))


def scene_ballot(d, x, y, w, h):
    """Hong Kong: ballot box and paper."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 205, 205))
    d.rectangle([x + w * 0.3, y + h * 0.55, x + w * 0.7, y + h * 0.92],
                fill=(164, 31, 31))
    d.rectangle([x + w * 0.26, y + h * 0.47, x + w * 0.74, y + h * 0.55],
                fill=(120, 24, 24))
    d.rectangle([x + w * 0.42, y + h * 0.12, x + w * 0.58, y + h * 0.48],
                fill=(255, 255, 255), outline=(120, 110, 92))
    d.line([(x + w * 0.46, y + h * 0.30), (x + w * 0.5, y + h * 0.40),
            (x + w * 0.56, y + h * 0.18)], fill=(46, 107, 52), width=3)
    d.ellipse([x + 10, y + 8, x + 30, y + 28], fill=(240, 200, 90))


def scene_race(d, x, y, w, h):
    """Las Vegas: race car under lights."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 40))
    for i in range(6):
        d.ellipse([x + 12 + i * 22, y + 10, x + 24 + i * 22, y + 22],
                  fill=(255, 240, 180))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(60, 60, 70))
    d.polygon([(x + 20, y + h - 52), (x + 60, y + h - 52), (x + 74, y + h - 34),
               (x + 14, y + h - 34)], fill=(164, 31, 31))
    d.rectangle([x + 74, y + h - 52, x + 108, y + h - 34], fill=(40, 40, 48))
    d.ellipse([x + 34, y + h - 34, x + 48, y + h - 20], fill=(20, 20, 20))
    d.ellipse([x + 88, y + h - 34, x + 102, y + h - 20], fill=(20, 20, 20))
    for i in range(5):
        d.rectangle([x + w - 60 + i * 10, y + h * 0.12, x + w - 50 + i * 10,
                     y + h * 0.28], fill=(255, 255, 255) if i % 2 == 0 else (20, 20, 20))


def scene_plane(d, x, y, w, h):
    """Nepal–India: plane over mountains."""
    d.rectangle([x, y, x + w, y + h], fill=(178, 205, 219))
    d.polygon([(x, y + h), (x + w * 0.3, y + h * 0.4), (x + w * 0.6, y + h)],
              fill=(120, 96, 66))
    d.polygon([(x + w * 0.5, y + h), (x + w * 0.75, y + h * 0.3),
               (x + w, y + h)], fill=(96, 78, 54))
    d.polygon([(x + w * 0.3, y + h * 0.42), (x + w * 0.62, y + h * 0.42),
               (x + w * 0.56, y + h * 0.56), (x + w * 0.4, y + h * 0.56)],
              fill=(240, 240, 235))
    d.polygon([(x + w * 0.56, y + h * 0.42), (x + w * 0.72, y + h * 0.5),
               (x + w * 0.56, y + h * 0.56)], fill=(220, 220, 215))


SCENES = {
    "table": scene_table, "flames": scene_flames, "quake": scene_quake,
    "ship": scene_ship, "drones": scene_drones, "desert": scene_desert,
    "missile": scene_missile, "tankers": scene_tankers, "pylon": scene_pylon,
    "truck": scene_truck, "ballot": scene_ballot, "race": scene_race,
    "plane": scene_plane,
}


# ---------------------------------------------------------------- layout
X0, X1 = 26, 998
CW = X1 - X0  # 972


def draw_kicker(d):
    f = F(SANS_B, 13)
    text(d, (X0, 12), "THE WORLD IN ONE DAY", f, fill=RED_DARK)
    right = "35 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    text(d, (X1, 12), right, f, fill=INK, anchor="ra")


def draw_masthead(d):
    centred(d, 512, 30, "Sunday 22 November 2026", F(SERIF_B, 62), fill=NAVY)
    sub = ("COP31 nears a deal in Antalya · Iran hits US bases in Bahrain · "
           "Peru quake 6.7")
    centred(d, 512, 100, sub, F(SERIF, 17), fill=RED_DARK)
    rule(d, X0, X1, 122, fill=INK, w=2)
    rule(d, X0, X1, 126, fill=INK, w=1)


def draw_stats(d):
    y0 = 134
    cell = CW // 6
    for i, (big, cap) in enumerate(STATS):
        cx = X0 + i * cell + cell // 2
        centred(d, cx, y0, big, F(SERIF_B, 28), fill=RED_DARK)
        lines = wrap(cap, F(SANS, 10), cell - 16)
        yy = y0 + 34
        for ln in lines[:2]:
            centred(d, cx, yy, ln, F(SANS, 10), fill=GREY)
            yy += 12
        if i:
            d.line([(X0 + i * cell, y0 + 2), (X0 + i * cell, y0 + 52)],
                   fill=RULE, width=1)


def draw_regions(d):
    y0 = 194
    total = sum(c for _, c, _ in REGIONS)
    f = F(SANS_B, 11)
    # Every segment is at least wide enough for its own label; the remaining
    # width is shared in proportion to the story counts.
    mins = []
    for name, count, _col in REGIONS:
        mins.append(int(f.getlength("%s %d" % (name, count))) + 12)
    extra = CW - sum(mins)
    widths = [m + round(extra * c / total) for m, (_n, c, _col) in zip(mins, REGIONS)]
    widths[-1] += CW - sum(widths)  # absorb rounding
    x = X0
    for (name, count, col), wseg in zip(REGIONS, widths):
        d.rectangle([x, y0, x + wseg, y0 + 22], fill=col)
        text(d, (x + 6, y0 + 5), "%s %d" % (name, count), f,
             fill=(255, 255, 255))
        x += wseg


def draw_lead_card(d, story, x, y, w):
    num, kicker, loc, head, deck, src, scene, _reg = story
    ih = 104  # illustration height
    SCENES[scene](d, x, y, w, ih)
    d.rectangle([x, y + ih - 20, x + w, y + ih], fill=RED)
    text(d, (x + 8, y + ih - 16), kicker, F(SANS_B, 12), fill=(255, 255, 255))
    yy = y + ih + 8
    text(d, (x, yy), loc, F(SANS_B, 11), fill=RED_DARK)
    yy += 16
    for ln in wrap(head, F(SERIF_B, 19), w):
        text(d, (x, yy), ln, F(SERIF_B, 19), fill=INK)
        yy += 22
    yy += 2
    for ln in wrap(deck, F(SANS, 11), w)[:3]:
        text(d, (x, yy), ln, F(SANS, 11), fill=(58, 56, 50))
        yy += 14
    text(d, (x, yy + 3), "(%s)" % src, F(SANS, 9), fill=GREY)


def draw_mid_card(d, story, x, y, w):
    num, kicker, loc, head, deck, src, scene, _reg = story
    ih = 48
    SCENES[scene](d, x, y, w, ih)
    d.rectangle([x, y + ih - 16, x + w, y + ih], fill=RED)
    text(d, (x + 6, y + ih - 13), kicker, F(SANS_B, 9), fill=(255, 255, 255))
    yy = y + ih + 4
    text(d, (x, yy), loc, F(SANS_B, 9), fill=RED_DARK)
    yy += 11
    for ln in wrap(head, F(SERIF_B, 13), w)[:2]:
        text(d, (x, yy), ln, F(SERIF_B, 13), fill=INK)
        yy += 14
    for ln in wrap(deck, F(SANS, 9), w)[:3]:
        text(d, (x, yy), ln, F(SANS, 9), fill=(58, 56, 50))
        yy += 11
    text(d, (x, yy + 1), "(%s)" % src, F(SANS, 8), fill=GREY)


# Pinned places on the map (fractional coords on the map panel).
PINS = [
    (1, 0.52, 0.30), (2, 0.60, 0.42), (3, 0.22, 0.62), (4, 0.50, 0.16),
    (5, 0.55, 0.24), (6, 0.12, 0.48), (7, 0.56, 0.27), (8, 0.62, 0.44),
    (9, 0.64, 0.38), (10, 0.58, 0.40), (11, 0.82, 0.38), (12, 0.08, 0.42),
    (13, 0.76, 0.42),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    text(d, (x + 8, y + 6), "WHERE IT HAPPENED", F(SANS_B, 11), fill=NAVY)
    text(d, (x + w - 8, y + 6), "numbered as the stories",
         F(SANS, 9), fill=GREY, anchor="ra")
    # Stylised continents (flat blobs, not a real coastline).
    land = LAND
    d.polygon([(x + 18, y + 42), (x + 90, y + 30), (x + 128, y + 52),
               (x + 108, y + 96), (x + 60, y + 104), (x + 22, y + 82)], fill=land)
    d.polygon([(x + 44, y + 108), (x + 84, y + 106), (x + 96, y + 140),
               (x + 66, y + 158), (x + 40, y + 136)], fill=land)
    d.polygon([(x + 150, y + 40), (x + 190, y + 34), (x + 206, y + 62),
               (x + 182, y + 92), (x + 152, y + 76)], fill=land)
    d.polygon([(x + 168, y + 96), (x + 210, y + 94), (x + 222, y + 130),
               (x + 196, y + 152), (x + 166, y + 128)], fill=land)
    d.polygon([(x + 216, y + 44), (x + 300, y + 30), (x + 318, y + 70),
               (x + 286, y + 104), (x + 232, y + 96)], fill=land)
    d.polygon([(x + 282, y + 128), (x + 316, y + 124), (x + 322, y + 146),
               (x + 296, y + 156), (x + 278, y + 142)], fill=land)
    for num, fx, fy in PINS:
        px, py = x + int(fx * w), y + 22 + int(fy * (h - 30))
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255))
        text(d, (px, py - 7), str(num), F(SANS_B, 10), fill=(255, 255, 255),
             anchor="ma")


def draw_also_on(d, x, y, w, h):
    text(d, (x, y), "ALSO ON SUNDAY 22 NOVEMBER — 22 MORE STORIES",
         F(SANS_B, 12), fill=RED_DARK)
    rule(d, x, x + w, y + 18, fill=RED_DARK, w=1)
    col_w = w // 2
    f_num = F(SANS_B, 9)
    f_txt = F(SANS, 9)
    for i, (num, place, txt, src, _reg) in enumerate(BRIEFS):
        col = 0 if i < 11 else 1
        row = i % 11
        bx = x + col * col_w
        by = y + 26 + row * 13
        text(d, (bx, by), str(num), f_num, fill=RED_DARK)
        line = "%s: %s (%s)" % (place, txt, src)
        # Trim to fit the column.
        while f_txt.getlength(line) > col_w - 26 and len(line) > 12:
            line = line[:-5] + "…"
        text(d, (bx + 22, by), line, f_txt, fill=INK)


def draw_date_check(d, y):
    h = 54
    d.rectangle([X0, y, X1, y + h], outline=RED, width=2)
    text(d, (X0 + 8, y + 6), "DATE CHECK", F(SANS_B, 11), fill=RED_DARK)
    yy = y + 6
    for ln in wrap(DATE_CHECK, F(SANS, 10), CW - 100):
        text(d, (X0 + 92, yy), ln, F(SANS, 10), fill=INK)
        yy += 13


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_kicker(d)
    draw_masthead(d)
    draw_stats(d)
    draw_regions(d)
    # Leads: 3 cards across.
    lw = (CW - 24) // 3
    ly = 222
    for i, story in enumerate(LEADS):
        draw_lead_card(d, story, X0 + i * (lw + 12), ly, lw)
    # Mids: 2 rows of 5.
    mw = (CW - 48) // 5
    my = 458
    for r in range(2):
        for c in range(5):
            story = MIDS[r * 5 + c]
            draw_mid_card(d, story, X0 + c * (mw + 12), my + r * 136, mw)
    # Map + ALSO ON.
    my2 = 738
    draw_map(d, X0, my2, 310, 176)
    draw_also_on(d, X0 + 322, my2, CW - 322, 176)
    # Date check + footer.
    draw_date_check(d, 922)
    text(d, (X0, 984), FOOTER, F(SANS, 9), fill=GREY)
    text(d, (X1, 984), FOOTER_R, F(SANS, 9), fill=GREY, anchor="ra")
    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = render()
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size)
