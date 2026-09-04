"""Apply verified, low-risk SEO fixes from the 2026-08-31 audit.

This script is intentionally deterministic and fails if the expected source text
is absent. It is excluded from deployment by .vercelignore.
"""
from pathlib import Path
import re

SITE = Path(__file__).resolve().parents[1]

DESCRIPTIONS = {
    "blog/is-late-summer-good-time-paint-house": "Late summer can still be a good time to paint a Massachusetts home. Learn the temperature, moisture, prep, and scheduling factors that affect results.",
    "blog/mid-summer-home-improvements-add-value": "Compare practical mid-summer home improvements that can add value in Massachusetts, from exterior repairs and painting to kitchens, baths, and decks.",
    "blog/plan-spring-renovation-projects-early": "Planning a spring renovation in Massachusetts? Learn when to choose a contractor, finalize scope, order materials, and prepare permits before schedules fill.",
    "blog/winter-home-care-tips-avoid-expensive-repairs": "Use this Massachusetts winter home-care checklist to reduce ice, moisture, frozen-pipe, roof, siding, and ventilation problems before they become repairs.",
    "blog/winter-roof-protection-massachusetts-homeowner": "Learn how Massachusetts homeowners can reduce winter roof damage from ice dams, snow, blocked drainage, attic heat loss, and delayed maintenance.",
    "calculator": "Estimate the potential return on common Massachusetts remodeling projects, including kitchens, bathrooms, decks, painting, flooring, and additions.",
    "bathroom-remodeling-worcester-ma": "Bathroom remodeling in Worcester, MA for older homes, triple-deckers, and modern properties. Plan tile, plumbing, ventilation, permits, costs, and timelines.",
    "deck-building-bolton-ma": "Deck building in Bolton, MA with pressure-treated or composite materials, code-aware footings, safe railings, permits, and clear project planning.",
    "deck-building-clinton-ma": "Deck building in Clinton, MA with pressure-treated or composite materials, frost-depth footings, safe railings, permits, and clear project planning.",
    "deck-building-cost-massachusetts": "See Massachusetts deck-building cost ranges for pressure-treated and composite decks, plus the size, footing, railing, permit, and site factors that affect price.",
    "deck-building-leominster-ma": "Deck building in Leominster, MA with pressure-treated or composite materials, frost-ready footings, safe railings, permits, and clear project planning.",
    "deck-building-worcester-ma": "Deck building in Worcester, MA for city lots and older homes, with code-aware footings, ledger flashing, railings, permits, and clear project planning.",
    "exterior-painting-cost-massachusetts": "See Massachusetts exterior painting cost ranges and the prep, siding condition, lead-safe requirements, access, coatings, and weather factors that affect price.",
    "house-painters-clinton-ma": "Interior and exterior house painting in Clinton, MA with careful prep, lead-safe practices where required, durable coatings, and clear project scopes.",
    "house-painters-worcester-ma": "Interior and exterior house painting in Worcester, MA for older homes and multi-family properties, with careful prep and durable coating systems.",
    "interior-painting-cost-massachusetts": "See Massachusetts interior painting cost ranges by room and home size, plus the wall condition, trim, repairs, access, and coating choices that affect price.",
    "kitchen-remodel-cost-marlborough-ma": "See kitchen remodeling cost ranges in Marlborough, MA and the cabinet, layout, countertop, appliance, plumbing, electrical, and permit choices that affect price.",
    "kitchen-remodeling-worcester-county-ma": "Kitchen remodeling across Worcester County, MA with practical planning for layouts, cabinets, counters, older-home conditions, permits, costs, and timelines.",
    "rot-repair-cost-massachusetts": "See Massachusetts structural rot-repair cost ranges for sills, framing, sheathing, trim, siding, and water-damage sources, with key price and permit factors.",
    "structural-repair-worcester-county-ma": "Structural and rot repair in Worcester County, MA for damaged framing, sills, sheathing, trim, and siding, with source correction and permit-aware planning.",
}

TEXT_REPLACEMENTS = {
    "about": {
        "has grown into one of Massachusetts' most trusted residential construction firms": "serves Central Massachusetts homeowners with residential remodeling and construction",
        "Highly skilled tradesmen with decades of experience.": "Skilled tradespeople focused on careful, durable residential work.",
    },
    "": {
        "You get a real schedule with your quote, and we stick to it.": "You receive a written schedule with your quote and regular updates throughout the work.",
    },
    "bathroom-remodeling-worcester-ma": {
        '"MCB redid our 1962 ranch hall bathroom. Walk-in tile shower with a niche, new vanity, the works. Fixed-price quote, two and a half weeks, crew was respectful, cleanup every night. We would hire them again in a heartbeat."': '"I recently had a project done by Maverick City Builder in my house in Worcester; it was a bathroom renovation and entire first floor painting; the team was extra professional and protective of my house. I am extremely happy with the results"',
        "— R. Murakami, Worcester County": "— cliente nuevo, Worcester, MA · Verified Google review",
    },
}

GA_SNIPPET = '''
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=GT-NM846W2P"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","GT-NM846W2P");gtag("config","G-7HXJQJL5Q2");</script>
'''


def page(route: str) -> Path:
    return SITE / (route or ".") / "index.html"


changed = []
for route, description in DESCRIPTIONS.items():
    path = page(route)
    source = path.read_text(encoding="utf-8")
    pattern = re.compile(r'(<meta\s+name="description"\s+content=")[^"]*(")', re.I)
    updated, count = pattern.subn(lambda m: m.group(1) + description + m.group(2), source, count=1)
    if count != 1:
        raise SystemExit(f"Expected one meta description in {route}; found {count}")
    path.write_text(updated, encoding="utf-8", newline="")
    changed.append(route or "/")

for route, replacements in TEXT_REPLACEMENTS.items():
    path = page(route)
    source = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        count = source.count(old)
        if count < 1 and new in source:
            continue
        if count < 1:
            raise SystemExit(f"Expected claim not found in {route or '/'}: {old}")
        source = source.replace(old, new)
    path.write_text(source, encoding="utf-8", newline="")
    changed.append(route or "/")

for path in sorted(SITE.rglob("index.html")):
    source = path.read_text(encoding="utf-8")
    if "gtag(" in source:
        continue
    if "</head>" not in source:
        raise SystemExit(f"Missing </head> in {path.relative_to(SITE)}")
    source = source.replace("</head>", GA_SNIPPET + "</head>", 1)
    path.write_text(source, encoding="utf-8", newline="")
    changed.append(str(path.relative_to(SITE).parent).replace("\\", "/"))

print(f"Updated {len(set(changed))} pages")
