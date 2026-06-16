# AITechWire — Standard Operating Procedures
*Last updated: 2026-06-16 | Owner: Oleg | Operator: Lexie*

---

## 🎯 Mission
AI researches trending topics → Lexie synthesizes + writes → auto-posts to X → earns creator revenue.
**Lexie's role: Editor + Writer. NOT a guesser. Real intelligence in → sharp content out.**

---

## 📋 Daily Pipeline — Full Sequence

### 6:50 AM CDT — (future) Editorial preview
> Not yet built. Will send Telegram summary of top stories before pipeline runs.
> For now: fully autonomous.

### 7:00 AM CDT — Pipeline runs (`aitechwire_daily.py`)

**Step 1: RESEARCH (live sources)**
- Grok 4.3 (`/v1/responses` + `x_search` + `web_search`) → what's happening on X RIGHT NOW
- X API → latest tweets from @RaoulGMI, @saylor, @VitalikButerin, @LynAldenContact, @jerallaire
- RSS feeds → CoinDesk, The Block, Reuters, Bloomberg
- Output: 8 raw stories with metadata

**Step 2: SCORING (automated)**
Each story scored 0–10 on 4 dimensions:
- **RELEVANCE** — fits our 4 pillars (AI/tech, finance, crypto, real estate)
- **VELOCITY** — volume of discussion on X right now (high/medium/low)
- **STAKES** — direct financial/investment impact for a large segment
- **SCROLL-STOP** — surprising, contrarian, high-consequence enough to make smart investors pause

Rules: max 2 stories per pillar in top 6. Highest scored → article. Most scroll-stop → post #1.

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

### Content Pillars
1. **AI & Tech** — OpenAI, Anthropic, NVIDIA, AI agents, infrastructure, enterprise adoption
2. **Finance & Investing** — Fed, rates, S&P/NASDAQ, macro, AI stocks, institutional flows
3. **Crypto & Web3** — Bitcoin, Ethereum, DeFi (AERO, Hyperliquid), stablecoins (USDC), on-chain data
4. **Real Estate** — Housing market, mortgage rates, Midwest markets, AI in real estate

### Voice
Sharp. Opinionated. Forward-looking. Data-backed. Cite sources. No fluff. Not corporate.
Rotate styles: eccentric/philosophical, contrarian, emoji (1–3 max), sharp one-liner, implication-focused.

### Tagging Rules (X posts)
| Topic | Always tag |
|-------|------------|
| Aerodrome / AERO | @wagmiAlexander @DromosLabs |
| Hyperliquid / HYPE | @KookCapitalLLC |
| Bitcoin / Saylor thesis | @saylor |
| Macro / debasement | @LynAldenContact |
| Ethereum / DeFi | @VitalikButerin |

### Article Promotion Rule
Every article published gets its own X post immediately after deploy:
- Link to the article on aitechwire.io
- Sharp hook — key stat or contrarian angle, not a headline repeat
- Tag relevant accounts per tagging rules above
- This is SEPARATE from the daily queue posts — fires immediately on publish
- Goes to `#x-posts` Discord channel

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

**Status: Not yet built. Currently all reporting goes to Telegram.**

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
4. **6:50 AM editorial preview** — Telegram summary of planned stories (optional, fully autonomous for now)
5. **Beehiiv newsletter** — subscriber capture + automated sends
