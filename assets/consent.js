/* Zgoda na cookies analityczne: GA4 (Consent Mode v2) + Microsoft Clarity.
   Domyslny stan "denied" ustawia inline skrypt w <head> kazdej strony, przed
   gtag('js'), i tam tez podnosi zgode zapisana wczesniej. Ten plik pokazuje
   baner, zapisuje decyzje i laduje Clarity WYLACZNIE po akceptacji.
   Decyzja w localStorage 'isabell_zgoda' = 'tak|<ms>' albo 'nie|<ms>',
   wazna 12 miesiecy (tyle obiecuje polityka prywatnosci). */
(function () {
  var KLUCZ = 'isabell_zgoda';
  var WAZNOSC = 365 * 24 * 3600 * 1000;
  var CLARITY_ID = 'ypdpyct87w';

  function odczytaj() {
    try {
      var z = (localStorage.getItem(KLUCZ) || '').split('|');
      if ((z[0] === 'tak' || z[0] === 'nie') && Date.now() - Number(z[1]) < WAZNOSC) return z[0];
    } catch (e) {}
    return null;
  }

  function zapisz(v) {
    try { localStorage.setItem(KLUCZ, v + '|' + Date.now()); } catch (e) {}
  }

  function zaladujClarity() {
    if (window.clarity) return;
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY_ID);
    window.clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: 'granted' });
  }

  function usunCiasteczkaAnalityczne() {
    document.cookie.split(';').forEach(function (c) {
      var n = c.split('=')[0].trim();
      if (/^(_ga|_gid|_clck|_clsk|CLID|MUID)/.test(n)) {
        var host = location.hostname;
        ['', host, '.' + host, '.' + host.replace(/^www\./, '')].forEach(function (d) {
          document.cookie = n + '=; Max-Age=0; path=/' + (d ? '; domain=' + d : '');
        });
      }
    });
  }

  function ustaw(decyzja) {
    zapisz(decyzja);
    var zgoda = decyzja === 'tak';
    if (typeof gtag === 'function') {
      gtag('consent', 'update', { analytics_storage: zgoda ? 'granted' : 'denied' });
    }
    if (zgoda) {
      zaladujClarity();
    } else {
      if (window.clarity) window.clarity('consentv2', { ad_Storage: 'denied', analytics_Storage: 'denied' });
      usunCiasteczkaAnalityczne();
    }
    schowaj();
  }

  var baner = null;
  function schowaj() { if (baner) { baner.remove(); baner = null; } }

  function pokaz() {
    if (baner) return;
    baner = document.createElement('div');
    baner.className = 'zgoda';
    baner.setAttribute('role', 'dialog');
    baner.setAttribute('aria-label', 'Zgoda na pliki cookies');
    baner.innerHTML =
      '<div class="zgoda-tresc">'
      + '<p>Używamy cookies analitycznych (Google Analytics i Microsoft Clarity), żeby sprawdzać, '
      + 'jak korzystasz ze strony, i poprawiać ją. Clarity zapisuje anonimowy przebieg wizyty '
      + '(kliknięcia, przewijanie), bez treści wpisywanych w formularze. '
      + 'Szczegóły w <a href="/polityka-prywatnosci.html#cookies">polityce prywatności</a>.</p>'
      + '<div class="zgoda-przyciski">'
      + '<button type="button" class="zgoda-btn zgoda-nie" data-zgoda="nie">Odrzucam</button>'
      + '<button type="button" class="zgoda-btn zgoda-tak" data-zgoda="tak">Akceptuję</button>'
      + '</div></div>';
    baner.addEventListener('click', function (e) {
      var v = e.target.getAttribute && e.target.getAttribute('data-zgoda');
      if (v) ustaw(v);
    });
    document.body.appendChild(baner);
  }

  function linkWStopce() {
    var stopka = document.querySelector('.footer-bottom');
    if (!stopka || stopka.querySelector('.zgoda-ustawienia')) return;
    var a = document.createElement('a');
    a.href = '#';
    a.className = 'zgoda-ustawienia';
    a.textContent = 'Ustawienia cookies';
    a.addEventListener('click', function (e) { e.preventDefault(); pokaz(); });
    stopka.appendChild(a);
  }

  function start() {
    linkWStopce();
    var z = odczytaj();
    if (z === 'tak') zaladujClarity();
    else if (z === null) pokaz();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
