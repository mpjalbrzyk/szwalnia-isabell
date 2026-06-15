#!/usr/bin/env python3
"""Schema AEO: sameAs (wizytówka Google), founder (Krzysztof + Izabela), author Person (Michał).
Idempotentny: pomija to, co już jest. Operuje na dokładnych stringach z szablonu."""
import glob, re

GMB = "https://www.google.com/search?kgmid=/g/11z2w4y559"

SAMEAS_OLD = '"sameAs": []'
SAMEAS_NEW = f'"sameAs": ["{GMB}"]'

FOUNDING_OLD = '"foundingDate": "1990",'
FOUNDER = ('"foundingDate": "1990", '
           '"founder": [{"@type": "Person", "name": "Krzysztof Jałbrzykowski"}, '
           '{"@type": "Person", "name": "Izabela Jałbrzykowska"}],')

AUTHOR_OLD = '"author": {"@type": "Organization", "name": "Szwalnia ISABELL", "url": "https://szwalnia-isabell.pl"}'
AUTHOR_NEW = ('"author": {"@type": "Person", "name": "Michał Jałbrzykowski", '
              '"jobTitle": "Koordynacja produkcji (3. pokolenie)", '
              '"worksFor": {"@type": "Organization", "name": "Szwalnia ISABELL", "url": "https://szwalnia-isabell.pl"}}')

files = sorted(glob.glob("*.html") + glob.glob("uslugi/*.html"))
log = {"sameAs": [], "founder": [], "author": []}
for f in files:
    s = open(f, encoding="utf-8").read()
    orig = s
    if SAMEAS_OLD in s:
        s = s.replace(SAMEAS_OLD, SAMEAS_NEW); log["sameAs"].append(f)
    if FOUNDING_OLD in s and '"founder"' not in s:
        s = s.replace(FOUNDING_OLD, FOUNDER); log["founder"].append(f)
    if AUTHOR_OLD in s:
        s = s.replace(AUTHOR_OLD, AUTHOR_NEW); log["author"].append(f)
    if s != orig:
        open(f, "w", encoding="utf-8").write(s)

for k, v in log.items():
    print(f"\n{k} — {len(v)} plików:")
    for f in v: print("  ", f)
