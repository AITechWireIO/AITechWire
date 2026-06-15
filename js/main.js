// AI TechWire — Card Navigation

// Per-page card URL map: [sectionClass, cardIndex] → url
// cardIndex = 0-based position within that section's cards-grid
const CARD_MAP = {
  // Homepage
  'index': [
    // AI & Tech section (cards 0-2)
    { section: 'badge-ai',          index: 0, url: '/ai-tech/ai-agents-and-money.html' },
    { section: 'badge-ai',          index: 1, url: '/ai-tech/' },
    { section: 'badge-ai',          index: 2, url: '/ai-tech/' },
    // Finance section (cards 0-2)
    { section: 'badge-finance',     index: 0, url: '/finance/death-of-correspondent-banking.html' },
    { section: 'badge-finance',     index: 1, url: '/finance/' },
    { section: 'badge-finance',     index: 2, url: '/finance/death-of-correspondent-banking.html' },
    // Crypto section (cards 0-2)
    { section: 'badge-crypto',      index: 0, url: '/crypto/future-of-ai-crypto.html' },
    { section: 'badge-crypto',      index: 1, url: '/crypto/future-of-ai-crypto.html' },
    { section: 'badge-crypto',      index: 2, url: '/crypto/' },
    // Real Estate section (cards 0-2)
    { section: 'badge-realestate',  index: 0, url: '/real-estate/' },
    { section: 'badge-realestate',  index: 1, url: '/real-estate/' },
    { section: 'badge-realestate',  index: 2, url: '/real-estate/' },
  ]
};

// Section page fallback — map each card to its flagship article
const SECTION_ARTICLE = {
  '/ai-tech/':     '/ai-tech/ai-agents-and-money.html',
  '/finance/':     '/finance/death-of-correspondent-banking.html',
  '/crypto/':      '/crypto/future-of-ai-crypto.html',
  '/real-estate/': '/real-estate/',
};

function getCurrentPage() {
  const path = window.location.pathname;
  if (path === '/' || path.includes('index.html') && !path.includes('/ai-tech') && !path.includes('/finance') && !path.includes('/crypto') && !path.includes('/real-estate')) return 'index';
  if (path.includes('/ai-tech/')) return 'ai-tech';
  if (path.includes('/finance/')) return 'finance';
  if (path.includes('/crypto/')) return 'crypto';
  if (path.includes('/real-estate/')) return 'real-estate';
  return 'index';
}

function initCards() {
  const page = getCurrentPage();
  const cards = document.querySelectorAll('.card');

  if (page === 'index') {
    // Track count per badge type
    const counters = {};
    cards.forEach(card => {
      const badge = card.querySelector('[class*="badge-"]');
      if (!badge) return;
      const badgeClass = [...badge.classList].find(c => c.startsWith('badge-'));
      if (!badgeClass) return;
      counters[badgeClass] = (counters[badgeClass] || 0);
      const idx = counters[badgeClass]++;
      const entry = CARD_MAP.index.find(e => e.section === badgeClass && e.index === idx);
      if (entry) {
        card.style.cursor = 'pointer';
        card.addEventListener('click', () => window.location.href = entry.url);
      }
    });
  } else {
    // Section pages — find the flagship article for this section
    const path = window.location.pathname;
    let sectionRoot = '/';
    for (const key of Object.keys(SECTION_ARTICLE)) {
      if (path.startsWith(key) || path.includes(key.replace(/\/$/, '/index'))) {
        sectionRoot = key;
        break;
      }
    }
    const articleUrl = SECTION_ARTICLE[sectionRoot] || sectionRoot;
    // First card → flagship article, rest → section index
    cards.forEach((card, i) => {
      const url = i === 0 ? articleUrl : sectionRoot;
      card.style.cursor = 'pointer';
      card.addEventListener('click', () => window.location.href = url);
    });
  }
}

// Hero & sidebar cards
function initHeroCards() {
  const hero = document.querySelector('.hero-main');
  if (hero) {
    hero.style.cursor = 'pointer';
    hero.addEventListener('click', () => {
      const badge = hero.querySelector('[class*="badge-"]');
      if (!badge) return;
      if (badge.classList.contains('badge-ai')) window.location.href = '/ai-tech/ai-agents-and-money.html';
      else if (badge.classList.contains('badge-finance')) window.location.href = '/finance/death-of-correspondent-banking.html';
      else if (badge.classList.contains('badge-crypto')) window.location.href = '/crypto/future-of-ai-crypto.html';
      else window.location.href = '/real-estate/';
    });
  }

  document.querySelectorAll('.sidebar-card').forEach(card => {
    const badge = card.querySelector('[class*="badge-"]');
    if (!badge) return;
    card.style.cursor = 'pointer';
    card.addEventListener('click', () => {
      if (badge.classList.contains('badge-ai')) window.location.href = '/ai-tech/';
      else if (badge.classList.contains('badge-finance')) window.location.href = '/finance/';
      else if (badge.classList.contains('badge-crypto')) window.location.href = '/crypto/';
      else window.location.href = '/real-estate/';
    });
  });
}

// Active nav
function initNav() {
  const path = window.location.pathname;
  document.querySelectorAll('nav a').forEach(link => {
    try {
      const lp = new URL(link.href).pathname;
      if (lp !== '/' && path.startsWith(lp)) link.classList.add('active');
      else if (lp === '/' && (path === '/' || path === '/index.html')) link.classList.add('active');
    } catch(e) {}
  });
}

// Newsletter
function initNewsletter() {
  const form = document.querySelector('.newsletter-form');
  if (!form) return;
  form.addEventListener('submit', e => {
    e.preventDefault();
    const input = form.querySelector('input');
    if (input && input.value) {
      form.innerHTML = '<p style="color:var(--finance-color);font-weight:700">✓ Subscribed! First issue tomorrow morning.</p>';
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initCards();
  initHeroCards();
  initNav();
  initNewsletter();
});
