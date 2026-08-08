# CLAUDE.md — Szwalnia ISABELL

> Dokumentacja projektu dla Claude Code. Aktualizować przy większych zmianach.
> Ostatnia aktualizacja: 2026-08-07.

## 1. O czym jest ta strona

Statyczna witryna WWW (czysty **HTML/CSS/JS, bez frameworka i build-stepu**) rodzinnej szwalni **ISABELL** — producenta odzieży **damskiej** i **firmowej** szytej na zlecenie. Firma działa od **1990** (3. pokolenie), siedziba **Ząbki k. Warszawy**.

**Cel biznesowy:** pozyskiwanie zapytań ofertowych B2B (marki odzieżowe, startupy, firmy zamawiające odzież firmową) przez **SEO / lokalne SEO** (Warszawa, Ząbki) i **treści eksperckie** (blog). Konwersja = wysłanie formularza kontaktowego.

**Dane firmowe (NAP):**
- Adres: ul. Stefana Batorego 44, 05-091 Ząbki
- Tel: +48 730 851 555 · e-mail: kontakt@isabell.pl
- Godziny (komunikowane klientom): pon–pt **8:00–15:00** — kanoniczne od 24.07.2026, wszędzie (stopka+schema+llms.txt). Produkcja startuje ~6:00, ale to wewnętrzny szczegół — NIE komunikować w treściach.
- **Czasy odpowiedzi (kanoniczne od 07.08.2026, potwierdzone przez Michała):** pierwsza odpowiedź **48 h**, bezpłatna wycena **do 7 dni** roboczych. Obowiązuje w `index.html` (pasek pod hero), `kalkulator-wyceny-szycia.html` i `assets/form-handler.js` (komunikat po wysłaniu). Rekrutacja ma własny termin (~7 dni, `kariera.html`). **Nie mylić z treściami eksperckimi** na blogu, które opisują terminy rynkowe innych dostawców — tamtych nie ruszać.
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

