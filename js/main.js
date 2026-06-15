// AI TechWire — Main JS
// Navigation is handled by <a href> tags in HTML.
// This file handles nav highlighting and newsletter only.

// ── ACTIVE NAV ────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;
  document.querySelectorAll('nav a').forEach(link => {
    try {
      const lp = new URL(link.href).pathname;
      if (lp !== '/' && path.startsWith(lp)) link.classList.add('active');
      else if (lp === '/' && (path === '/' || path === '/index.html')) link.classList.add('active');
    } catch(e) {}
  });

  // ── NEWSLETTER ──────────────────────────────────────────────────────
  const form = document.querySelector('.newsletter-form');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const input = form.querySelector('input');
      if (input && input.value) {
        form.innerHTML = '<p style="color:var(--finance-color);font-weight:700">✓ Subscribed! First issue tomorrow morning.</p>';
      }
    });
  }
});
