// Theme switch, mobile menu, the feature showcase and old links. No third-party code.
(function () {
  'use strict';

  // The site used to be one long page: its section links (#funciones...) now go to their page.
  const main = document.querySelector('main[data-legacy-anchors]');
  if (main && location.hash) {
    try {
      const target = JSON.parse(main.dataset.legacyAnchors)[decodeURIComponent(location.hash.slice(1))];
      if (target) location.replace(target);
    } catch (e) { /* stays on the home page */ }
  }

  const root = document.documentElement;
  const themeButton = document.querySelector('[data-theme-toggle]');
  if (themeButton) {
    themeButton.addEventListener('click', () => {
      const next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('miga-theme', next); } catch (e) { /* not remembered */ }
    });
  }

  const nav = document.querySelector('.nav');
  const menuButton = document.querySelector('[data-menu-toggle]');
  if (nav && menuButton) {
    menuButton.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      menuButton.setAttribute('aria-expanded', String(open));
    });
    const close = () => {
      nav.classList.remove('open');
      menuButton.setAttribute('aria-expanded', 'false');
    };
    nav.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', close));
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        close();
        menuButton.focus();
      }
    });
  }

  // Showcase: one tab per area of the app, with arrow-key navigation.
  const tabs = Array.from(document.querySelectorAll('.picker [role="tab"]'));
  function select(tab) {
    tabs.forEach(t => {
      const selected = t === tab;
      t.setAttribute('aria-selected', String(selected));
      t.tabIndex = selected ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !selected;
    });
  }
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab));
    tab.addEventListener('keydown', e => {
      const step = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!step) return;
      e.preventDefault();
      const next = tabs[(i + step + tabs.length) % tabs.length];
      select(next);
      next.focus();
    });
  });

  // The marquee repeats its chips once so the loop has no gap.
  document.querySelectorAll('.marquee-track').forEach(track => {
    Array.from(track.children).forEach(chip => {
      const copy = chip.cloneNode(true);
      copy.setAttribute('aria-hidden', 'true');
      track.appendChild(copy);
    });
  });
})();