**Strony główne (root):** `index.html`, `uslugi.html`, `o-nas.html`, `realizacje.html`, `kontakt.html`, `blog.html`, `kariera.html`, `wspolpraca.html`, `polityka-prywatnosci.html`, `404.html`.

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
| **2026-08-06/07** | **SESJA: KALKULATOR WYCEN LIVE.** (1) **`/kalkulator-wyceny-szycia.html`** — 6 kroków, wynik w widełkach, **bez bramki mailowej**, 4 zakończenia (brak materiału / poniżej MOQ / wyrób poza ofertą / wycena). Klocki wyboru zamiast list rozwijanych, pasek 12 miesięcy z oznaczeniem obłożenia, przyklejony pasek z ceną na telefonie; (2) **Decyzje właściciela zmieniające pierwotny pakiet:** MOQ **50 szt.** jednolite (zgodne z „od 50 sztuk" na całej stronie), **nie odrzucamy w kalkulatorze, odrzucamy w rozmowie** (powyżej MOQ cena zawsze), **próg skali per wyrób** (płaszcz 200, żakiet 280, bluzka 1040) z komunikatem o rozłożeniu na partie, zakres dopasowany do kroku 1, odpowiedź **~7 dni roboczych** zamiast 24 h (poprawione też w `form-handler.js`, dotyczy wszystkich formularzy); (3) **Cennik `2026-08-e`** generowany z modelu kosztowego (`~/ISABELL-model`, poza repo), wyłącznie punkty cenowe i progi, zero stawek i czasów; (4) **Weryfikacja:** 9090 kombinacji vs model (zero zaniżeń poniżej progu opłacalności), 192 testy przecieków ceny, układ na 8 szerokościach 320-1440 px; (5) **SEO:** treść statyczna w źródle (tabela widełek, 3 sekcje, FAQ w akordeonie), FAQPage + BreadcrumbList, linkowanie dwukierunkowe z wpisami o kosztach i MOQ, pozycja w stopce na 37 stronach, sitemap + llms.txt; (6) **Pipeline sprawdzony:** filtr 2. gałęzi routera przepuszcza `form_type=kalkulator` (**nie było blokera**), dane idą w polu `description` → kolumna `Notes`, test zakończony sukcesem (1,8 KB wobec 453 B) | `b8ffd2b`, `8f02b9b`, `da27bc7` |
| **2026-07-30/08-01** | **SESJA: naprawa bugów + /wspolpraca.html + sieć partnerska.** (1) **Bugfixy krytyczne:** podwójna wysyłka formularzy (inline handler usunięty z 33 stron, zostaje `form-handler.js`), faux bold w `DM Serif Display` (jawne `font-weight: 400`, 320 deklaracji w 26 plikach), 345 myślników em/en → łącznik w 39 plikach; (2) **AWARIA I HARTOWANIE:** bot wysłał na webhook etykietę placeholdera „Wybierz zakres", Airtable odbił `422`, Make **wyłączył scenariusz na ~12 h**. Pola `Rodzaj usługi` i `Szacowana ilość` w tabeli leadów zamienione z listy wyboru na **tekst**, więc żadna wartość już go nie położy; (3) **`/wspolpraca.html` LIVE** — sieć dostawców uzupełniających (zdobienie, materiały, konsultacje), 9 sekcji, formularz 14 pól, FAQ, własne grafiki Higgsfield; Airtable tabela `Wspolpraca` + **trzecia gałąź routera Make** (uwaga: router uruchamia KAŻDĄ pasującą gałąź, więc filtr leadów trzeba było zawęzić); (4) **GA4:** `partner_application` jako trzeci typ zgłoszenia + wymiar niestandardowy „Strona formularza" dla `form_source`; (5) **Social + OG:** ikony IG/FB/YT/TikTok w stopce na 36 stronach, profile w `sameAs` na 10 stronach, **31 dedykowanych obrazków OG** (wcześniej 34 strony dzieliły jeden ogólny); (6) polityka prywatności: sekcja formularza współpracy, doprecyzowane retencje (3 lata od końca roku / 5 lat podatkowe), linki do dokumentów Make i Airtable | `8dab40d`, `4038f75`, `e4bb802`, `3a05eee` |
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

**Faza wzrostu: pomiar → autorytet → konwersja.** Fundament gotowy i live.

**Stan po sesji 2026-08-06/07:**
- ✅ **KALKULATOR WYCEN ZAMKNIĘTY I LIVE.** `/kalkulator-wyceny-szycia.html`, cennik `2026-08-e`, pipeline sprawdzony end-to-end. Model kosztowy powstał i leży w `~/ISABELL-model` (**poza repo**, zawiera płace i faktury). Pakiet wdrożeniowy w `pakiet-publiczny/` (gitignore).
- ✅ **Pomiar jest uczciwy.** Do 30.07 każde wysłanie formularza tworzyło **dwa** rekordy w Airtable i dwa maile. Naprawione. Historia sprzed 30.07 jest **zawyżona** i czeka na odduplikowanie.
- ✅ **Trzy typy zgłoszeń mierzone osobno w GA4:** `generate_lead`, `job_application`, `partner_application`, plus `contact_click`. Kalkulator liczy się jako `generate_lead` z `form_source=/kalkulator-wyceny-szycia.html`. Wymiar „Strona formularza" **nie działa wstecz**, historia od 30.07.
- ✅ **`/kariera.html`, `/wspolpraca.html`, `/kalkulator-wyceny-szycia.html` LIVE.**
- ✅ **POMIAR DOMKNIĘTY 07.08 (audyt GA4/GTM).** **GTM nie istnieje i to decyzja** — wszystko na `gtag.js` na 37/37 stron, dla statycznej strony bez e-commerce GTM to zbędna warstwa. Właściwa usługa GA4 to **„Szwalnia ISABELL" (530061872)**, nie `isabell.pl` (422659936, sklep DTC) — obie siedzą w koncie 298400248 na `mpjecommerce@gmail.com`. Domknięte: GA4 **połączony z Search Console** (raporty „Zapytania" i „Ruch z bezpłatnych wyników" działają, historia zaciągnęła się od razu), kluczowe zdarzenia uzupełnione o `job_application`/`partner_application`/`contact_click`, odznaczone martwe `close_convert_lead`/`qualify_lead`, zarejestrowane **wymiary kalkulatora** (`wyrob`, `ilosc`, `prog_ilosci`, `niska_wartosc`). Wymiary i kluczowe zdarzenia **nie działają wstecz**, historia od 07.08.
- ⏳ **Pit stop pomiarowy: 2026-09-01** (przesunięty z 19.08 — Michał niedostępny ok. 10 dni od 19/20.08). Eksport GSC (Performance + Coverage) + GA4. Pierwszy pomiar z kalkulatorem i trzema wpisami z 08.08 w indeksie. Dłuższe okno to zresztą lepszy pomiar: nowe wpisy zdążą się zaindeksować.
- 🔍 **Stan indeksacji sprawdzony 08.08 przez API:** strona główna **„Submitted and indexed"**, ostatni crawl 07.08 20:38, czyli **już po zmianie title/meta** — nowy snippet jest w indeksie i pit stop go zmierzy. Rich results: wykryte „Review snippets", zero błędów. Linki przychodzące widziane przez Google: `isabell.pl`, `szwalnia-zabki.pl`, `/realizacje.html`.
- ⚠️ **`/kalkulator-wyceny-szycia.html`: „Crawled - currently not indexed"** (crawl 07.08 04:18). Google go odwiedził i na razie nie zaindeksował. Przy stronie opublikowanej dzień wcześniej to normalne, ale **sprawdzić ponownie na pit stopie** — jeśli stan się utrzyma, to sygnał, że Google uznaje stronę za zbyt cienką lub zbyt zbliżoną do innych.
- ℹ️ **Sitemap zgłoszony ponownie 08.08.** Uwaga: Google **nie udostępnia w API przycisku „Request Indexing"** dla zwykłych stron (Indexing API obsługuje wyłącznie JobPosting i BroadcastEvent). Ręczne zgłoszenie pojedynczych URL-i jest możliwe tylko z panelu GSC.

**Pomiar bazowy 07.08 (28 dni, 10.07-06.08), źródło: API GSC + GA4 Data API:** 264 użytkowników, 433 sesje, 1 018 odsłon. Kanały: Organic 264, Direct 98, **AI Assistant 56 (~13% ruchu)**, Referral 11, Social 3. Lejek: `form_start` 22 → `generate_lead` 10 = **45% ukończenia**. GSC: **170 kliknięć, 6 595 wyświetleń, CTR 2,58%, śr. poz. 10,76**, 183 unikalne frazy. Trend rosnący: początek lipca 1-8 kliknięć dziennie, początek sierpnia 10-13, pozycja z ~12 na ~9.

> ⚠️ **Nie czytać liczb GSC z raportu Search Console w GA4.** Pokazuje ~30 kliknięć i CTR 0,86% wobec 170 i 2,58% z API — bo dopasowuje tylko sesje, które GA4 potrafi powiązać ze stroną wejścia. Zaniża ~5×. Liczby raportowe brać z `gsc-archiwum/`, raport w GA4 służy wyłącznie do wiązania fraz z zachowaniem na stronie.

**Co pomiar 07.08 pokazał o treści (materiał wyjściowy do wpisów 21-27):**
- ✅ **Long-tail działa.** „szwalnia małe ilości" → `/uslugi/male-serie.html`, **pozycja 3,1, CTR 25,6%**. „szwalnia od 1 sztuki" → `/minimalne-zamowienie-szwalnia-moq.html`, **pozycja 4,2**, wpis o MOQ prawidłowo przechwytuje i tłumaczy próg 50 szt. Ten mechanizm działa, nie ruszać.
- ⛔ **„szwalnie odzieży ciężkiej" — 500 wyświetleń, pozycja 7,3, ZERO kliknięć. NIE OPTYMALIZOWAĆ POD TĘ FRAZĘ.** Sesja 07.08 zapisała, że „Michał potwierdził, że odzież ciężka to realna oferta" — **to było nieporozumienie, sprostowane 08.08.** Potwierdzenie dotyczyło kurtek i płaszczy, a nie „odzieży ciężkiej" w znaczeniu branżowym. W branży **odzież ciężka = kaletnictwo, obuwie, odzież motocyklowa** — czyli dokładnie to, od czego `uslugi/szycie-odziez-damska.html:225` sam odsyła klienta („branże dla szwalni wysoce specjalistycznych"). **08.08 usunięto „odzież ciężką i lekką" z `description` i `og:description`** w `index.html`; na jej miejsce weszły konkretne wyroby: kurtki, płaszcze, żakiety, sukienki, odzież firmowa. Fraza zostaje niewykorzystana **świadomie** — intencja jest cudza, a kliknięcia z niej i tak by nie skonwertowały.
- 🔧 **Strona główna zbiera 3 820 z 6 595 wyświetleń (58%) przy CTR 1,8%** (2 677 wyświetleń przypisanych do konkretnych fraz, 124 frazy, CTR 0,64%). Łapie ogólne frazy na pozycjach 9-15 i nie zamienia ich na kliknięcia. **07.08 przepisany title/meta**, efekt do sprawdzenia na pit stopie 19.08.

