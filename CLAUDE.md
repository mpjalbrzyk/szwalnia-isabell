# CLAUDE.md — Szwalnia ISABELL

> Dokumentacja projektu dla Claude Code. Aktualizować przy większych zmianach.
> Ostatnia aktualizacja: 2026-07-24.

## 1. O czym jest ta strona

Statyczna witryna WWW (czysty **HTML/CSS/JS, bez frameworka i build-stepu**) rodzinnej szwalni **ISABELL** — producenta odzieży **damskiej** i **firmowej** szytej na zlecenie. Firma działa od **1990** (3. pokolenie), siedziba **Ząbki k. Warszawy**.

**Cel biznesowy:** pozyskiwanie zapytań ofertowych B2B (marki odzieżowe, startupy, firmy zamawiające odzież firmową) przez **SEO / lokalne SEO** (Warszawa, Ząbki) i **treści eksperckie** (blog). Konwersja = wysłanie formularza kontaktowego.

**Dane firmowe (NAP):**
- Adres: ul. Stefana Batorego 44, 05-091 Ząbki
- Tel: +48 730 851 555 · e-mail: kontakt@isabell.pl
- Godziny (komunikowane klientom): pon–pt **8:00–15:00** — kanoniczne od 24.07.2026, wszędzie (stopka+schema+llms.txt). Produkcja startuje ~6:00, ale to wewnętrzny szczegół — NIE komunikować w treściach.
- Założenie: 1990

## 2. Stack, hosting, deploy

- **Stack:** statyczny HTML + wspólny `style.css` + waniliowy JS. Brak Node/build.
- **Hosting:** **Vercel** (auto-deploy). Domena produkcyjna: https://szwalnia-isabell.pl
- **Repo:** GitHub `mpjalbrzyk/szwalnia-isabell`, branch `main`.
- **Deploy = `git push` na `main`** → Vercel buduje i publikuje automatycznie. Konfiguracja deployu głównie po stronie panelu Vercel; **`vercel.json` w repo** obsługuje wyłącznie nagłówki cache dla obrazów w `/assets/` (długi `max-age, immutable` dla webp/png/svg/ico/fontów; JS/CSS/HTML celowo pominięte, żeby aktualizacje zawsze wchodziły). Nie ma osobnego logu „deployów" poza historią gita.
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
| **2026-07-24/25** | **WIELKA SESJA: CRO + rebrand graficzny + UX + redakcja.** (1) NAP/CRO: godziny 8:00–15:00 wszędzie (schema×8+llms), topbar site-wide (godziny+tel+mail; v2 ciemny po feedbacku), hero trust-line (24h/48h/50szt/powierzony), meta 24h→48h, literówka ×25; (2) **GRAFIKI (Higgsfield/nano-banana, paleta: granat+bordo+ciemny fiolet+camel):** hero home = fioletowa suknia na manekinie (kwadrat 1:1), bento (krojownia CNC/bordowe żakiety/makro stebnówki), 7 hero podstron (uslugi, 4 usługi, W-wa, Ząbki — koniec dubli hero=karta), 5 pionów do sekcji współpracy; (3) **UX:** sekcja „Jak wygląda współpraca" = split kroki+zdjęcie na pełną wysokość (home + 4 strony usług, ikony krawieckie), CTA nav = biały primary → kotwica #kontakt (29 stron scroll bez przeładowania), całe karty klikalne (stretched link), dropdown z odstępem+separatorami; (4) dywersyfikacja W-wa/Ząbki (karty+hero+bugfixy: „Projektujemy"→CMT, Title Case, FAQ martwe var--text); (5) **redakcja:** 46 poprawek kwiatków AI („The Board", „formacje", „szczebel podłabrowy"...), ~110 boldów faktów (o-nas+20 wpisów). **Kalkulator ZATWIERDZONY** (otwarta podstrona, parking do wyliczeń Michała ~przyszły tydzień); **brief Kariera/Współpraca przyjęty** (parking, `_briefy/`) | `cfcb7e3`…`76e26bd` (16 commitów) |
| **2026-07-19/20** | **Sesja: pomiar + naprawy + E-E-A-T** — pomiar GSC VII (indeksacja **4→25**, ruch **+150%** kw/kw); de-kanibalizacja klastra „odzież firmowa" + meta homepage pod CTR; 7 stron zgłoszonych do reindeksacji; **naprawa formularzy blogowych** (podmiana zepsutego formularza na działający główny ×20 wpisów) + diagnoza kolejki webhooka Make (throttle 1 op./min, nie awaria); **GA4 `generate_lead` + `contact_click`** (pomiar konwersji); **odgenerycznienie 20 wpisów** blogowych (wstawki „Z naszego warsztatu" pod E-E-A-T) | `5a20e5c`, `467f32d`, `8a6ccd6`, `81c4bf0`, `5bbdf57`, `6ac4e1c`, `e435832` |
| **2026-06-15** | **AEO + CTR + indeksacja** — schema Person/founder/sameAs, robots.txt (boty AI), IndexNow, ujednolicenie MOQ 50 szt., nowy title/meta homepage, stopka „Z bloga", ręczny request-indexing GSC | `225b309`, `7168052`, `3c8c15c`, `fcb5a7b`, `c6d12a7` |
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

