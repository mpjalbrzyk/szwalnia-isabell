/**
 * Szwalnia ISABELL - Webhook Form Handler
 * Wysyła dane formularzy do Make.com webhook → Airtable
 */
(function () {
  const WEBHOOK_URL = 'https://hook.eu1.make.com/iuy4kuiieqqawf3bfw9iq0jxgjh75ggr';

  document.querySelectorAll('.contact-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

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
        // Checkboxy i radio: bierzemy tylko zaznaczone.
        // Kilka checkboxow o tej samej nazwie (np. maszyny w formularzu kariery)
        // laczymy w jeden ciag po przecinku, zeby Airtable dostal czytelna liste.
        if (el.type === 'checkbox' || el.type === 'radio') {
          if (!el.checked) return;
          const val = el.value || 'TAK';
          data[key] = (el.type === 'checkbox' && data[key]) ? data[key] + ', ' + val : val;
          return;
        }
        data[key] = el.value;
      });

      // Add source page
      data['source'] = window.location.pathname;

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
            var formType = data.form_type || 'wycena';
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

            // Komunikat po wysylce. To JEDYNE zrodlo tych tekstow w calym serwisie
            // (handlery inline zostaly usuniete 30.07), wiec musza byc dopracowane.
            var messages = {
              kariera: ['Zgłoszenie wysłane!', 'Dziękujemy. Odezwiemy się telefonicznie, zwykle w ciągu kilku dni roboczych.'],
              wspolpraca: ['Zgłoszenie wysłane!', 'Dziękujemy. Michał odezwie się telefonicznie, zwykle w ciągu kilku dni roboczych.'],
              wycena: ['Wiadomość wysłana!', 'Z wyceną staramy się wrócić jak najszybciej, najczęściej zajmuje to około 7 dni roboczych.']
            };
            var msg = messages[formType] || messages.wycena;

            // Success
            form.innerHTML =
              '<div style="text-align:center;padding:40px 20px;">' +
              '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" style="margin-bottom:16px;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>' +
              '<h3 style="color:var(--primary);margin-bottom:8px;">' + msg[0] + '</h3>' +
              '<p style="color:var(--text-body);">' + msg[1] + '</p>' +
              '</div>';
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