**Title/meta strony głównej — stan kanoniczny po korekcie 08.08:**
```
title: Szwalnia odzieży: kurtki, żakiety, odzież firmowa | Warszawa   (59 zn.)
meta:  Szyjemy na zlecenie kurtki, płaszcze, żakiety, sukienki
       i odzież firmową. Rodzinna szwalnia w Ząbkach k. Warszawy
       od 1990. Małe serie od 50 sztuk.                            (145 zn.)
```
`<title>` i `og:title` bez zmian od 07.08. **`description` i `og:description` poprawione 08.08** — wypadło „odzież ciężką i lekką" (patrz punkt wyżej), weszły płaszcze. **Z meta świadomie usunięto „Bezpłatna wycena w 48h"** — nie obiecujemy terminu w snippecie. Punkt odniesienia do porównania na pit stopie: CTR strony głównej **1,8%**.
- 🟡 **`/uslugi/odziez-firmowa.html`: 509 wyświetleń, 6 kliknięć (CTR 1,2%).** Druga strona wg wyświetleń, najsłabszy CTR z dużych.
- ⚪ **~230 wyświetleń to ruch brandowy obcej marki** („isabell", „isabella", „isabelle sukienki", „isabelle butik rzeszów") — 0 kliknięć, intencja cudza. Odjąć od bazy przy liczeniu CTR, nie optymalizować.

