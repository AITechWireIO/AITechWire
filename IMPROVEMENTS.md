# AITechWire — System Improvements Master Doc
*Last updated: 2026-06-21 | Maintained by Lexie 🦊*

---

## 🗂️ TABLE OF CONTENTS
1. Content & Style Rules
2. Quality Assurance Checks
3. Pipeline Architecture
4. Cron Schedule
5. X API — What Works / What Doesn't
6. Weekly Performance Review (Week 1 Results)
7. Integrations Map
8. Known Issues & Fixes Log

---

## 1. 📝 CONTENT & STYLE RULES

### Post Formats (ranked by performance)
| Rank | Style | Avg Impressions | Formula |
|------|-------|----------------|---------|
| 🥇 | Contrarian | 11.3 | Named figure + counterintuitive claim + 2–4 word punchline |
| 🥈 | Reactive | 5.5 | Breaking event + investment implication |
| 🥉 | Educational | 3.3 | Context → insight → takeaway |
| 4 | Cross-asset | 2.7 | Crypto vs stocks/gold/AI/TradFi comparison |
| 5 | Article promo | 3.0 | Tease + link + handle |
| 6 | One-liner | 1.5 | Tight punchy observation |

**The #1 rule (explains 30% of engagement gap):**
> *Named figure + counterintuitive claim + 2–4 word punchline = contrarian post that outperforms everything else.*

### Hard Content Rules
- ❌ NEVER use "Let me break it down 👇" on a standalone single tweet — ever
  - ✅ ONLY allowed: long articles OR numbered thread series (1/n format)
  - Blocked at both generation AND QA level — hardened June 21
- ❌ No pure price action posts ("BTC up 4%") — must include investment thesis
- ❌ No fabricated numbers — all data from real Grok/X/web research
- ❌ No sycophantic openers: "Appreciate", "Great point", "Thanks for asking"
- ✅ Every post: complete sentence ending with . ! or ?
- ✅ Under 280 chars total including " | @AITechWireIO"
- ✅ Named data points only (not vague "some analysts say")

### Cross-Asset Rule
At least **1 of 5** daily posts MUST compare asset classes:
crypto vs stocks, crypto vs gold, crypto vs AI tech, DeFi vs TradFi

### Pillar Strategy
| Pillar | Status | Notes |
|--------|--------|-------|
| Crypto & DeFi | ✅ Active | Primary focus |
| Prediction Markets | ✅ Active | Replaced Real Estate |
| AI & Tech | ✅ Active | Infrastructure, compute |
| Finance & Investing | ✅ Active | Macro, Fed, equities |
| Real Estate | ⏸️ PAUSED | Returns when Fed starts rate cuts |

### Opinion Leader Strategy
Primary focus = analysis of what key voices just said/did:
- Michael Saylor (@saylor) — MicroStrategy
- Vitalik Buterin (@VitalikButerin) — Ethereum
- Lyn Alden (@LynAldenContact) — macro analyst *(single 'n' in Lyn)*
- Raoul Pal (@RaoulGMI) — Real Vision
- Jordi Visser (@jvisserlabs) — AI Macro Nexus
- Anthony Scaramucci (@scaramucci) — SkyBridge
- Larry Fink (@LarryFink) — BlackRock
- Alexander Cutler (@wagmiAlexander) — Aerodrome / Dromos *(single 't' in Cutler)*
- Jeremy Allaire (@jerallaire) — Circle
- Ki Young Ju (@ki_young_ju) — CryptoQuant

Frame = "What [Leader] just said and why it matters."

### Article Structure (LAYERED approach)
- **Never start inside the topic** — start where the READER lives
- Framework: Cause → Effect → Solution → Investment lens
- Layer 1: Real-world problem the reader already feels
- Layer 2: Why existing solutions fail
- Layer 3: How the new thing restructures the problem
- Layer 4: Investment angle — pros, cons, what to watch
- Depth is fine. Wrong entry point is not.

### Excluded Topics
- HYPE/Hyperliquid — EXCLUDED from standalone articles & posts (context only)

---

## 2. 🔍 QUALITY ASSURANCE

### Site QA (`qa_site.py`) — 55 checks
Must return **"🟢 CLEAR TO DEPLOY"** before any git push.

