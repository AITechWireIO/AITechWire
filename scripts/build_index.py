#!/usr/bin/env python3
"""
AITechWire Dynamic Index Builder

Automatically generates index.html by scanning article directories.
- Extracts metadata from article HTML (og:title, og:description, date, category)
- Sorts by date (newest first)
- Populates hero, trending sidebar, latest grid, and category sections
- Runs before each git push to keep front page fresh

Usage: python3 build_index.py
"""

import os
import re
from datetime import datetime
from pathlib import Path
from html import escape

# Configuration
WORKSPACE_DIR = Path(__file__).parent.parent
ARTICLES_DIR = WORKSPACE_DIR / "aitechwire" / "articles"
CATEGORY_DIRS = {
    "ai-tech": "AI & Tech",
    "finance": "Finance & Investing",
    "crypto": "Crypto & Web3",
    "prediction-markets": "Prediction Markets",
}
INDEX_OUTPUT = WORKSPACE_DIR / "aitechwire" / "index.html"

# Emoji map for categories
EMOJI_MAP = {
    "ai-tech": "🧠",
    "finance": "🏦",
    "crypto": "⚡",
    "prediction-markets": "🎯",
}

# Badge CSS classes
BADGE_MAP = {
    "ai-tech": "badge-ai",
    "finance": "badge-finance",
    "crypto": "badge-crypto",
    "prediction-markets": "badge-pm",
}

# Line color classes
LINE_MAP = {
    "ai-tech": "line-ai",
    "finance": "line-finance",
    "crypto": "line-crypto",
    "prediction-markets": "line-pm",
}


def extract_meta(html_path):
    """Extract metadata from an HTML file."""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract og:title
        title_match = re.search(r'<meta property="og:title" content="([^"]+)"', content)
        title = title_match.group(1) if title_match else Path(html_path).stem
        
        # Extract og:description
        desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', content)
        excerpt = desc_match.group(1) if desc_match else "No description"
        
        # Truncate excerpt to ~120 chars + ellipsis
        if len(excerpt) > 120:
            excerpt = excerpt[:117] + "…"
        
        # Extract date from meta (try multiple patterns)
        # Pattern 1: og:article:published_time
        date_match = re.search(r'<meta property="article:published_time" content="([^"]+)"', content)
        # Pattern 2: Custom meta date tag
        if not date_match:
            date_match = re.search(r'<meta name="date" content="([^"]+)"', content)
        # Pattern 3: Look for date in filename or article text
        if not date_match:
            # Try to find date in filename (YYYY-MM-DD-...)
            filename = Path(html_path).stem
            date_str_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
            if date_str_match:
                date_match = date_str_match
        
        if date_match:
            date_str = date_match.group(1)
            # Parse YYYY-MM-DD format
            try:
                if len(date_str) == 10:  # YYYY-MM-DD
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                else:  # ISO format with time
                    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                date_display = date_obj.strftime("%B %d, %Y")
            except:
                date_display = date_str
        else:
            date_display = "Unknown date"
        
        return {
            "path": html_path,
            "title": title,
            "excerpt": excerpt,
            "date": date_display,
            "date_sort": date_match.group(1) if date_match else "1970-01-01",
        }
    except Exception as e:
        print(f"Error parsing {html_path}: {e}")
        return None


def get_articles_by_dir():
    """Scan all article directories and return articles grouped by category."""
    articles = []
    
    # Scan /articles/ (no category subdirectory)
    if ARTICLES_DIR.exists():
        for html_file in sorted(ARTICLES_DIR.glob("*.html")):
            meta = extract_meta(html_file)
            if meta:
                meta["category"] = None
                meta["category_name"] = None
                meta["url"] = f"/articles/{html_file.name}"
                articles.append(meta)
    
    # Scan category subdirectories
    for cat_slug, cat_name in CATEGORY_DIRS.items():
        cat_dir = WORKSPACE_DIR / "aitechwire" / cat_slug
        if cat_dir.exists():
            for html_file in sorted(cat_dir.glob("*.html")):
                meta = extract_meta(html_file)
                if meta:
                    meta["category"] = cat_slug
                    meta["category_name"] = cat_name
                    meta["url"] = f"/{cat_slug}/{html_file.name}"
                    articles.append(meta)
    
    # Sort by date (newest first)
    articles.sort(key=lambda x: x["date_sort"], reverse=True)
    return articles