**Backlog, kolejność ustalona 07.08:**
1. 📋 **Wpisy blogowe: 23 z 25 opublikowane, zostały DWA.** Plan skrócony z 27 do 25 decyzją Michała 08.08.
   - ✅ **#27 `/jaka-odziez-firmowa-dla-pracownikow.html`** — LIVE 08.08. Bluzy/polo/kurtki, gramatury i składy. Klaster firmowy jest **pozycjonerski, bez zrealizowanych zleceń** (patrz pamięć projektu). Uczciwie mówi, że przy 50 szt. gotowa baza wychodzi taniej.
   - ✅ **#22 `/stopniowanie-rozmiarowe-wykroju.html`** — LIVE 08.08. Nisza pusta: cały TOP 10 to wizytówki 200-400 słów. Zero kwot w tekście, intencja cenowa zostaje przy #2.
   - ✅ **#25 `/rodzaje-sciegow-maszyny-szwalnicze.html`** — LIVE 08.08. **Odrzucono strukturę z researchu** („audyt szwalni", teza „brak renderki to sygnał alarmowy") — postawiłaby ISABELL pod kryterium, którego nie spełnia (specjalizacja w tkaninach, renderka to maszyna do dzianin). Oś to technologia ściegu.
   - ✅ **#23 `/metkowanie-odziezy-co-musi-byc-na-metce.html`** — LIVE 08.08. Dwa mity obalone: **kraj pochodzenia NIE jest obowiązkowy** dla tekstyliów w UE, a **symbole konserwacji są znakami towarowymi GINETEX/COFREET i wymagają licencji**. Metkowanie to realna usługa, więc tekst mówi „my to robimy", z zastrzeżeniem, że za treść metki odpowiada marka. Miało pokrycie w ofercie (`/uslugi/krojenie-wykonczenie.html`: „Metkowanie i pakowanie", metki żakardowe). Rozjechać z tech packiem, który wymienia metkę główną, care label i hangtag jako pozycje dokumentacji. Silny wątek prawny: rozporządzenie UE 1007/2011, symbole ISO 3758.
   - ✅ **#21 `/szwalnia-z-wlasna-krojownia.html`** — LIVE 08.08, **plan bloga domknięty: 25 wpisów**. Kąt potwierdzony trzema źródłami: grupy branżowe FB, ogłoszenia Oferteo, forum ekrawiectwo. Marki pytają wprost „czy posiadacie Państwo również krojownię", więc tekst odpowiada na to pytanie zamiast definiować krojownię. **Granice utrzymane:** zero cen i zero parametrów maszyn (podstrona usług zostaje celem intencji transakcyjnej), matematyka metrażu zostaje przy wpisie o powierzonym materiale, opisy sprzętu przy wpisie o maszynach.

   ⚠️ **DECYZJA O OCENIE TEMATU (Michał, 08.08):** nie oceniać potencjału frazy po 28 dniach GSC. Mierzyliśmy naszą widoczność (2 wyświetlenia na „krojownia"), nie popyt rynkowy, a wpisy dopiero wchodzą w indeks. **Horyzont oceny: ~6 miesięcy.** Krojownia uzupełnia bezpośrednią usługę, więc ma wartość strukturalną niezależnie od wolumenu.

   📊 **REZERWY WIDOCZNE W GSC 08.08 (materiał na pit stop 01.09) — problem to CTR i pozycje, nie brak treści:**
   „szwalnia odzieży" 145 wyśw. / poz. 9,4 / **0 klik**; „usługi szwalnicze" 103 / 14,7 / 0; „produkcja odzieży" 70 / **43,6** / 0; „szycie odzieży damskiej" 64 / 12,4 / 0; „szwalnia usługowa" 60 / 19,4 / 0; „produkcja odzieży na zamówienie" 55 / 42,8 / 0; „szycie ubrań na zamówienie" 51 / 43,8 / 0; „szwalnia dla marek odzieżowych" 41 / 10,2 / 0. Frazy „produkcja odzieży*" siedzą na 5. stronie przy realnym wolumenie. Frazy usługowe należą do `/uslugi.html`, która do 08.08 miała **zero** linków kontekstowych z bloga.
   - ❌ **#24 i #26 SKREŚLONE 08.08.** #24 powielał opublikowany #3, #26 zjadałby #2 i kalkulator. Nie wracać.

   ⚠️ **DŁUG GRAFICZNY (Higgsfield, do zrobienia 09.08):**
   - **`/metkowanie-odziezy-co-musi-byc-na-metce.html`: hero i OG są TYMCZASOWE** — wykadrowane z istniejącej `assets/metkowanie-pakowanie-odziez.webp`. Do wygenerowania własne: hero (metka żakardowa i wszywka z informacjami na stole) + śródtekstowa (podział na dwa nośniki: metka z logo przy karku vs wszywka w szwie bocznym).
   - **`/rodzaje-sciegow-maszyny-szwalnicze.html`: brak grafiki śródtekstowej** — nie powstała, bo skończyły się kredyty Higgsfield (08.08). Michał doładowuje. Ma pokazywać różnicę między podwinięciem renderką (dwie równoległe linie) a szwem overlockowym. Prompt w historii sesji; preset: `nano_banana_pro`, 3:2, 2k, plik `assets/Blogi/`, 1440×966 webp.

2. 📋 **FAZA TREŚCI NA WRZESIEŃ 2026 (notatka Michała, przyjęta 08.08).** Ruszamy **po pit stopie 01.09**, na danych, nie na przypuszczeniach. Dwa wąskie kierunki, **selektywnie, świadomie NIE budujemy klastra:**
   - **Proof-content, 2-3 wpisy** — proces produkcji w ujęciu „co to znaczy dla marki": prasowanie i stabilizacja wyrobu, kontrola procesu, wykończenia. Cel: **E-E-A-T i cytowalność przez modele AI** (AI Assistant to już ~13% ruchu, patrz pomiar 07.08). **Uwaga: temat maszyn jest już zajęty** przez `/rodzaje-sciegow-maszyny-szwalnicze.html` z 08.08, więc proof-content musi wejść od innej strony niż park maszynowy.
   - **Top-of-funnel, 3-5 wpisów** — „jak założyć markę odzieżową" **widziane od strony produkcji**, czyli to, czego nie napisze agencja marketingowa: od pomysłu do pierwszej partii, co musisz mieć przed pierwszą rozmową ze szwalnią, ile trwa dojście do pierwszej sprzedaży. Szersza góra lejka niż dotychczasowe long-taile.
   - **Zasada nadrzędna:** każdy nowy temat przechodzi przez tę samą kontrolę anty-kanibalizacji co wpisy 22, 25 i 27. Przy 23 opublikowanych wpisach ryzyko zjadania własnych stron jest już realne i to ono, a nie liczba wpisów, wyznacza limit.

2. ❄️ **Odduplikowanie tabeli leadów — ODPUSZCZONE (decyzja Michała 08.08).** Duplikaty sprzed 30.07 zostają w tabeli, nie przeszkadzają w pracy. Pamiętać tylko przy czytaniu historii.
3. ✅ **Odzież ciężka: ZAMKNIĘTE 08.08 przez sprostowanie, nie przez treść.** Fraza odpada jako cel (patrz punkt o niewykorzystanych frazach wyżej), meta poprawione. **Nie wracać do tematu bez nowej decyzji Michała.**
4. ✅ **Rozjazd czasu odpowiedzi: ZAMKNIĘTY 07.08.** Michał podał realne terminy — odpowiedź 48 h, wycena do 7 dni. Ujednolicone w trzech miejscach (patrz §1). Sprawdzone: zero pozostałości „24 h" jako naszej obietnicy.
- ✅ **Dostęp GSC + GA4 po API: NAPRAWIONY 07.08.** Przyczyną nie była propagacja ani złe konto człowieka. Serwer MCP łączy się jako **konto usługi `gsc-mcp@isabell-gsc.iam.gserviceaccount.com`** (projekt `isabell-gsc`, klucz w `~/.config/gsc-mcp/service-account.json`, chmod 600, poza repo) — i to konto nie było dodane do property szwalni. Dodane z uprawnieniem Pełne w GSC oraz rolą Przeglądający w GA4, włączone Analytics Data API. Klucz nie wygasa, więc nadaje się pod crona. Skrypt archiwizacji: **`gsc-archiwum/seo-archiwum.py`** (cały katalog w `.gitignore`, bo repo jest publiczne i Vercel serwuje wszystko, co do niego wjedzie). Uruchomienie: `python3 seo-archiwum.py --miesiac 2026-07`. Eksport miesięczny robić **najwcześniej 4 dnia następnego miesiąca** — GSC ma 2-3 dni opóźnienia.
6. 📋 **Archiwizacja GSC** — dane znikają po 16 miesiącach. Materiał z okresu indeksacji 4→25 stron przestanie być dostępny w połowie 2027.
7. 📋 Strona autora Michała (czeka na bio + cytat); opinie Google (2 → kilkanaście).
8. 📋 `validThrough` w trzech `JobPosting` wygasa **2026-10-31**, odświeżać co kwartał.
9. 📋 **Reautoryzacja Gmail w Make do 2026-10-12** — po tej dacie maile ze zgłoszeń przestaną przychodzić.
10. 📋 Strona współpracy ma ok. 18 ekranów telefonu; dalsze skrócenie = decyzja redakcyjna.
- ❄️ Umowy powierzenia (DPA) z Make i Airtable — **świadomie odłożone 31.07**. Szczegóły w `_briefy/rodo-podkladka-wspolpraca.md`.
- ❄️ `baseSalary` w ofertach pracy — **świadomie odrzucone**. Nie wracać bez decyzji Michała.
- ❄️ Karta wyceny w PDF z kalkulatora — odłożona, nie blokuje.

**Dług techniczny (drobny, nie pilny):**
- Nagłówki FAQ na wpisach blogowych mają 24 px wysokości zamiast wymaganych 44 px (cel dotykowy). W kalkulatorze poprawione lokalnie, na blogu nie ruszane. Jedna reguła w `style.css`.
- Sześć pustych kolumn w tabeli leadów (`wyrob`, `ilosc_dokladna`, `wycena`, `wersja_cennika`, `form_type`, `source`) czeka na mapowanie w Make. Dane i tak docierają w polu `description`. **UWAGA: `Refresh` przy tabeli w module Airtable kasuje całe istniejące mapowanie.**

**Leady:** ~26–30 zgłoszeń tygodniowo **łącznie ze wszystkich kanałów** (formularze + wizytówka Google + telefony + WhatsApp + maile), nie z samego formularza. GA4 mierzy wyłącznie formularz, więc jego liczby są z natury niższe i to nie jest błąd.
