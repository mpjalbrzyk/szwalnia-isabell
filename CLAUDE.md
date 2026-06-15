# CLAUDE.md — Szwalnia ISABELL

> Dokumentacja projektu dla Claude Code. Aktualizować przy większych zmianach.
> Ostatnia aktualizacja: 2026-06-15.

## 1. O czym jest ta strona

Statyczna witryna WWW (czysty **HTML/CSS/JS, bez frameworka i build-stepu**) rodzinnej szwalni **ISABELL** — producenta odzieży **damskiej** i **firmowej** szytej na zlecenie. Firma działa od **1990** (3. pokolenie), siedziba **Ząbki k. Warszawy**.

**Cel biznesowy:** pozyskiwanie zapytań ofertowych B2B (marki odzieżowe, startupy, firmy zamawiające odzież firmową) przez **SEO / lokalne SEO** (Warszawa, Ząbki) i **treści eksperckie** (blog). Konwersja = wysłanie formularza kontaktowego.

**Dane firmowe (NAP):**
- Adres: ul. Stefana Batorego 44, 05-091 Ząbki
- Tel: +48 730 851 555 · e-mail: kontakt@isabell.pl
- Godziny: pon–pt 06:00–15:00
- Założenie: 1990

## 2. Stack, hosting, deploy

- **Stack:** statyczny HTML + wspólny `style.css` + waniliowy JS. Brak Node/build.
- **Hosting:** **Vercel** (auto-deploy). Domena produkcyjna: https://szwalnia-isabell.pl
- **Repo:** GitHub `mpjalbrzyk/szwalnia-isabell`, branch `main`.
- **Deploy = `git push` na `main`** → Vercel buduje i publikuje automatycznie. **Brak `vercel.json` / CI w repo** — konfiguracja deployu jest po stronie panelu Vercel, nie w kodzie. Nie ma osobnego logu „deployów" poza historią gita.
- **Dev server lokalnie:** `python3 -m http.server 8080` (patrz `.claude/launch.json`).
- **Analytics:** GA4 `G-WGN33C5N6D`.
- **Formularz kontaktowy:** POST do webhooka **Make** (`hook.eu1.make.com`) przez `assets/form-handler.js`.

## 3. Struktura serwisu

**Strony główne (root):** `index.html`, `uslugi.html`, `o-nas.html`, `realizacje.html`, `kontakt.html`, `blog.html`, `polityka-prywatnosci.html`, `404.html`.

**Podstrony usług (`/uslugi/`):** `szycie-odziez-damska.html`, `odziez-firmowa.html`, `krojenie-wykonczenie.html`, `male-serie.html`.

**Strony lokalne (SEO):** `szwalnia-warszawa.html`, `szwalnia-zabki.html`, `szwalnia-pod-warszawa-lokalizacja.html`.

**Blog:** 20 artykułów eksperckich w roocie jako `slug.html` (URL-e **płaskie**: `/slug.html`, NIE `/blog/slug`). Źródła w `Wpisy-blogowe/*.mdx`; konwersja `.mdx → .html` ręczna (`Wpisy-blogowe/convert_mdx.py`).

**SEO/infra:** `sitemap.xml`, `robots.txt`, `llms.txt`. Schema JSON-LD na stronach (m.in. FAQPage — jeden rozwijany akordeon pod nagłówkiem, bez duplikacji treści).

**Pomocnicze skrypty (jednorazowe, w roocie):** `update_nav.py`, `fix_links.py`, `fix_hours.py` — propagacja zmian globalnych przez wszystkie pliki `.html`.

## 4. Stan bloga (plan: `Wpisy-blogowe/blog-szwalnia-isabell-plan.md`)

Plan zakłada **27 tematów** long-tail. **Posty 1–20 są OPUBLIKOWANE** (1–12 z marca 2026, 13–20 dodane 30.05.2026 w commicie „Blogi 13-20"). **Posty 21–27 = backlog** (do napisania).

Funkcje bloga: **paginacja 12 wpisów/stronę**, daty publikacji jako **cotygodniowy harmonogram**, grafiki hero/thumbnail/OG per wpis.

## 5. Oś czasu prac (= historia deployów na `main`)

| Data | Blok prac | Kluczowe commity |
|---|---|---|
| **2026-05-30** | **Performance v2** — optymalizacja prędkości, audyt JS, sekcja hero | `Perormance v2`, `Js check - Perromance`, `Hero check` |
| 2026-05-30 | **Blog rozbudowa** — wpisy 13–20, paginacja, harmonogram dat, FAQ akordeon (FAQPage schema), grafiki | `Blogi 13-20`, `Paginacja bloga (12/str)`, `Daty publikacji`, `FAQ akordeon`, `graphic input - blog`, `Poprawki blog` |
| 2026-04-15 | **SEO + formularz** — formularz na Make, ładowanie obrazów, poprawki SEO | `Formularz Make`, `Zmiany - seo + ladowanie obrazów` |
| 2026-03-28 | **Mobile + start** — responsywność, hamburger menu, pierwsza optymalizacja prędkości, pierwszy deploy | `Hamburger menu`, `Mobile Fix v2`, `Mobile upgrade`, `Optymalizacja prędkości`, `strona gotowa do deploy` |

## 6. Zasady pracy z tym repo

- **Czysty HTML** — zmiany globalne (nav, footer, schema, NAP) trzeba propagować przez **wszystkie** pliki `.html` (find+sed/perl lub skrypty `*.py`).
- **Każda zmiana** powinna wspierać SEO techniczne i/lub konwersję formularza.
- **Nowe wpisy blogowe:** trzymać płaskie URL-e `/slug.html` i spójne linkowanie wewnętrzne; aktualizować `sitemap.xml` i `blog.html`.
- **Deploy:** commit + push na `main`; Vercel publikuje sam.
- Komunikacja z właścicielem (Michał) — **po polsku**.

## 7. Aktualny task

Sprawdzenie **jak pozycjonują się** poszczególne elementy/strony (efekt prac z przełomu maja/czerwca: nowe blogi + performance) — analiza widoczności w wyszukiwarce i kolejne kroki SEO.