def render_card(article, card_type="full"):
    """Render an article card in HTML."""
    category_slug = article["category"] or "crypto"
    emoji = EMOJI_MAP.get(category_slug, "⚡")
    badge_class = BADGE_MAP.get(category_slug, "badge-crypto")
    category_name = article.get("category_name") or "Crypto & Web3"
    
    if card_type == "sidebar":
        # Sidebar card (numbered, compact)
        return f'''    </a><a href="{article['url']}" style="text-decoration:none;color:inherit;display:block"><div class="sidebar-card">
      <div class="sidebar-card-num"></div>
      <div class="sidebar-card-content">
        <div class="sidebar-card-title">{escape(article['title'])}</div>
        <div class="sidebar-card-meta"><span class="category-badge {badge_class}" style="font-size:10px;padding:2px 7px">{category_name}</span> · {article['date']}</div>
      </div>
    </div>'''
    else:
        # Full card (grid)
        return f'''  <a href="{article['url']}" style="text-decoration:none;color:inherit;display:block">
  <div class="card">
    <div class="card-img card-img-{category_slug}">{emoji}</div>
    <div class="card-body">
      <span class="category-badge {badge_class}">{category_name}</span>
      <div class="card-title">{escape(article['title'])}</div>
      <div class="card-excerpt">{escape(article['excerpt'])}</div>
      <div class="card-meta"><span>{article['date']}</span><span>5 min read</span></div>
    </div>
  </div></a>'''


def build_index_html(articles):
    """Generate full index.html with article data."""
    
    # Get hero article (latest)
    hero = articles[0] if articles else None
    hero_category_slug = hero["category"] or "crypto" if hero else "crypto"
    hero_category_name = hero.get("category_name") or "Crypto & Web3" if hero else "Crypto & Web3"
    
    # Build trending sidebar (top 4 articles)
    trending = articles[:4] if articles else []
    sidebar_html = ""
    for i, article in enumerate(trending, 1):
        category_slug = article["category"] or "crypto"
        badge_class = BADGE_MAP.get(category_slug, "badge-crypto")
        category_name = article.get("category_name") or "Crypto & Web3"
        sidebar_html += f'''    </a><a href="{article['url']}" style="text-decoration:none;color:inherit;display:block"><div class="sidebar-card">
      <div class="sidebar-card-num">{i:02d}</div>
      <div class="sidebar-card-content">
        <div class="sidebar-card-title">{escape(article['title'])}</div>
        <div class="sidebar-card-meta"><span class="category-badge {badge_class}" style="font-size:10px;padding:2px 7px">{category_name}</span> · {article['date']}</div>
      </div>
    </div>'''
    
    # Build latest articles grid (6 articles)
    latest_articles = articles[:6] if articles else []
    latest_html = "\n".join([render_card(a, "full") for a in latest_articles])
    
    # Build category sections
    category_sections = {}
    for cat_slug, cat_name in CATEGORY_DIRS.items():
        cat_articles = [a for a in articles if a["category"] == cat_slug][:2]
        if cat_articles:
            cards = "\n".join([render_card(a, "full") for a in cat_articles])
            line_class = LINE_MAP.get(cat_slug, "line-crypto")
            category_sections[cat_slug] = f'''<div class="section-header">
  <div class="section-title"><div class="section-line {line_class}"></div>{cat_name}</div>
  <a href="/{cat_slug}/" class="see-all">See all →</a>
</div>
<div class="cards-grid">
{cards}
</div>
'''
    
    # Render HTML template
    hero_emoji = EMOJI_MAP.get(hero_category_slug, "⚡")
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI TechWire — Where AI Meets Money</title>
  <meta name="description" content="Sharp analysis on AI, crypto, and markets for investors and forward-thinkers. No hype — just intelligence." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/style.css" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'><rect width='400' height='400' fill='%231a1a2e'/><circle cx='200' cy='200' r='175' fill='none' stroke='%23f0b429' stroke-width='3' stroke-opacity='0.4'/><polygon points='220,60 150,210 195,210 175,345 265,175 215,175 240,60' fill='%23f0b429'/></svg>" />
  <link rel="canonical" href="https://aitechwire.io/" />
  <meta property="og:title" content="AI TechWire — Where AI Meets Money" />
  <meta property="og:description" content="Sharp analysis on AI, crypto, and markets for investors and forward-thinkers." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://aitechwire.io/" />
  <meta property="og:image" content="https://aitechwire.io/img/og-default.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@AITechWireIO" />
  <meta name="twitter:image" content="https://aitechwire.io/img/og-default.png" />
