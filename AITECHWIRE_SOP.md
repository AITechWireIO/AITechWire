# AITechWire — Standard Operating Procedures
*Last updated: 2026-06-16 | Owner: Oleg | Operator: Lexie*

---

## 🎯 Mission
AI researches trending topics → Lexie synthesizes + writes → auto-posts to X → earns creator revenue.
**Lexie's role: Editor + Writer. NOT a guesser. Real intelligence in → sharp content out.**

---

## 📋 Daily Pipeline — Full Sequence

### 6:50 AM CDT — Editorial Preview (`editorial_preview.py`)
> **Built 2026-06-17.** Runs Grok research, scores top 6 stories, sends Oleg a preview via Telegram + Discord #research-feed — 10 minutes before the pipeline fires.
> Format: ranked story list with pillar, score/50, headline, key voices.
> No writing, no posting — pure visibility.

### 7:00 AM CDT — Pipeline runs (`aitechwire_daily.py`)

**Step 1: RESEARCH (live sources)**
- Grok 4.3 (`/v1/responses` + `x_search` + `web_search`) → what's happening on X RIGHT NOW
- X API → latest tweets from @RaoulGMI, @saylor, @VitalikButerin, @LynAldenContact, @jerallaire
- RSS feeds → CoinDesk, The Block, Reuters, Bloomberg
- Output: 8 raw stories with metadata

**Step 2: SCORING (automated)**
Each story scored 0–10 on 5 dimensions:
- **RELEVANCE** — fits our 4 pillars (AI/tech, finance, crypto/DeFi, prediction markets)
- **VELOCITY** — volume of discussion on X right now (high/medium/low)
- **STAKES** — direct financial/investment impact for a large segment
- **SCROLL-STOP** — surprising, contrarian, high-consequence enough to make smart investors pause
- **EDITORIAL FIT** — has investment thesis/analysis, not pure price action

**HARD RULE 1: Reject pure price action news.** Stories like "Bitcoin dipped to $63K" or "Tech stock up 5%" are automatically excluded unless they include explicit analysis language: "why", "analysis", "breakdown", "thesis", "implication", "explained", etc. Price + macro context alone ≠ analysis.

**HARD RULE 2: Reject pure FUD without balance.** Stories with doom language ("collapse", "crash", "panic", "meltdown", "disaster") are excluded unless they include balanced perspective: "why", "opportunity", "structural", "thesis", "long-term", etc. Don't become a "fear-mongering resource" — bearish takes must have reasoning or counterbalance.

Rules: max 2 per pillar in top 6 (crypto gets 3). Highest scored → article. Most scroll-stop → post #1.

**Step 3: WRITING (Claude Sonnet)**
- 5 X posts — rotate styles: eccentric, contrarian, emoji, one-liner, sharp take
- 1 full article (600–900 words) on highest-scored story
- Voice: Sharp, opinionated, forward-looking. Data-backed. Cite sources. No fluff.

**Step 4: POST #1 → X immediately**
- QA: body ≤240 chars, ends with complete sentence, append " | @AITechWireIO"
- Posts 2–5 queued to `x_post_queue.json`

**Step 5: ARTICLE → aitechwire.io**
- Write HTML, run QA (`qa_site.py`), push to GitHub → Netlify auto-deploys
- Update `articles.json` + rebuild section index

**Step 6: REPORT → Telegram**
- Daily cost breakdown (AI tokens + X API + fixed)
- Article link, 5 story headlines
- Any errors

### Spread Posting Schedule (CDT)
| Time | Action |
|------|--------|
| 7:00 AM | Post #1 (pipeline) |
| 10:00 AM | Post #2 (queue cron) |
| 1:00 PM | Post #3 (queue cron) |
| 4:00 PM | Post #4 (queue cron) |
| 7:00 PM | Post #5 (queue cron) |

### Other Daily Jobs

#### X Reply Monitor (every 4h)
- Checks @AITechWireIO for new replies from real users
- Drafts a response for each using Claude (on-brand voice)
- Sends draft to Telegram for review
- **Purpose**: never leave a real reply unanswered; builds community
- **Script**: `scripts/x_reply_monitor.py`

