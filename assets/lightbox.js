/* Lightbox galerii realizacji (bez bibliotek).
   Wlacza sie na kontenerze z atrybutem data-lightbox, np.
   <div class="realizacje-grid" data-lightbox>. Kazdy kafel z <img> dostaje
   przezroczysty <button> na calej powierzchni (prawdziwy przycisk: fokus,
   Enter/Spacja, czytnik ekranu), a klikniecie otwiera natywny <dialog>
   z tym samym plikiem, podpisem i strzalkami.
   Zamykanie: X, Esc, klikniecie w tlo. Fokus wraca na kafel.
   Nie rusza loading="lazy" na kaflach: duzy obraz dostaje src dopiero
   przy otwarciu i jest to ten sam plik, wiec idzie z cache przegladarki.
   Bez wplywu na zgody i GA4.
   Filtry (np. /realizacje.html) ukrywaja kafle atrybutem hidden: strzalki
   i licznik obejmuja wtedy tylko widoczne zdjecia (lista liczona przy
   kazdym otwarciu i kroku). */
(function () {
  'use strict';
  var grids = document.querySelectorAll('[data-lightbox]');
  if (!grids.length || typeof HTMLDialogElement !== 'function') return;

  var items = [];
  grids.forEach(function (grid) {
    grid.querySelectorAll('.realizacja-tile, .gallery-tile').forEach(function (tile) {
      var img = tile.querySelector('img');
      if (!img) return;
      var badge = tile.querySelector('.tile-badge');
      var title = tile.querySelector('h3');
      var item = {
        tile: tile,
        img: img,
        badge: badge ? badge.textContent.trim() : '',
        title: title ? title.textContent.trim() : (img.alt || '')
      };
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'lightbox-trigger';
      btn.setAttribute('aria-haspopup', 'dialog');
      btn.setAttribute('aria-label', 'Powiększ zdjęcie: ' + item.title);
      btn.addEventListener('click', function () { open(item, btn); });
      tile.appendChild(btn);
      tile.classList.add('lightbox-tile');
      item.trigger = btn;
      items.push(item);
    });
  });
  if (!items.length) return;

  var dlg = document.createElement('dialog');
  dlg.className = 'lightbox';
  dlg.setAttribute('aria-label', 'Powiększone zdjęcie realizacji');
  dlg.innerHTML =
    '<div class="lightbox-inner">' +
      '<figure class="lightbox-figure">' +
        '<img class="lightbox-img" alt="" width="1067" height="1600" decoding="async">' +
        '<figcaption class="lightbox-caption">' +
          '<span class="lightbox-badge"></span>' +
          '<span class="lightbox-title"></span>' +
          '<span class="lightbox-count" aria-hidden="true"></span>' +
        '</figcaption>' +
      '</figure>' +
      '<button type="button" class="lightbox-btn lightbox-close" aria-label="Zamknij powiększenie">' +
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>' +
      '</button>' +
      '<button type="button" class="lightbox-btn lightbox-prev" aria-label="Poprzednie zdjęcie">' +
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><polyline points="15 6 9 12 15 18"/></svg>' +
      '</button>' +
      '<button type="button" class="lightbox-btn lightbox-next" aria-label="Następne zdjęcie">' +
        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><polyline points="9 6 15 12 9 18"/></svg>' +
      '</button>' +
    '</div>';
  document.body.appendChild(dlg);

  var bigImg = dlg.querySelector('.lightbox-img');
  var elBadge = dlg.querySelector('.lightbox-badge');
  var elTitle = dlg.querySelector('.lightbox-title');
  var elCount = dlg.querySelector('.lightbox-count');
  var btnClose = dlg.querySelector('.lightbox-close');
  var btnPrev = dlg.querySelector('.lightbox-prev');
  var btnNext = dlg.querySelector('.lightbox-next');
  var current = null;
  var returnFocus = null;
  var list = items;

  // Tylko kafle, ktorych nie ukryl filtr (hidden na kaflu lub przodku).
  function visible() {
    var v = items.filter(function (it) { return !it.tile.closest('[hidden]'); });
    return v.length ? v : items;
  }

  function show(it) {
    current = it;
    bigImg.src = it.img.currentSrc || it.img.src;
    bigImg.alt = it.img.alt || it.title;
    elBadge.textContent = it.badge;
    elBadge.hidden = !it.badge;
    elTitle.textContent = it.title;
    elCount.textContent = list.length > 1 ? (list.indexOf(it) + 1) + ' / ' + list.length : '';
  }

  function step(d) {
    if (list.length < 2) return;
    var k = list.indexOf(current);
    show(list[(k + d + list.length) % list.length]);
  }

  function open(it, trigger) {
    returnFocus = trigger || null;
    list = visible();
    if (list.indexOf(it) < 0) list = items;
    btnPrev.hidden = btnNext.hidden = list.length < 2;
    show(it);
    document.documentElement.classList.add('lightbox-open');
    dlg.showModal();
    btnClose.focus();
  }

  function close() {
    if (dlg.open) dlg.close();
  }

  dlg.addEventListener('close', function () {
    document.documentElement.classList.remove('lightbox-open');
    bigImg.removeAttribute('src');
    // Fokus na kafel, z ktorego otwarto (albo na biezacy po przewijaniu strzalkami).
    var target = current && current.trigger ? current.trigger : returnFocus;
    if (target) { try { target.focus({ preventScroll: true }); } catch (e) { target.focus(); } }
  });

  btnClose.addEventListener('click', close);
  btnPrev.addEventListener('click', function () { step(-1); });
  btnNext.addEventListener('click', function () { step(1); });

  // Klikniecie w tlo (poza zdjeciem, podpisem i przyciskami) zamyka.
  dlg.addEventListener('click', function (e) {
    if (e.target === dlg || e.target.classList.contains('lightbox-inner') ||
        e.target.classList.contains('lightbox-figure')) close();
  });

  dlg.addEventListener('keydown', function (e) {
    if (list.length < 2) return;
    if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
  });
  // Esc obsluguje sam <dialog> (zdarzenie cancel -> close).
})();
