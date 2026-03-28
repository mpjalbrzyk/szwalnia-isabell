import os
import re

base_dir = "/Users/michaljalbrzykowski/Szwalnia ISABELL - Claude Code"

new_nav = """  <!-- NAVBAR -->
  <div class="navbar-wrapper">
    <nav class="navbar">
      <a href="/" class="logo"><img src="/assets/logo-szwalnia-isabell-v21.webp" alt="Szwalnia ISABELL" width="160" height="auto"></a>
      <ul class="nav-links">
        <li class="nav-dropdown">
          <a href="/uslugi.html" class="nav-dropdown-trigger">Usługi <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></a>
          <div class="dropdown-menu">
            <a href="/uslugi/szycie-odziez-damska.html">Szycie odzieży damskiej</a>
            <a href="/uslugi/odziez-firmowa.html">Odzież firmowa na zamówienie</a>
            <a href="/uslugi/krojenie-wykonczenie.html">Krojenie i wykończenie</a>
            <a href="/uslugi/male-serie.html">Małe serie</a>
            <a href="/szwalnia-warszawa.html">Szwalnia Warszawa</a>
            <a href="/szwalnia-zabki.html">Szwalnia Ząbki</a>
          </div>
        </li>
        <li><a href="/realizacje.html">Realizacje</a></li>
        <li><a href="/o-nas.html">O nas</a></li>
        <li><a href="/kontakt.html">Kontakt</a></li>
      </ul>
      <a href="/kontakt.html" class="btn-nav">Wyślij zapytanie</a>
      <button class="hamburger" aria-label="Menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </nav>
  </div>

  <!-- MOBILE MENU -->
  <div class="mobile-menu" id="mobile-menu">
    <ul>
      <li class="mobile-dropdown">
        <button class="mobile-dropdown-trigger">Usługi <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg></button>
        <ul class="mobile-dropdown-menu">
          <li><a href="/uslugi/szycie-odziez-damska.html">Szycie odzieży damskiej</a></li>
          <li><a href="/uslugi/odziez-firmowa.html">Odzież firmowa</a></li>
          <li><a href="/uslugi/krojenie-wykonczenie.html">Krojenie i wykończenie</a></li>
          <li><a href="/uslugi/male-serie.html">Małe serie</a></li>
          <li><a href="/szwalnia-warszawa.html">Szwalnia Warszawa</a></li>
          <li><a href="/szwalnia-zabki.html">Szwalnia Ząbki</a></li>
        </ul>
      </li>
      <li><a href="/realizacje.html">Realizacje</a></li>
      <li><a href="/o-nas.html">O nas</a></li>
      <li><a href="/kontakt.html">Kontakt</a></li>
      <li><a href="/kontakt.html" class="btn-nav">Wyślij zapytanie</a></li>
    </ul>
  </div>"""

new_footer = """  <!-- FOOTER -->
  <footer class="footer">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo"><img src="/assets/logo-szwalnia-isabell-v21.webp" alt="Szwalnia ISABELL" width="160" height="auto"></a>
        <p>Rodzinna szwalnia z tradycją w Ząbkach pod Warszawą. Krojenie, szycie i wykończenie pod jednym dachem.</p>
      </div>
      <div class="footer-col">
        <h4>Usługi</h4>
        <ul>
          <li><a href="/uslugi/szycie-odziez-damska.html">Szycie odzieży damskiej</a></li>
          <li><a href="/uslugi/odziez-firmowa.html">Odzież firmowa</a></li>
          <li><a href="/uslugi/krojenie-wykonczenie.html">Krojenie i wykończenie</a></li>
          <li><a href="/uslugi/male-serie.html">Małe serie</a></li>
          <li><a href="/szwalnia-warszawa.html">Szwalnia Warszawa</a></li>
          <li><a href="/szwalnia-zabki.html">Szwalnia Ząbki</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Strony informacyjne</h4>
        <ul>
          <li><a href="/realizacje.html">Realizacje</a></li>
          <li><a href="/o-nas.html">O nas</a></li>
          <li><a href="/kontakt.html">Kontakt</a></li>
          <li><a href="/blog.html">Blog</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Kontakt</h4>
        <ul>
          <li>Ząbki, ul. Batorego 44</li>
          <li>Pon–Pt: 8:00–16:00</li>
          <li><a href="mailto:kontakt@isabell.pl">kontakt@isabell.pl</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 Szwalnia ISABELL. Wszelkie prawa zastrzeżone.</p>
      <a href="/polityka-prywatnosci.html">Polityka prywatności</a>
    </div>
  </footer>"""

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Replace Navbar -> Main
            # Match everything from <!-- NAVBAR --> up to just before <main
            pattern_nav = re.compile(r'<!-- NAVBAR -->.*?(?=<main)', re.DOTALL)
            content = pattern_nav.sub(new_nav + "\n\n  ", content)
            
            # Replace Footer -> body end
            pattern_footer = re.compile(r'<!-- FOOTER -->.*?(?=</footer>)', re.DOTALL)
            content = pattern_footer.sub(new_footer.replace('</footer>', ''), content)
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)

print("Updated navigation and footer blocks successfully.")