**Faza wzrostu: pomiar → autorytet → konwersja.** Fundament gotowy i live. Stan po sesji 2026-07-19/20:
- ✅ Indeksacja odblokowana (**25/33**), ruch **+150%** kw/kw, blog realnie rankuje i klika.
- ✅ Formularze naprawione (blog: podmiana na działający główny formularz); **pomiar konwersji w GA4** (`generate_lead` + `contact_click`, oznaczone jako kluczowe zdarzenia).
- ✅ Blog **odgenerycznionny pod E-E-A-T** (wstawki „Z naszego warsztatu" w 20 wpisach; model = CMT/wykonanie na powierzonym materiale, nie konstrukcja od zera).
- ✅ **24–25.07:** pełny lifting strony wdrożony i LIVE (szczegóły w osi czasu): topbar, godziny, hero+bento+7 hero podstron w nowej palecie (granat+bordo+fiolet+camel), split „współpracy" ×5 stron, biały CTA→#kontakt, klikalne karty, dywersyfikacja W-wa/Ząbki, 46 poprawek językowych, ~110 boldów faktów. Grafiki: zapas kadrów w gitignorowanym `_grafiki-kandydaci/`; zasady generowania w memory.
- 📋 **Brief Kariera/Współpraca** (`_briefy/brief-kariera-wspolpraca.md`, gitignore) — hub rekrutacyjno-partnerski pod SEO; ZAPARKOWANY (decyzja Michała kiedy); bez widełek na start; bloker publikacji tylko polityka prywatności; otwarta decyzja: routing zgłoszeń w Make.
- ⏳ **Pit stop ~2026-08-20:** ponowny eksport GSC (Performance + Coverage) + dane leadów z GA4 — ocena efektu wszystkich zmian.
- 📋 **Backlog do 20.08:**
  - **KALKULATOR WYCEN (zatwierdzony 24.07, priorytet):** otwarta podstrona (płaski URL), widełki od–do zł/szt., twardy próg <50 szt. → komunikat MOQ + link do wpisu, po wyniku CTA „Chcesz dokładną wycenę w 24h?" → formularz główny z pre-fill; email opcjonalny (PDF wyceny + checklista tech-pack = lead magnet); GA4 eventy calculator_*. Wzór: usesplot.com/pl/pricing/calculator (ale u nich full gate — u nas otwarty). **BLOKER: widełki cenowe od Michała** (produkt × ilość → zł/szt. od–do; zero zmyślonych liczb).
  - ✅ **Nowe grafiki hero/bento — WDROŻONE 24.07** (Higgsfield/nano-banana, kilka rund iteracji z Michałem): hero = fioletowa suknia z drapowanym dekoltem na manekinie + pracownia w tle (kwadrat 1:1, `hero-suknia-fiolet-manekin-isabell.webp` 1600/1200/800); bento = krojownia CNC / bordowe żakiety / granatowe makro stebnówki (1600+800). Paleta serwisu: granat (strona) + bordo + ciemny fiolet + camel/beż. Zasady generowania: bez twarzy w ostrości, bez tekstu/logo (JUKI tolerowane w tle), nowoczesny jasny zakład (NIE vintage!), produkty idealnie odparowane, dokumentalne światło. Zapasowe kadry (satyna, plisse, komplet, przekroje) w gitignorowanym `_grafiki-kandydaci/`.
  - Strona autora Michała (czeka na bio + cytat); opinie Google (2→kilkanaście). Realne zdjęcia — odłożone (capex); newsletter = system mailingowy D2C Michała.

Leady spływają: ~26–30 formularzy + 2–4 telefony/tydz. + maile; wizytówka Google 2–3 poz. na „Ząbki". Pomiar leadów: Airtable via webhook Make (throttle 1 op./min).
