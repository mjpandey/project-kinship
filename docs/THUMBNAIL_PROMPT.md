# Project Thumbnail — Image Generation Guide

**Project:** Hey Mommy · Hello Dad (Project Kinship)  
**Use for:** YouTube capstone video, GitHub social preview, submission portal, Streamlit header

---

## Recommended dimensions

| Platform | Size | Aspect ratio |
|----------|------|--------------|
| YouTube thumbnail | 1280 × 720 | 16:9 |
| GitHub / general | 1280 × 640 | 2:1 |
| Square (social) | 1024 × 1024 | 1:1 |

---

## Primary image prompt (recommended)

Use this for DALL·E 3, Midjourney, Leonardo, or Ideogram:

```
Warm cinematic illustration for a tech capstone project thumbnail, 16:9 aspect ratio.
A cozy modern home at golden hour — soft amber window light, dinner table with pasta in the background slightly blurred.
In the foreground, a child (age 10–12, diverse, hopeful expression) holds a phone or tablet showing a gentle glowing orb of warm light shaped like a heart, with subtle friendly AI particle aura in soft pink and sky blue (not robotic, not scary).
Two translucent warm parental presences suggested as soft light silhouettes — one nurturing (motherly warmth, rose gold tones), one supportive (fatherly warmth, calm blue tones) — embracing the scene like digital presence, not replacing real parents.
Small subtle holographic UI elements float delicately: a calendar icon, a dinner plate icon, a shield icon, a home icon — representing AI agents working quietly in the background.
Mood: emotional, trustworthy, human-first AI, family connection, warmth, safety, love.
Style: premium editorial illustration, Pixar-adjacent warmth meets modern tech, soft gradients, no harsh neon, no dystopia, no uncanny faces.
Color palette: warm cream, soft coral, rose gold, gentle sky blue, honey amber.
Leave clear negative space in the upper third for title text overlay.
No logos, no watermarks, no readable text in the image itself.
Highly polished, submission-ready, 4K quality.
```

---

## Short prompt (DALL·E / fast models)

```
Cinematic warm family illustration, golden hour home interior, child smiling at glowing warm AI presence on phone — soft heart-shaped light, rose gold and sky blue, subtle agent icons (calendar, shield, home) floating gently. Two soft parental light silhouettes suggest Mommy and Daddy digital presence. Emotional, human-first AI, cozy, trustworthy. Upper area empty for text. Editorial illustration style, 16:9, no text, no robots, no dystopia.
```

---

## Midjourney prompt (with parameters)

```
Warm cinematic illustration, cozy home golden hour, child with tablet showing gentle glowing heart-shaped AI aura, soft rose gold motherly light and calm blue fatherly light silhouettes as digital parental presence, subtle floating icons calendar shield home representing multi-agent AI, emotional human-first technology, family warmth safety trust, premium editorial style, soft gradients --ar 16:9 --style raw --s 250 --no robot face text logo watermark dystopian neon cyberpunk
```

---

## Title text overlay (add in Canva / Figma after generation)

**Main title (large):**
```
Hey Mommy .... Hi Dad
```

**Subtitle (smaller):**
```
Multi-Agent AI · Digital Parental Presence
```

**Optional tagline:**
```
When life pulls you away, presence stays home.
```

### Typography suggestions

| Element | Font style | Color |
|---------|------------|-------|
| Main title | Rounded sans or soft serif (Nunito, Quicksand, Playfair) | White with soft shadow, or deep coral `#E91E63` |
| Subtitle | Light sans | Cream `#FFF8F0` or muted gray |
| Accent | — | Rose gold `#F8BBD0` · Sky blue `#BBDEFB` |

Place title in **upper third** where the prompt leaves negative space.

---

## Negative prompt (use if tool supports it)

```
robot, android, cyborg, scary AI, red eyes, dystopia, surveillance, cold blue hospital lighting, generic stock photo, clip art, low quality, blurry, watermark, logo, readable text, misspelled text, extra fingers, distorted faces, horror, dark thriller, military, guns, chains, prison bars, lonely empty room, elderly only, no child, neon cyberpunk, matrix code rain, overly technical circuit boards, blockchain, bitcoin
```

---

## Concept variants (pick one mood)

### Variant A — Emotional connection (recommended for capstone)
Emphasis: child + warm dual parental glow + phone/tablet  
Best for: Agents for Good track, empathy narrative

### Variant B — Home + agents
Emphasis: house cutaway, tiny agent icons orbiting (Persona, Safety, Logistics)  
Best for: technical judges who want architecture hint

### Variant C — Split moment
Emphasis: left = parent at work (soft blur), right = child at home with warm AI presence  
Best for: "bridge when parent is absent" story

**Variant A prompt snippet to swap in:**
```
Focus on emotional connection between child and warm dual parental digital presence, minimal tech chrome, maximum warmth and trust.
```

---

## Brand keywords (keep consistent)

- Digital **presence**, not replacement  
- **Warmth**, nicknames, family dinner  
- **Safety** without fear  
- **Multi-agent** as invisible helpers (icons, not robots)  
- **Mommy / Daddy** persona — rose gold + calm blue  

---

## Quick checklist before export

- [ ] Title readable at small size (YouTube mobile)
- [ ] No AI-generated gibberish text in image — add text in Canva
- [ ] Warm palette, not cold/sci-fi
- [ ] Child looks safe and hopeful, not anxious
- [ ] 16:9 crop with title safe zone clear
- [ ] Export PNG, sRGB, ≥1280px wide

---

## Generate with OpenAI (script)

```bash
source .venv/bin/activate
pip install openai python-dotenv   # if not already installed
python scripts/generate_thumbnail.py
python scripts/generate_thumbnail.py --variant short
python scripts/generate_thumbnail.py --size 1792x1024 --output assets/thumbnail.png
```

Requires `OPENAI_API_KEY` in `.env`.

**Per-demo story slides (deck):** [DEMO_THUMBNAIL_PROMPTS.md](./DEMO_THUMBNAIL_PROMPTS.md) — six-scene video order + one thumbnail per scenario with chit-chat overlay text.

---

*Project Kinship · Capstone submission asset*
