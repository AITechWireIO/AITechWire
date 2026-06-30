# Discord System Update — AITechWire Dynamic Index Builder

**Channel:** #needs-your-input / #pipeline-log  
**Date:** 2026-06-28  
**Topic:** System improvement — automated homepage article rotation

---

## 📢 Summary for Cowork

Lexie has implemented a **dynamic index builder system** for AITechWire that automatically rotates new articles on the homepage. This solves the problem of articles being published but not appearing on the front page.

**What changed:**
- ✅ New script: `build_index.py` (430 lines) — scans articles, sorts by date, regenerates homepage
- ✅ Before each deployment, run: `python3 scripts/build_index.py`
- ✅ Homepage now auto-populates:
  - Hero section = latest article
  - Trending sidebar = top 4 newest
  - Latest grid = 6 newest articles
  - Category sections = 2 per category (AI & Tech, Finance, Crypto & Web3, Prediction Markets)
- ✅ Live test passed: AERO article (June 28, 2026) auto-detected → featured as hero → live

**Files updated:**
- `/aitechwire/scripts/build_index.py` (NEW)
- `/aitechwire/AITECHWIRE_SOP.md` (updated deployment section)
- `/MEMORY.md` (documented system improvement)

**No breaking changes.** This is a pure improvement with zero downside:
- Old articles still accessible
- Category pages unchanged
- All metadata extraction automatic
- One-line deploy: `python3 scripts/build_index.py && git add . && git commit && git push`

---

## How It Works

### For Writers/Publishers:

1. Write article in `/articles/your-article.html`
2. Add date metadata to `<head>`:
   ```html
   <meta property="og:title" content="Your Title">
   <meta property="og:description" content="Excerpt">
   <meta property="article:published_time" content="2026-06-28">
   ```
3. Before pushing, run:
   ```bash
   python3 scripts/build_index.py
   ```
4. Deploy:
   ```bash
   git add . && git commit -m "Publish: Your Title" && git push origin main
   ```

**Result:** Article automatically becomes hero (if newest) or appears in relevant sections.

### Architecture

```
Article published (with date metadata)
         ↓
build_index.py scans all articles
         ↓
Extracts: title, excerpt, date, category
         ↓
Sorts by date (newest first)
         ↓
Regenerates index.html with:
  - Hero = article #1
  - Sidebar = articles #1–4
  - Latest grid = articles #1–6
  - Categories = 2 per section
         ↓
Homepage auto-rotates
```

No manual edits. Pure logic.

---

## What This Solves

**Before:**
- ❌ New articles sitting in `/articles/` with no homepage visibility
- ❌ Manual editing of `index.html` required
- ❌ Empty space on dashboard (articles existed but weren't visible)
- ❌ Hero section stayed outdated

**After:**
- ✅ All new articles auto-appear on homepage
- ✅ Homepage always shows latest first
- ✅ No manual index editing
- ✅ Category sections auto-populate
- ✅ Trending sidebar updates automatically

---

## Testing Results

**Live test (June 28, 2026):**
- Article: "AERO vs UNI: The DEX War Comes to Ethereum"
- Status: Published to `/articles/aerodrome-ethereum-l1-competition.html`
- Run: `python3 scripts/build_index.py`
- Output: Found 23 articles, AERO detected as June 28 (newest)
- Result: AERO featured as hero on aitechwire.io ✅

---

## Technical Details

**Script location:** `/home/ubuntu/.openclaw/workspace/aitechwire/scripts/build_index.py`

**Key functions:**
- `extract_meta(html_path)` — reads og:title, og:description, article:published_time from HTML
- `get_articles_by_dir()` — scans all article directories, extracts metadata, returns sorted list
- `render_card(article, card_type)` — generates HTML card (sidebar or full grid)
- `build_index_html(articles)` — generates complete index.html with all sections
- `main()` — orchestrates the full build

**Dependencies:** None (Python 3 stdlib only)

**Runtime:** <1 second for 23 articles

---

## Deployment Workflow (Updated)

**Old workflow (manual editing):**
```
Write article → Manually edit index.html → git push
```

**New workflow (automated):**
```
Write article → python3 scripts/build_index.py → git push
```

**Updated SOP:** See `/aitechwire/AITECHWIRE_SOP.md` section "Homepage Auto-Update System (Index Builder)"

---

## Questions for Cowork/Oleg

1. ✅ **Should we commit this to documentation?** (DONE — updated AITECHWIRE_SOP.md + MEMORY.md)
2. ✅ **Should this run automatically before each deploy?** (Can add to CI/pre-push hook if desired, but currently manual call is fine for visibility)
3. ✅ **Should older articles be archived/hidden?** (No — all articles remain searchable and in category pages; only hero/trending/latest sections rotate)

---

## Next Steps

- Monitor performance of auto-rotated articles
- Collect engagement data per rotation cycle
- Consider adding build step to automated deployment pipeline if publish frequency increases

---

**Implemented by:** Lexie  
**Approved by:** Oleg (request: 2026-06-28 16:45 UTC, "make sure it uses some logic and rotates in new articles on the front page")  
**Status:** ✅ LIVE & TESTED
