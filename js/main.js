// AI TechWire — Main JS

// Make cards clickable (placeholder — links to full articles later)
document.querySelectorAll('.card, .hero-main, .sidebar-card').forEach(card => {
  card.style.cursor = 'pointer';
});

// Active nav link
const path = window.location.pathname;
document.querySelectorAll('nav a').forEach(link => {
  if (link.href === window.location.href) {
    link.classList.add('active');
  }
});

// Newsletter form
const form = document.querySelector('.newsletter-form');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const input = form.querySelector('input');
    if (input.value) {
      form.innerHTML = '<p style="color:var(--finance-color);font-weight:700">✓ You\'re subscribed! First issue lands tomorrow morning.</p>';
    }
  });
}
