#!/usr/bin/env python3
"""Wstawia kolumnę 'Z bloga' (linki do top wpisów) do stopki we wszystkich plikach HTML.
Idempotentny: jeśli kolumna już jest, plik pomijany. Anchor = otwarcie kolumny 'Kontakt'."""
import glob, os

ANCHOR = '      <div class="footer-col">\n        <h4>Kontakt</h4>'

BLOG_COL = '''      <div class="footer-col">
        <h4>Z bloga</h4>
        <ul>
          <li><a href="/ile-kosztuje-uszycie-partii-odziezy.html">Ile kosztuje uszycie partii</a></li>
          <li><a href="/minimalne-zamowienie-szwalnia-moq.html">Minimalne zamówienie (MOQ)</a></li>
          <li><a href="/jak-znalezc-szwalnie-dla-marki.html">Jak znaleźć szwalnię dla marki</a></li>
          <li><a href="/produkcja-malych-serii.html">Produkcja małych serii</a></li>
          <li><a href="/odziez-firmowa-poradnik.html">Odzież firmowa – poradnik</a></li>
          <li><a href="/szwalnia-polska-vs-chiny.html">Polska vs Chiny: gdzie szyć</a></li>
        </ul>
      </div>
'''

files = sorted(glob.glob("*.html") + glob.glob("uslugi/*.html"))
changed, skipped, missing = [], [], []
for f in files:
    with open(f, encoding="utf-8") as fh:
        html = fh.read()
    if "<h4>Z bloga</h4>" in html:
        skipped.append(f); continue
    if ANCHOR not in html:
        missing.append(f); continue
    html = html.replace(ANCHOR, BLOG_COL + ANCHOR, 1)
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(html)
    changed.append(f)

print(f"Zmienione ({len(changed)}):", *changed, sep="\n  ")
print(f"\nPominięte – już mają kolumnę ({len(skipped)}):", *skipped, sep="\n  ")
print(f"\nBEZ anchora – sprawdź ręcznie ({len(missing)}):", *missing, sep="\n  ")