</head>
<body>

<header>
  <div class="header-inner">
    <a href="/" class="logo"><svg width="36" height="36" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0">
      <defs>
        <radialGradient id="lgbg" cx="50%" cy="40%" r="60%"><stop offset="0%" stop-color="#1a1a2e"/><stop offset="100%" stop-color="#0a0a0f"/></radialGradient>
        <linearGradient id="lgbolt" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ffd96a"/><stop offset="100%" stop-color="#f0b429"/></linearGradient>
      </defs>
      <rect width="400" height="400" fill="url(#lgbg)"/>
      <circle cx="200" cy="200" r="175" fill="none" stroke="#f0b429" stroke-width="2" stroke-opacity="0.3"/>
      <polygon points="220,60 150,210 195,210 175,345 265,175 215,175 240,60" fill="url(#lgbolt)" stroke="#ffd96a" stroke-width="2" stroke-linejoin="round"/>
    </svg>AI <span>TechWire</span></a>
    <nav>
      <a href="/" class="active">Home</a>
      <a href="/ai-tech/">AI &amp; Tech</a>
      <a href="/finance/">Finance</a>
      <a href="/crypto/">Crypto &amp; Web3</a>
      <a href="/prediction-markets/">Prediction Markets</a>
      <a href="https://x.com/AITechWireIO" target="_blank" rel="noopener noreferrer" class="nav-x-btn">𝕏 Follow</a>
    </nav>
  </div>
</header>

<!-- HERO / TICKER -->
<section class="hero">
  <div class="hero-inner">
    <div class="hero-main">
      <div class="hero-badge">⚡ Latest</div>
      <h1 class="hero-title">{escape(hero['title'])}</h1>
      <p class="hero-subtitle">{escape(hero['excerpt'])}</p>
      <a href="{hero['url']}" class="hero-cta">Read Now →</a>
    </div>
    <div class="hero-sidebar">
      <div class="sidebar-label">Trending Now</div>
        {sidebar_html}
    </div>
  </div>
</section>

<!-- LATEST ARTICLES -->
<div class="section-header">
  <div class="section-title"><div class="section-line" style="background:var(--accent)"></div>Latest</div>
</div>
<div class="cards-grid">
{latest_html}
</div>

{category_sections.get('ai-tech', '')}
{category_sections.get('finance', '')}
{category_sections.get('crypto', '')}
{category_sections.get('prediction-markets', '')}

<!-- X PROMO -->
<div class="x-promo">
  <div class="x-promo-card">
    <div class="x-promo-handle">𝕏 @AITechWireIO</div>
    <div class="x-promo-desc">Daily AI news, market signals, and tech analysis for forward-thinking investors. No fluff — just intelligence.</div>
    <a href="https://x.com/AITechWireIO" target="_blank" rel="noopener noreferrer" class="x-follow-btn">Follow on 𝕏</a>
  </div>
  <div class="x-promo-card">
    <div class="x-promo-handle">⚡ AI TechWire</div>
    <div class="x-promo-desc">Where AI meets money. Sharp analysis on crypto, markets, and AI for investors and forward-thinkers.</div>
    <a href="#newsletter" class="x-follow-btn">Get Newsletter</a>
  </div>
  <div class="x-promo-card">
    <div class="x-promo-handle">📬 Morning Brief</div>
    <div class="x-promo-desc">Top AI, crypto, and market stories every morning before the bell. Free, sharp, to the point.</div>
    <a href="#newsletter" class="x-follow-btn">Subscribe Free</a>
  </div>
