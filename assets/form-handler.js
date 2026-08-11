/**
 * Szwalnia ISABELL - Webhook Form Handler
 * Wysyła dane formularzy do Make.com webhook → Airtable
 *
 * OCHRONA ANTYSPAMOWA (12.08.2026) - trzy warstwy po stronie przegladarki:
 *   1. honeypot   - ukryte pole, ktorego czlowiek nie zobaczy i nie wypelni,
 *   2. czas       - wyslanie szybsze niz MIN_FILL_MS to nie jest czlowiek,
 *   3. form_token - dowod, ze zgloszenie przeszlo przez ten skrypt.
 *
 * CZEGO TO NIE ROBI: nie zabezpiecza webhooka. Formularz strzela z przegladarki
 * PROSTO na hook.eu1.make.com, wiec bot, ktory zna adres (a adres wyciekl
 * publicznie do 11.08.2026), moze wyslac POST bez dotykania strony i zadna
 * z tych trzech warstw go nie zobaczy. Twarda bariera jest WYLACZNIE filtr
 * w scenariuszu Make - sprawdza form_token i poprawnosc pol przed Airtable.
 *
 * Honeypot wstrzykujemy JS-em zamiast wklejac do 33 plikow HTML, bo
 * convert_mdx.py trzyma wlasna kopie formularza i cofnalby taka zmiane
 * przy regeneracji wpisu.
 */