#### X Reply Game (8 AM + 6 PM CDT = 4 replies/day)
- Fetches 10 recent public tweets from each target account via X API search
- Scores relevance against account topics (AI, crypto, macro, DeFi)
- Claude drafts a sharp, opinionated reply from @AITechWireIO
- Auto-posts if reply passes QA (complete sentence, ≤280 chars, no truncation)
- Posts to same tweet as a reply (visible to that account's followers)
- **Purpose**: get seen by @RaoulGMI / @saylor / @VitalikButerin followers → grow @AITechWireIO
- **Script**: `scripts/x_reply_game.py`
- **Rate limit**: max 3h between replies to same account; 2 replies per run

**Target accounts (reply game):**
| Handle | Name | Topics |
|--------|------|--------|
| @RaoulGMI | Raoul Pal | Macro, AI+crypto, Exponential Age |
| @saylor | Michael Saylor | Bitcoin, digital capital |
| @VitalikButerin | Vitalik Buterin | Ethereum, DeFi |
| @LynAldenContact | Lynn Alden | Monetary policy, debasement |
| @jerallaire | Jeremy Allaire | Stablecoins, USDC |
| @wagmiAlexander | Alexander | Aerodrome, DeFi, Base |
| @APompliano | Anthony Pompliano | Bitcoin, investing |
| @fundstrat | Tom Lee | Markets, stocks |
| @toly | Anatoly Yakovenko | Solana |
| @aixbt_agent | AIXBT | AI+crypto |

---

## 🏛️ Editorial Framework — What Gets Published

### Story Selection Criteria (Oleg's words)
> "News with large impact on the financial community — people talk about the topic a lot, or it's an important decision point for a large segment: crypto community, investors at large. I want stuff that makes smart investors stop scrolling."

**Publish if:**
- Relevant to 1+ of our 4 pillars
- High discussion velocity in target community on X
- Has clear financial/investment implication
- Specific enough to be useful (names, numbers, events — not vague)

**Do NOT publish if:**
- Vague or generic ("AI is growing fast")
- No financial angle
- Not verifiable / no real source
- **Hyperliquid / HYPE as primary subject** — excluded by editorial decision June 16. HYPE may be referenced as context within other stories but never as standalone article topic.

### Content Pillars
1. **AI & Tech** — OpenAI, Anthropic, NVIDIA, AI agents, infrastructure, enterprise adoption
2. **Finance & Investing** — Fed, rates, S&P/NASDAQ, macro, AI stocks, institutional flows
3. **Crypto, DeFi & Web3** — Bitcoin, Ethereum, DeFi (Aerodrome/AERO, Uniswap, Curve), stablecoins, on-chain data, L2s, TVL, protocol revenue
4. **Prediction Markets** — Polymarket, Kalshi, election odds, macro event probabilities, crowd vs analyst divergence

**PAUSED:** Real Estate — returns when rate cuts begin. No new real estate content until then.

### Opinion Leader Focus
The primary content strategy is **analysis of what opinion leaders say, write, and do** — not generic news.

| Leader | Handle | Focus |
|---|---|---|
| Michael Saylor | @saylor | MicroStrategy Exec Chairman — Bitcoin hard money thesis |
| Vitalik Buterin | @VitalikButerin | Ethereum co-founder — DeFi, crypto philosophy |
| Lyn Alden (Schwartzer) | @LynAldenContact | Macro analyst — monetary policy, currency debasement |
| Raoul Pal | @RaoulGMI | Real Vision CEO — Exponential Age, AI + Crypto macro |
| Jordi Visser | @jvisserlabs | 22V Research, Head of AI Macro Nexus |
| Anthony Scaramucci | @scaramucci | SkyBridge Capital founder — institutional crypto |
| Laurence "Larry" Fink | @LarryFink | BlackRock Chairman & CEO — ETF flows, institutional adoption |
| Alexander Cutler | @wagmiAlexander | Aerodrome Finance / Dromos Labs — DeFi, on-chain economy |
| Jeremy Allaire | @jerallaire | Circle co-founder & CEO — USDC, stablecoins |
| Ki Young Ju | @ki_young_ju | CryptoQuant founder & CEO — Bitcoin on-chain data, market cycles |

**Content angles:** Their latest thread → "What [Name] just said and why it matters". Their interview → key insight pulled, framed for our audience. Their contrarian take → we analyze the data behind it.

### Voice
Sharp. Opinionated. Forward-looking. Data-backed. Cite sources. No fluff. Not corporate.

### Post Style Rotation (5 types, one per daily post)
1. **ECCENTRIC** — unconventional/philosophical angle, makes reader stop and think
2. **CONTRARIAN** — surprising take backed by a specific named data point
3. **EDUCATIONAL** — Use EXACTLY: *"Let me break it down for you 👇"* as opener. Complex mechanism explained in plain language. For: Fed mechanics, DeFi yield, AI capex cycles, monetary debasement, crypto vs gold. ~1x/week max.
4. **SHARP ONE-LINER** — under 120 chars, one devastating observation
5. **IMPLICATION** — don’t report the news, tell the reader what it MEANS for their money

### Cross-Asset Comparison Rule — MANDATORY
At least **1 of 5 daily posts** MUST compare asset classes:
- Crypto vs Stocks (returns, risk, liquidity)
- Crypto vs Gold (store of value, portability, track record)
- Crypto vs Prediction Markets (what odds say vs what price says)
- AI Tech vs Crypto (infrastructure plays, where money flows)
- DeFi vs Traditional Finance (fees, speed, transparency)

**Why:** All-crypto feeds only attract crypto natives. Cross-asset comparisons attract the broader smart-investor audience we’re building.

### Content Quality Rules
- NO pure price action posts (“X up 18%”) — always add investment thesis
- Named data points required (“4.2% inflation” not “high inflation”)
- Thought leader references quote the IDEA, not just the person
- Every post must make a smart investor think, not just react

### Editorial Exclusions
- **HYPE/Hyperliquid** — excluded from all standalone articles and X posts. Context-only mention allowed.
- **Real Estate** — PAUSED. No new articles or posts until rate cuts begin.
- Any pure speculation story with no investment thesis

### Tagging Rules (X posts)
| Topic | Always tag |
|-------|------------|
| Aerodrome / AERO | @wagmiAlexander @DromosLabs |
| Hyperliquid / HYPE | @KookCapitalLLC |
| Bitcoin / Saylor thesis | @saylor |
| Macro / debasement | @LynAldenContact |
| Ethereum / DeFi | @VitalikButerin |

### Content QA Standard — NON-NEGOTIABLE (Oleg: "utmost importance")

**Every X post runs through `qa_x_post()` before posting. Failed posts are dropped, not fixed.**

| Check | Rule |
|---|---|
| Sentence | Complete, ends with . ! or ? |
| Length | ≤280 chars including handle |
| Handle | Must end with \| @AITechWireIO |
| Opener | No sycophantic starts (Appreciate, Great point, Thanks...) |
| Educational | MUST use exact phrase: "Let me break it down for you 👇" |
| Price action | If post mentions % move, must include WHY (investment thesis) |
| Numbers | Only from real research data — never fabricated |
| Substance | Minimum 40 chars of actual content |

**Batch check (`qa_post_batch()`) — every 5-post batch:**
- ≥1 cross-asset comparison post (crypto vs stocks/gold/AI/DeFi vs TradFi)
- Mix of 5 style types (eccentric, contrarian, educational, one-liner, implication)

---

### Article Promotion Rule — NON-NEGOTIABLE STANDARD

> **Every article published MUST have an OG image. No exceptions. A post without an image card is substandard and will not be published.**

**Automated pipeline sequence (hardcoded in `aitechwire_daily.py`):**
1. Article HTML written
2. `generate_og_image(headline, section, path, summary)` — 1200×630px, dark theme, pillar color
3. `add_og_tags_to_html()` — injects `og:image`, `og:image:width/height`, `twitter:image`
4. QA (`qa_site.py`) — hard stop if fails, Discord error alert fires
5. **Rebuild homepage** — `python3 ../scripts/build_index.py` — auto-regenerates index.html with newest article as hero
6. Deploy to GitHub — `GIT_TERMINAL_PROMPT=0 git push origin main`
7. `post_article_to_x_with_image()` — uploads image via v1.1, posts tweet with `media_ids`
8. Discord `#x-posts` notification

### Homepage Auto-Update System (Index Builder)

**New in June 2026:** All articles automatically appear on the homepage. No manual index editing.

**How it works:**
- Every article includes `<meta property="article:published_time" content="YYYY-MM-DD">` in the `<head>`
- Before deploy, run: `python3 ../scripts/build_index.py`
- Script scans all articles, sorts by date (newest first), regenerates `index.html`
- Hero section = latest article automatically
- Trending sidebar = top 4 newest articles
- Category sections = 2 latest per category

**For manual article posts:**
```bash
# After writing article, run before git push:
python3 /home/ubuntu/.openclaw/workspace/scripts/build_index.py

# Then:
cd /home/ubuntu/.openclaw/workspace/aitechwire
git add .
git commit -m "Publish: [article title]"
git push origin main
```

**Full deployment SOP:** see `/home/ubuntu/.openclaw/workspace/AITECHWIRE_DEPLOY_SOP.md`

**OG image spec:**
- Size: 1200×630px (Twitter `summary_large_image` standard)
- Background: #0a0a0f (matches site dark theme)
- Left accent bar: pillar color (purple/teal/gold/red)
- Fonts: Inter Bold (headline 64px), Inter Bold auto-sized (subtitle 22–36px)
- Subtitle: first sentence of article summary — article-specific, never generic tagline
- Footer: “⚡ AI TechWire” (gold) + “aitechwire.io” (muted)
- Generator: `scripts/og_image_generator.py` — zero API cost, runs in <1s

**X post with image standard:**
- Hook: key stat or contrarian angle — NOT a repeat of the headline
- Article link included
- Tag relevant accounts (see Tagging Rules)
- Image uploaded via `tweepy.API.media_upload()` — v1.1 endpoint
- `media_ids` passed to `create_tweet()` — v2 endpoint
- Fires IMMEDIATELY after deploy — separate from daily queue

**Why this matters:** X shows a grey placeholder without `og:image`. Image cards get 3–5x more engagement. This is the minimum viable standard for a professional media publication.

### Article Catalyst Rule
For any article covering a specific protocol (AERO, HYPE, etc.):
- **Always research upcoming catalysts on CT via Grok** before finalizing the article
- Include a dedicated “Upcoming Catalysts” section with specific, sourced items
- Cite the key CT accounts following that protocol
- Tag relevant builders/founders in the closing line

### Key Voices to Reference
- Raoul Pal (@RaoulGMI) — Exponential Age, AI + Crypto
- Lynn Alden (@LynAldenContact) — Currency debasement, monetary policy
- Michael Saylor (@saylor) — Bitcoin as hard money
- Vitalik Buterin (@VitalikButerin) — Ethereum, DeFi
- Jeremy Allaire (@jerallaire) — Stablecoins, Circle/USDC

---

## 💬 Discord — Command Center (TO BUILD)

### Channel Structure (agreed)
| Channel | Purpose |
|---------|---------|
| `#pipeline-log` | Every pipeline run: article link, cost, post count, errors |
| `#x-posts` | Every X post as it fires (with link) |
| `#research-feed` | Raw stories Grok found each morning + scores |
| `#errors-alerts` | Any pipeline failure, QA fail, push error — immediate |
| `#performance` | Weekly engagement summary (impressions, likes, top post) |
| `#memory-updates` | When MEMORY.md is updated — what changed and why |

**Status: Built 2026-06-17. Script: `scripts/editorial_preview.py`**

---

## 🔄 Learning & Feedback Loop

### How Lexie "learns" (no model retraining — this is prompt/criteria improvement)

**Weekly (Sunday AM cron — to build):**
1. Pull X analytics via API: impressions, likes, replies per post
2. Compare: which posts/styles/topics got most engagement
3. Write findings to `memory/performance-log.md`
4. Update scoring weights + writing criteria in pipeline

**Per session:**
- Write significant decisions, lessons, bugs to `memory/YYYY-MM-DD.md`
- Distill to `MEMORY.md` for long-term retention
- Update SOPs when processes change

**Knowledge lives in:**
- `MEMORY.md` — long-term curated memory
- `memory/YYYY-MM-DD.md` — daily raw logs
- `memory/performance-log.md` — engagement data (to create)
- `AITECHWIRE_SOP.md` — this file — process documentation
- Scripts themselves — prompt criteria embedded

**Discord** = visibility window only. Files = the actual brain.

---

## 💰 Cost Structure

| Item | Cost | Type |
|------|------|------|
| Claude Sonnet (writing) | ~$0.02/day | Variable |
| Grok 4.3 (research) | ~$0.04/day | Variable |
| X API (posting) | ~$0.04/day | Variable |
| X Premium | $8/mo | Fixed |
| Domain (aitechwire.io) | ~$0.08/day | Fixed |
| **Total estimate** | **~$0.18/day / ~$5.50/mo** | |

---

## 🚨 Failure Protocol

If pipeline errors:
1. Telegram failure alert fires immediately (configured on cron)
2. Check: `scripts/aitechwire_daily.log`
3. Fix, then manually trigger: `python3 /workspace/scripts/aitechwire_daily.py`
4. Never deploy to GitHub without QA passing: `python3 /workspace/scripts/qa_site.py`

---

## 🛠️ Key Files
| File | Purpose |
|------|---------|
| `scripts/aitechwire_daily.py` | Main pipeline |
| `scripts/research_engine.py` | Grok + X API + RSS research |
| `scripts/post_from_queue.py` | Spread posting (10AM/1PM/4PM/7PM) |
| `scripts/x_reply_game.py` | Proactive replies to grow followers |
| `scripts/x_reply_monitor.py` | Monitor + draft responses to mentions |
| `scripts/qa_site.py` | Pre-deploy QA |
| `scripts/x_post_queue.json` | Today's queued posts |
| `aitechwire/` | Site files (HTML, CSS, articles) |

---

## 📌 What's Next (Priority Order)
1. **Build Discord integration** — wire pipeline outputs to channels above
2. **Performance tracking** — pull X analytics weekly, log to `memory/performance-log.md`
3. **Weekly performance cron** — Sunday AM, update scoring weights
4. **6:50 AM editorial preview** — Telegram + Discord #research-feed preview of top 6 stories (`editorial_preview.py`)
5. **Beehiiv newsletter** — subscriber capture + automated sends