Key checks:
- ✅ `og:image` present on every article
- ✅ `og:title` matches `<h1>` (no mismatch)
- ✅ HTML structure integrity (no truncated/broken tags)
- ✅ Balanced `<a>` tags (open = close count)
- ✅ All internal links resolve to real files
- ✅ Titles & meta descriptions within correct length
- ✅ No leaked API keys or secrets
- ✅ Security headers in `netlify.toml`
- ✅ `sitemap.xml` and `robots.txt` present
- ✅ No `onclick` remnants (proper `<a>` tags only)
- ✅ Logo SVG present on all pages
- ✅ Footer and nav present on all pages

**Deploy command (only after QA passes):**
```bash
cd /workspace/aitechwire && python3 /workspace/scripts/qa_site.py && \
git add . && git commit -m "..." && git push origin main
```

### X Post QA — Per-Post Rules
Before any post queues:
- Complete sentence (ends with . ! ?)
- Under 280 chars with `| @AITechWireIO`
- Body under 240 chars before handle
- No "let me break it down" on standalone tweets (HARD REJECT)
- Investment thesis present (not pure price action)
- All numbers sourced from real data

---

## 3. 🔧 PIPELINE ARCHITECTURE

### Daily Flow
```
6:50 AM CDT  → Editorial Preview (research 3–5 stories → Telegram)
7:00 AM CDT  → Daily Pipeline (5 posts + 1 article)
7:30 AM CDT  → Good Morning Briefing → Discord #good-morning
7:30 AM CDT  → Daily Cost Report → Telegram + Discord #pipeline-log
10 AM CDT    → Post #2 from queue
1 PM CDT     → Post #3 from queue
4 PM CDT     → Post #4 from queue
7 PM CDT     → Post #5 from queue
Every 4h     → Reply Monitor (check for new replies → Telegram for manual response)
9 AM CDT     → Reply Performance Check (24h engagement feedback)
```

### Weekly Flow
```
Sunday 9 AM CDT → Weekly Style & Performance Review
                  → Pull X analytics
                  → Tag by style, calculate avg engagement
                  → Update style-feedback.md + STYLE_GUIDE.md
                  → Update scoring weights in aitechwire_daily.py
                  → Post to Discord #performance
```

### Research Engine
- **Primary:** Grok 4.3 live X search (`x_search` tool)
- **Secondary:** `web_search` for corroboration
- **Fallback:** Claude direct research
- Zero fake data — system failed at this before June 16, now fixed

### Scoring System (0–40 pts)
- Relevance to pillars: 0–10
- Velocity (trending): 0–10
- Stakes (financial impact): 0–10
- Scroll-stop factor: 0–10
- Contrarian format bonus applied post-Week 1

---

## 4. ⏰ CRON SCHEDULE

| Job | Schedule | Timeout |
|-----|----------|---------|
| Editorial Preview | 6:50 AM CDT daily | 360s |
| Daily Pipeline | 7:00 AM CDT daily | 600s |
| Good Morning Briefing | 7:30 AM CDT daily | 300s |
| Daily Cost Report | 7:30 AM CDT daily | 180s |
| Post Queue — 10 AM | 10:00 AM CDT daily | 120s |
| Reply Performance Check | 9:00 AM CDT daily | 240s |
| Post Queue — 1 PM | 1:00 PM CDT daily | 120s |
| Post Queue — 4 PM | 4:00 PM CDT daily | 120s |
| Post Queue — 7 PM | 7:00 PM CDT daily | 120s |
| Thread Engine | Mon/Wed/Fri 11 AM CDT | 360s |
| Reply Monitor | Every 4h | 300s |
| Weekly Style Review | Sunday 9 AM CDT | 600s |
| Profile Picture Upload | June 23 12:00 UTC (one-shot) | 300s |

*All timeouts bumped 2–3× on June 21 — no more timeout failures.*

---

## 5. 🐦 X API — WHAT WORKS / WHAT DOESN'T

### Pay-Per-Use Tier (current)
| Feature | Status | Notes |
|---------|--------|-------|
| Original tweets | ✅ Works | Main posting method |
| Self-replies (threads 1/n) | ✅ Works | Thread Engine uses this |
| @mentions in original tweets | ✅ Works | Opinion leader strategy |
| Replies to others | ❌ Dead | Feb 2026 X policy change, Enterprise only |
| Quote-tweets via API | ❌ Dead | Removed April 20, 2026 |