(function () {
  const WEBHOOK_URL = 'https://hook.eu1.make.com/iuy4kuiieqqawf3bfw9iq0jxgjh75ggr';

  // UWAGA: zmiana tej wartosci wymaga zmiany RÓWNIEŻ w filtrze scenariusza Make,
  // inaczej wszystkie zgloszenia zostana odrzucone jako spam.
  const FORM_TOKEN = 'isabell-web-2026';
  const HONEYPOT_NAME = 'website';
  const MIN_FILL_MS = 3000;

  const LOADED_AT = Date.now();

  // Komunikat po wysylce. To JEDYNE zrodlo tych tekstow w calym serwisie
  // (handlery inline zostaly usuniete 30.07), wiec musza byc dopracowane.
  const MESSAGES = {
    kariera: ['Zgłoszenie wysłane!', 'Dziękujemy. Odezwiemy się telefonicznie, zwykle w ciągu kilku dni roboczych.'],
    wspolpraca: ['Zgłoszenie wysłane!', 'Dziękujemy. Michał odezwie się telefonicznie, zwykle w ciągu kilku dni roboczych.'],
    wycena: ['Wiadomość wysłana!', 'Odezwiemy się w ciągu 48 h. Przygotowanie pełnej wyceny zajmuje zwykle do 7 dni roboczych.']
  };

  function renderSuccess(form, formType) {
    var msg = MESSAGES[formType] || MESSAGES.wycena;
    form.innerHTML =
      '<div style="text-align:center;padding:40px 20px;">' +
      '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" style="margin-bottom:16px;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>' +
      '<h3 style="color:var(--primary);margin-bottom:8px;">' + msg[0] + '</h3>' +
      '<p style="color:var(--text-body);">' + msg[1] + '</p>' +
      '</div>';
  }

  document.querySelectorAll('.contact-form').forEach(function (form) {
    // Honeypot: poza ekranem, poza tabulacja, niewidoczny dla czytnikow ekranu.
    // data-lpignore / data-1p-ignore powstrzymuja menedzery hasel przed
    // autouzupelnieniem, ktore zrobiloby z czlowieka falszywy alarm.
    var hp = document.createElement('input');
    hp.type = 'text';
    hp.name = HONEYPOT_NAME;
    hp.tabIndex = -1;
    hp.value = '';
    hp.setAttribute('autocomplete', 'off');
    hp.setAttribute('aria-hidden', 'true');
    hp.setAttribute('data-lpignore', 'true');
    hp.setAttribute('data-1p-ignore', '');
    hp.style.cssText = 'position:absolute !important;left:-9999px !important;width:1px;height:1px;opacity:0;pointer-events:none;';
    form.appendChild(hp);

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var formType = (form.querySelector('[name="form_type"]') || {}).value || 'wycena';

      // FILTR BOTOW. Cichy sukces - bot nie dowiaduje sie, ze zostal zlapany.
      // Ryzyko falszywego alarmu jest znikome: trzeba wypelnic komplet pol
      // wymaganych w mniej niz 3 sekundy albo wpisac cos w pole, ktorego
      // nie widac. Swiadomie NIE wysylamy zdarzenia GA4 i NIE strzelamy
      // na webhook, zeby spam nie zawyzal generate_lead ani tabeli leadow.
      var hpFilled = (hp.value || '').trim() !== '';
      var tooFast = (Date.now() - LOADED_AT) < MIN_FILL_MS;
      if (hpFilled || tooFast) {
        renderSuccess(form, formType);
        return;
      }

      const btn = form.querySelector('button[type="submit"]');
      const originalText = btn.textContent;
      btn.textContent = 'Wysyłanie...';
      btn.disabled = true;

      // Collect all named fields
      const data = {};
      const inputs = form.querySelectorAll('input, select, textarea');
      inputs.forEach(function (el) {
        const key = el.name || el.id;
        if (!key || el.type === 'file') return;
        if (key === HONEYPOT_NAME) return;
        // Checkboxy i radio: bierzemy tylko zaznaczone.
        // Kilka checkboxow o tej samej nazwie (np. maszyny w formularzu kariery)
        // laczymy w jeden ciag po przecinku, zeby Airtable dostal czytelna liste.
        if (el.type === 'checkbox' || el.type === 'radio') {
          if (!el.checked) return;
          const val = el.value || 'TAK';
          data[key] = (el.type === 'checkbox' && data[key]) ? data[key] + ', ' + val : val;
          return;
        }
        // Listy wyboru: gdy zaznaczona jest opcja-placeholder (disabled), wysylamy
        // pusty ciag zamiast jej etykiety. W lipcu 2026 bot wyslal na webhook
        // etykiete "Wybierz zakres", Airtable odbil 422 i Make wylaczyl
        // scenariusz na ~12 h. Ten guard jest generyczny, wiec obejmuje kazda
        // liste w serwisie, takze te dodane w przyszlosci.
        if (el.tagName === 'SELECT') {
          var opt = el.options[el.selectedIndex];
          data[key] = (opt && opt.disabled) ? '' : el.value;
          return;
        }
        data[key] = el.value;
      });

      // Add source page
      data['source'] = window.location.pathname;

      // Dowod przejscia przez ten skrypt. Filtr w Make przepuszcza wylacznie
      // zgloszenia z ta wartoscia, wiec POST wyslany prosto na webhook odpada.
      data['form_token'] = FORM_TOKEN;

      // Normalizacja pol formularza blogowego -> zgodnosc z mapowaniem Make/Airtable.
      // Blog wysyla: name, contact (telefon LUB e-mail w jednym polu), message.
      // Glowny formularz i scenariusz Make mapuja: email, phone, description.
      // Wypelniamy tylko gdy puste, wiec glownego formularza to nie dotyczy.
      if (data.contact && !data.email && !data.phone) {
        if (data.contact.indexOf('@') !== -1) {
          data.email = data.contact;
        } else {
          data.phone = data.contact;
        }
      }
      if (data.message && !data.description) {
        data.description = data.message;
      }

      fetch(WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (res.ok) {
            // Trzy rodzaje formularzy, trzy osobne zdarzenia GA4. Zgloszenie rekrutacyjne
            // i partnerskie to NIE leady sprzedazowe, wiec nie moga zawyzac generate_lead,
            // ktore jest oznaczone w GA4 jako kluczowe zdarzenie.
            var eventName = formType === 'kariera' ? 'job_application'
                          : formType === 'wspolpraca' ? 'partner_application'
                          : 'generate_lead';

            // GA4: konwersja (guard: liczymy raz na formularz)
            if (!form.dataset.leadTracked && typeof gtag === 'function') {
              form.dataset.leadTracked = 'true';
              gtag('event', eventName, {
                form_source: window.location.pathname,
                form_id: form.id || 'contact-form',
                form_type: formType
              });
            }

            renderSuccess(form, formType);
          } else {
            throw new Error('HTTP ' + res.status);
          }
        })
        .catch(function () {
          btn.textContent = originalText;
          btn.disabled = false;

          // Show error below button
          var existing = form.querySelector('.form-error-msg');
          if (existing) existing.remove();

          var err = document.createElement('p');
          err.className = 'form-error-msg';
          err.style.cssText = 'color:#dc2626;text-align:center;margin-top:12px;font-size:0.95rem;';
          err.textContent = 'Coś poszło nie tak. Spróbuj ponownie lub napisz na kontakt@isabell.pl';
          btn.parentNode.insertBefore(err, btn.nextSibling);
        });
    });
  });

  // GA4: klikniecia w telefon / e-mail (leady poza formularzem - telefony i maile z GMB/stopki)
  document.querySelectorAll('a[href^="tel:"], a[href^="mailto:"]').forEach(function (link) {
    link.addEventListener('click', function () {
      if (typeof gtag !== 'function') return;
      var isTel = link.getAttribute('href').indexOf('tel:') === 0;
      gtag('event', 'contact_click', {
        method: isTel ? 'phone' : 'email',
        link_source: window.location.pathname
      });
    });
  });
})();
