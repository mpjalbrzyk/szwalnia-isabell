/**
 * Szwalnia ISABELL – Webhook Form Handler
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
        data[key] = el.value;
      });

      // Add source page
      data['source'] = window.location.pathname;

      fetch(WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (res) {
          if (res.ok) {
            // Success
            form.innerHTML =
              '<div style="text-align:center;padding:40px 20px;">' +
              '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" style="margin-bottom:16px;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>' +
              '<h3 style="color:var(--primary);margin-bottom:8px;">Wiadomosc wyslana!</h3>' +
              '<p style="color:var(--text-body);">Odpowiemy najszybciej jak to mozliwe - zazwyczaj w ciagu kilku godzin.</p>' +
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
          err.textContent = 'Cos poszlo nie tak. Sprobuj ponownie lub napisz na kontakt@szwalnia-isabell.pl';
          btn.parentNode.insertBefore(err, btn.nextSibling);
        });
    });
  });
})();