### Reply Strategy (adapted)
- **API replies:** Disabled — 100% 403 failure rate
- **Thread Engine:** 1/n series Mon/Wed/Fri, self-replies (allowed) — 3x/week
- **Manual replies:** Oleg handles from phone
  - Oleg screenshots a thread → Lexie gives **1 response** (no options, no lists)
  - Style: eccentric + smart, surprising angle, make people click the profile

---

## 6. 📊 WEEK 1 PERFORMANCE REVIEW (June 15–21)

**16 posts | 82 total impressions**

### Top 3 Posts
1. *"OpenAI burns $34B a year..."* — **30 impressions**
   - Why: Named figure + "Eyes open." punchline
2. *"Kevin Warsh inherits a Fed holding at 3.50–3.75%..."* — **9 impressions**
   - Why: Named official + original metaphor
3. *"Warsh's dot plot: PCE 3.6%, core 3.3%..."* — **6 impressions**
   - Why: Specific data + portfolio call-to-action

### Bottom 3 Posts
1. *"Prediction markets hit $21B volume..."* — 1 impression
   - Why: Niche topic + weak hook, no named figure
2. *"The Fed whispered 'October'..."* — 3 impressions
   - Why: Too abstract, no investment angle
3. *"OpenAI/NVIDIA targeting 10GW+..."* — 2 impressions
   - Why: "10GW" meaningless without context for reader

### Actions Taken from Week 1 Data
- `style-feedback.md` — full analytics table saved
- `aitechwire_daily.py` — contrarian format elevated to #1 in scoring
- `STYLE_GUIDE.md` — data-backed patterns section added
- "Let me break it down" ban hardened to explicit FAIL in QA

---

## 7. 🔌 INTEGRATIONS MAP

| Service | Purpose | Status |
|---------|---------|--------|
| Anthropic (Claude Sonnet 4.6) | Writing, pipeline brain | ✅ Active |
| xAI / Grok 4.3 | Live research, X search | ✅ Active ($5 credit) |
| X API (Pay-per-use) | Auto-posting | ✅ Active ($10 credit) |
| Netlify | Site hosting (aitechwire.io) | ✅ Active |
| GitHub | Site deployment via git push | ✅ Active |
| Discord | Cockpit / durable record | ✅ Active (6 channels) |
| Telegram | Primary comms + alerts | ✅ Active |
| Apify | Oleg's other projects | ✅ Active (DO NOT cancel) |

### Discord Channels
| Channel | Purpose |
|---------|---------|
| #good-morning | Daily briefing |
| #pipeline-log | Daily pipeline + cost reports |
| #performance | Weekly analytics |
| #errors-alerts | Immediate failure alerts |
| #memory-updates | System changes, major decisions |
| #needs-your-input | Items awaiting Oleg |
| #research-feed | Editorial preview (6:50 AM) |

### Cost Structure (steady state)
| Item | Monthly |
|------|---------|
| VPS | $30 |
| Netlify | $9 |
| X Premium | $8 |
| Domain | $2.34 |
| Claude API | ~$5.63 |
| Grok API | ~$1.05 |
| X API | ~$3.48 |
| **Total (ex-Apify)** | **~$59.50** |

---

## 8. 🐛 KNOWN ISSUES & FIXES LOG

| Date | Issue | Fix |
|------|-------|-----|
| June 16 | Pipeline crash (FIXED_MONTHLY bug) | Fixed, deployed |
| June 16 | GitHub push failing (GIT_TERMINAL_PROMPT) | Set `GIT_TERMINAL_PROMPT=0` |
| June 16 | Fake research (Claude hallucinating data) | Replaced with live Grok 4.3 research |
| June 18 | X reply game 100% 403 failure | Disabled; replaced with Thread Engine |
| June 18 | Quote-tweets via API broken | Removed from pipeline (X policy) |
| June 21 | Weekly Style Review timing out (300s) | Bumped all cron timeouts 2–3× |
| June 21 | Telegram audio — machine transcripts | Noted: transcripts are untrusted, treat as approximate |

---

*This document lives at: `aitechwire/IMPROVEMENTS.md`*
*Update after every significant system change.*