</div>

<!-- NEWSLETTER -->
<div class="newsletter" id="newsletter">
  <div class="newsletter-inner">
    <h2>⚡ The AI TechWire Morning Brief</h2>
    <p>Top AI, markets, and crypto stories — delivered every morning before the bell. Free forever.</p>
    <form class="newsletter-form" onsubmit="return false;">
      <input type="email" placeholder="your@email.com" />
      <button type="submit">Subscribe Free</button>
    </form>
  </div>
</div>

<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <div class="logo" style="margin-bottom:12px"><svg width="36" height="36" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0">
      <defs>
        <radialGradient id="lgbg2" cx="50%" cy="40%" r="60%"><stop offset="0%" stop-color="#1a1a2e"/><stop offset="100%" stop-color="#0a0a0f"/></radialGradient>
        <linearGradient id="lgbolt2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ffd96a"/><stop offset="100%" stop-color="#f0b429"/></linearGradient>
      </defs>
      <rect width="400" height="400" fill="url(#lgbg2)"/>
      <circle cx="200" cy="200" r="175" fill="none" stroke="#f0b429" stroke-width="2" stroke-opacity="0.3"/>
      <polygon points="220,60 150,210 195,210 175,345 265,175 215,175 240,60" fill="url(#lgbolt2)" stroke="#ffd96a" stroke-width="2" stroke-linejoin="round"/>
    </svg>AI <span>TechWire</span></div>
      <p>Where AI meets money. Sharp analysis for investors and forward-thinkers.</p>
    </div>
    <div class="footer-col"><h4>Sections</h4><ul>
      <li><a href="/ai-tech/">AI &amp; Tech</a></li>
      <li><a href="/finance/">Finance</a></li>
      <li><a href="/crypto/">Crypto &amp; Web3</a></li>
      <li><a href="/prediction-markets/">Prediction Markets</a></li>
    </ul></div>
    <div class="footer-col"><h4>Follow Us</h4><ul>
      <li><a href="https://x.com/AITechWireIO" target="_blank" rel="noopener noreferrer">𝕏 @AITechWireIO</a></li>
    </ul></div>
    <div class="footer-col"><h4>Company</h4><ul>
      <li><a href="/topics/">All Topics</a></li>
      <li><a href="#">About</a></li>
      <li><a href="#">Advertise</a></li>
      <li><a href="#">Privacy Policy</a></li>
    </ul></div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 AI TechWire. All rights reserved.</span>
    <span>Powered by <a href="#" style="color:var(--accent)">Lexonia Group</a></span>
  </div>
</footer>

</body>
</html>'''
    
    return html_content


def main():
    print("🔄 Building AITechWire index...")
    
    # Get all articles
    articles = get_articles_by_dir()
    print(f"✅ Found {len(articles)} articles")
    
    if not articles:
        print("⚠️  No articles found. Skipping index build.")
        return
    
    # Show top 3
    print("\nTop 3 articles (will appear on homepage):")
    for i, a in enumerate(articles[:3], 1):
        print(f"  {i}. {a['title'][:60]}... ({a['date']})")
    
    # Generate HTML
    html_content = build_index_html(articles)
    
    # Write to index.html
    INDEX_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\n✅ Index rebuilt: {INDEX_OUTPUT}")
    print(f"   Hero: {articles[0]['title'][:50]}...")
    print(f"   Latest section: {len(articles[:6])} articles")
    print(f"   Categories: AI & Tech, Finance, Crypto & Web3, Prediction Markets")


if __name__ == "__main__":
    main()
