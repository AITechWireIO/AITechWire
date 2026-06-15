// AI TechWire — Main JS

// ── CARD CLICK NAVIGATION ────────────────────────────────────────────
// Maps card title keywords → article URLs
const ARTICLE_MAP = [
  // Flagship articles
  { key: "ai agents control",         url: "/ai-tech/ai-agents-and-money.html" },
  { key: "correspondent banking",     url: "/finance/death-of-correspondent-banking.html" },
  { key: "intelligence infrastructure", url: "/crypto/future-of-ai-crypto.html" },
  { key: "fight for intelligence",    url: "/crypto/future-of-ai-crypto.html" },

  // AI & Tech
  { key: "claude opus 4.8",           url: "/ai-tech/ai-agents-and-money.html" },
  { key: "autonomous ai agents",      url: "/ai-tech/ai-agents-and-money.html" },
  { key: "anthropic files for ipo",   url: "/ai-tech/ai-agents-and-money.html" },
  { key: "apple wwdc",                url: "/ai-tech/" },
  { key: "nvidia nemotron",           url: "/ai-tech/" },

  // Finance
  { key: "$36 billion chip",          url: "/finance/death-of-correspondent-banking.html" },
  { key: "portfolio shift",           url: "/finance/death-of-correspondent-banking.html" },
  { key: "s&p 500 breaks",           url: "/finance/" },
  { key: "fed holds",                 url: "/finance/" },
  { key: "rate cuts are coming",      url: "/finance/" },

  // Crypto
  { key: "bitcoin at $64",           url: "/crypto/future-of-ai-crypto.html" },
  { key: "ethereum at $1",           url: "/crypto/future-of-ai-crypto.html" },
  { key: "on-chain data shows btc",  url: "/crypto/future-of-ai-crypto.html" },
  { key: "10 ai x crypto",          url: "/crypto/future-of-ai-crypto.html" },
  { key: "regulated perpetual",      url: "/crypto/" },

  // Real Estate
  { key: "housing market finds",     url: "/real-estate/" },
  { key: "lock-in effect",           url: "/real-estate/" },
  { key: "midwest markets",          url: "/real-estate/" },
  { key: "rate cut playbook",        url: "/real-estate/" },
];

// Section fallback by badge
const SECTION_MAP = {
  "badge-ai":          "/ai-tech/",
  "badge-finance":     "/finance/",
  "badge-crypto":      "/crypto/",
  "badge-realestate":  "/real-estate/",
};

function getCardUrl(card) {
  const titleEl = card.querySelector(".card-title, .hero-title, .sidebar-card-title");
  const titleText = titleEl ? titleEl.textContent.toLowerCase() : "";

  // Try exact article match first
  for (const item of ARTICLE_MAP) {
    if (titleText.includes(item.key.toLowerCase())) {
      return item.url;
    }
  }

  // Fall back to section based on badge color
  const badge = card.querySelector("[class*='badge-']");
  if (badge) {
    for (const [cls, url] of Object.entries(SECTION_MAP)) {
      if (badge.classList.contains(cls)) return url;
    }
  }

  return null;
}

// Make all cards clickable
document.querySelectorAll('.card, .hero-main, .sidebar-card').forEach(card => {
  const url = getCardUrl(card);
  if (url) {
    card.style.cursor = 'pointer';
    card.addEventListener('click', () => { window.location.href = url; });
  }
});

// ── ACTIVE NAV LINK ──────────────────────────────────────────────────
document.querySelectorAll('nav a').forEach(link => {
  const linkPath = new URL(link.href, window.location.origin).pathname;
  const currentPath = window.location.pathname;
  if (linkPath !== '/' && currentPath.startsWith(linkPath)) {
    link.classList.add('active');
  } else if (linkPath === '/' && (currentPath === '/' || currentPath === '/index.html')) {
    link.classList.add('active');
  }
});

// ── NEWSLETTER FORM ──────────────────────────────────────────────────
const form = document.querySelector('.newsletter-form');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const input = form.querySelector('input');
    if (input && input.value) {
      form.innerHTML = '<p style="color:var(--finance-color);font-weight:700;font-size:15px">✓ You\'re subscribed! First issue lands tomorrow morning.</p>';
    }
  });
}
