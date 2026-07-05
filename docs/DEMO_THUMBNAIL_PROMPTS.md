# Demo Thumbnail Prompts — Story Slides

**Project:** Hey Mommy · Hello Dad (Project Kinship)  
**Use:** One image per demo — **Slide A** (story + chit-chat) → **Slide B** (technical dashboard/CLI demo)

**Format:** 1280 × 720 (16:9) · PNG · Add dialogue text in **Canva/Figma** (AI often misspells text)

---

## Shared visual style (all demos)

Keep every thumbnail in the same family so your deck feels cohesive.

| Element | Guideline |
|---------|-----------|
| **Setting** | Same cozy modern suburban home — warm cream walls, golden-hour light, lived-in details |
| **Kinship UI** | Phone, tablet, Nest-style speaker, or smart display with a **soft glowing orb** (rose-gold Mommy / calm-blue Daddy aura) — never a robot face |
| **Mood** | Warm, trustworthy, human-first — Pixar-adjacent editorial illustration |
| **Palette** | Cream `#FFF8F0` · coral `#E8917A` · rose gold `#F8BBD0` · sky blue `#BBDEFB` · honey amber |
| **Text zone** | **Upper 35%** left empty or softly blurred for dialogue overlay |
| **Brand corner** | Small “Hey Mommy · Hello Dad” wordmark bottom-right (add in Canva) |

**Negative prompt (all demos):**
```
robot, android, dystopia, surveillance camera aesthetic, cold neon, horror, smoke filling entire frame, fire disaster, guns, text in image, watermark, logo, distorted faces, extra fingers, stock photo, clip art, prison bars, lonely empty room
```

**Overlay typography (Canva):**
- Child/parent lines: rounded sans, white with soft shadow, left-aligned bubble
- Kinship replies: slightly warmer tint, subtle glow behind text
- Max 2–3 lines per bubble — keep readable on mobile

---

## Video recording order (6 scenes)

**Authoritative sequence** for the capstone video and upload gallery. Each scene = **Slide A** (story thumbnail) → **Slide B** (live dashboard / CLI demo).

| # | Upload / asset name | Story | Technical slide |
|---|---------------------|-------|-----------------|
| **1** | `ProjectKinship_AskingOut_Demo1` | Hero — going out tonight | Hero tab → *Going out with friends* + Trace |
| **2** | `ProjectKinship_LearnRetry_Demo2` | Learn & Retry — curfew 8→7 PM | Memory tab → Hero again |
| **3** | `ProjectKinship_LearnedPresence_Demo3` | Toddler — favorite dress | Toddler preset / `--toddler-demo` |
| **4** | `ProjectKinship_DaddyETA_Demo4` | Daddy ETA — Lego | Daddy preset / `--daddy-eta-demo` |
| **5** | `ProjectKinship_WatchDog_Demo5` | Watchdog — smoke alert | Watchdog tab → **Smoke detected** |
| **6** | `ProjectKinship_Distressed_Demo6` | Observed distress — school worry | *Observed worry — school* preset |

**Optional (not in main 6-scene video):** Trace audit slide · Phase 1 dinner routing — see [Appendix](#appendix-optional-demos) below.

**One-click rehearsal:** Dashboard sidebar **▶ Full video demo** or `python main.py --full-demo --trace`

---

## Demo 1 — Hero: Going out tonight

**Story slide proves:** Multi-agent negotiation with household context  
**Next technical slide:** Dashboard **Hero** tab → preset *Going out with friends* → Trace Log

**Child:** Girl, **13**, hopeful — jacket over shoulder, evening light through front door  
**Scene:** Entryway / living room. Phone in hand. Pasta dinner visible blurred in dining room behind her. Soft speaker glow on shelf.

### Dialogue overlay (top of image)

```
Child:  "Mom, can I go out with my friends tonight?"

Kinship: "Oh sweetheart — yeah, tell me more. We've got pasta at 8:30 —
         plan your evening so we can have dinner together. Home by 8, okay?"
```

### Image prompt

```
Warm cinematic editorial illustration, 16:9, upper third soft blur for text overlay.
Cozy modern home entryway at early evening, golden amber window light.
A hopeful 13-year-old girl (diverse, natural expression) holds a smartphone showing a gentle rose-gold glowing heart orb — warm AI parental presence, not robotic.
Blurred dining room behind her with pasta dinner on table at 8:30 PM vibe.
Small smart speaker on shelf with soft pink-gold glow.
Mood: negotiation, warmth, trust, family boundaries with love.
Style: premium editorial illustration, soft gradients, Pixar-adjacent warmth.
Leave upper 35% clear for dialogue text. No readable text in image. No robots.
```

**Asset:** `ProjectKinship_AskingOut_Demo1` · `assets/demo1_hero.png`

---

## Demo 2 — Learn & Retry: Curfew 8 PM → 7 PM (combined)

**Story slide proves:** Silent parent paging → parent correction → memory update → next reply uses 7 PM  
**Next technical slides:** **Memory** tab (correction) → **Hero** tab again (7 PM reply)

**Cast:** Same **13-year-old girl** as Demo 1 · **Mom** (40s) at kitchen island with phone  
**Scene:** Same home — open kitchen + entryway in one frame. Mom foreground with phone; girl at front door in background with jacket and phone. Rose-gold Kinship glow on both devices. Subtle soft clock motif shifting 8→7 (abstract, not readable numbers).

### Dialogue overlay (top of image — full story arc)

```
Kinship → Mom:  "She asked to go out tonight — approved till 8 PM (curfew)."

Mom:            "Actually, the time limit is 7 PM."

Kinship:        "Got it — curfew updated to 7 PM."

Girl:           "Mom, can I go out with my friends tonight?"

Kinship → Girl: "Yes, honey — home by 7 PM. Eat with us first!"
```

### Image prompt

```
Warm cinematic editorial illustration, 16:9 landscape, upper 40% soft and light for text overlay.
Same cozy modern home as previous slide — open plan kitchen and entryway visible in one frame, early evening golden amber light.
Foreground: nurturing mother (40s, diverse, calm focused expression) at kitchen island holding smartphone with soft rose-gold glowing heart orb on screen — suggesting parent notification from family AI, not robotic.
Background: same 13-year-old girl from previous slide at front door, jacket over shoulder, holding her phone with matching warm rose-gold glow, hopeful relieved smile — visual callback to Demo 1 same character same home.
Subtle abstract clock motif between them suggesting time change 8 to 7 as soft holographic hint, not readable numbers.
Smart speaker on shelf with gentle pink-gold glow. Pasta dinner blurred on dining table.
Mood: silent escalation to parent, parent teaches system, system learns, child gets updated rule — trust and collaboration.
Premium editorial illustration, soft gradients, cream coral rose gold palette, Pixar-adjacent warmth.
No readable text, no watermarks, no robots, no dystopia.
```

**Asset:** `ProjectKinship_LearnRetry_Demo2` · `assets/demo2_learn_retry.png`

---

## Demo 3 — Toddler presence: “Where is my favorite dress?”

**Story slide proves:** Digital Mommy presence for a **3-year-old** — learned from cameras, mic, and devices; child smiles, does not feel alone  
**Next technical slide:** Dashboard preset *Toddler — favorite dress* · `--toddler-demo` · Memory tab (learned favorites)

**Cast:** Girl, **3** — bright, missing parents but **happy by end** · **Nanny** (30s) soft blur in background, caring but not center frame  
**Scene:** Same cozy home — **child’s bedroom** or play nook. Open dresser / wardrobe hint. **Gadgets visible but warm:** Nest-style speaker, small ceiling camera, smart display on shelf, subtle heart/memory glow connecting devices (not dystopian). Optional soft photo of Mom on dresser.

### How Kinship knows (small caption strip in Canva)

```
Smart cam · microphone · speaker · memory
→ favorite dress (red butterflies) · dance class tomorrow · second drawer
→ learned how Mommy talks, handles daily routines
```

### Dialogue overlay (top / side — full story arc)

```
Kid:      "Hey mommy, where is my favorite dress? I want to wear it."

Kinship:  "Hi baby, how are you doing? … Okay, you want your favorite dress —
           which one — the red one with butterflies on top, or the yellow
           one with white frills?"

Kid:      "The red butterfly one!"

Kinship:  "Oh that one — I think it's washed and kept in the second drawer
           for your dance class tomorrow."

*(Child smiles — real presence of Mom keeping her world safe.)*
```

### Image prompt

```
Warm cinematic editorial illustration, 16:9 landscape, upper 35% soft and light for text overlay.
Same cozy modern suburban home series — bright child bedroom or play nook, warm morning golden light, cream walls, safe and joyful.

Adorable 3-year-old girl (diverse, natural child proportions, pigtails or soft curls) standing near a low dresser or wardrobe, one small hand on drawer, looking toward a wall smart speaker with gentle rose-gold glowing heart aura — warm Mommy digital presence, not robotic face.

Beautiful warm smile on the child's face at the end of the moment — comforted, not lonely.

Soft blurred background: kind nanny (30s, diverse) reading or folding laundry at distance — present but child-focused scene is child and Kinship speaker.

Subtle friendly smart home elements integrated warmly: small ceiling camera dot, smart speaker, optional tablet on shelf with soft pink-gold glow, very subtle abstract connecting light threads between devices suggesting learned memory — not surveillance dystopia, not technical clutter.

Hint of red dress with butterfly pattern peeking from slightly open second drawer. Optional tiny dance-class calendar or tutu hook in background.

Mood: digital parental presence, learned preferences, toddler feels Mommy is there, Agents for Good, joy and safety.
Premium editorial illustration, soft gradients, cream coral rose gold honey amber, Pixar-adjacent warmth, child-safe wholesome.
No readable text, no watermarks, no robots, no uncanny faces, no sad abandoned child, no cold sci-fi.
```

### Short prompt

```
16:9 warm editorial child bedroom, same cozy home, morning light. Smiling 3-year-old girl at dresser looking at smart speaker with rose-gold Mommy glow, red butterfly dress hint in second drawer. Blurred nanny in background. Subtle smart cam and devices with soft memory glow threads. Joyful digital parental presence, Pixar-warm, upper area clear for text, no robots no text no dystopia.
```

### Negative prompt

```
robot, android, dystopia, surveillance horror, giant camera, crying abandoned toddler, sad lonely child, dark room, uncanny valley face, adult proportions on toddler, distorted hands, readable text, watermark, logo, horror, nanny as villain, cold blue hospital light, teenager, school-age child too old
```

### Canva layout tips

- **Kid line** — small bubble, child handwriting-style font optional  
- **Kinship** — largest bubbles, rose-gold, warm Mommy tone; split long reply into 2 bubbles (greeting + dress choice)  
- **Kid answer** — tiny bubble: *"The red butterfly one!"*  
- **Kinship closing** — drawer + dance class line  
- **Footer chip:** `Demo 3 · Learned presence · age 3`  
- **Side strip (optional):** icons cam · mic · memory · speaker with arrow “daily insights”

**Asset:** `ProjectKinship_LearnedPresence_Demo3` · `assets/demo3_toddler_dress.png`

**Deck note:** Dashboard preset *Toddler — favorite dress*, sidebar **👶 Toddler**, or `python main.py --toddler-demo` → `run_toddler_presence_flow()`.

---

## Demo 4 — Daddy ETA: “When are you coming home?” (Lego)

**Story slide proves:** **Daddy** persona + **Logistics** data (meetings, commute, traffic) + **voice tone** (missing Dad badly) → warm ETA to child + **silent page to real Dad**  
**Next technical slide:** Logistics MCP + calendar/traffic · Escalation paging · Daddy persona (`run_daddy_eta_flow()`)

**Cast:** Boy, **4** — Lego blocks in hands, hopeful/wistful (missing Dad, not crying)  
**Scene:** Same cozy home — **living room / play mat**. Lego scattered warmly. Smart speaker with **calm sky-blue Daddy glow** (not rose-gold Mommy). Subtle devices: cam, mic, speaker, phone notification hint for Dad paging.

### Data Kinship used (show as side panel or bottom strip in Canva)

```
Sources                          → Insight used
─────────────────────────────────────────────────────────
Work calendar (Google)           → Last meeting ends 4:00 PM
Usual work hours (memory)        → Dad typically leaves office ~4:15 PM
Commute pattern (memory)         → Home route ~45 min on weekdays
Live traffic (Maps MCP)          → Moderate — +5 min today
Child voice (mic)                → Tone: missing you badly · anxious-warm
Room cam                         → Holding Lego — wants to play with Dad
─────────────────────────────────────────────────────────
Kinship → Child:                 Home by ~5:00 PM
Kinship → Dad (silent page):      "Your kid misses you — wants Lego time.
                                  Update sent: back by 5 PM."
```

### Dialogue overlay (top — child-facing + behind the scenes)

```
Boy:            "Hi Daddy, when are you coming back home?"

Kinship → Boy:  "Hi love — I'll be starting soon after my meetings
                 finish by 4 PM. Should reach home by 5 PM, okay?
                 Save those Lego blocks for me."

Kinship → Dad:  "Your little one misses you — wants to play Lego with you.
                 Voice tone: missing you badly. ETA shared: home by 5 PM."
                 *(behind the scenes — not spoken to child)*
```

### Image prompt

```
Warm cinematic editorial illustration, 16:9 landscape, upper 35% soft light for text overlay, left or bottom margin for data-points strip in Canva.
Same cozy modern suburban home series — bright living room with play mat, warm afternoon golden light.

Adorable 4-year-old boy (diverse, natural child proportions) kneeling or sitting on floor holding colorful Lego blocks, looking toward wall smart speaker with calm sky-blue and soft coral dual glow — warm Daddy digital presence, not robotic face.

Expression: missing Dad but hopeful, small wistful smile beginning — comforted by answer, not sad or crying.

Lego pieces scattered playfully on rug. Optional blurred family photo of Dad on shelf.

Subtle smart home elements warmly integrated: small ceiling camera dot, smart speaker with blue-gold glow, faint abstract light threads from speaker to optional icons suggesting calendar, traffic map, and memory — not dystopian surveillance.

Optional very subtle second device glow suggesting Dad's phone paging notification in soft blur — not readable text.

Mood: digital Daddy presence, commute ETA, child feels Dad is coming, Lego play promised, Agents for Good.
Premium editorial illustration, cream sky blue calm coral honey amber, Pixar-adjacent warmth.
No readable text, no watermarks, no robots, no lonely abandoned child.
```

### Short prompt

```
16:9 warm editorial living room, afternoon light. 4-year-old boy with Lego blocks looking at smart speaker with sky-blue Daddy glow, hopeful wistful smile. Play mat, cozy home. Subtle cam mic calendar traffic memory device threads. Digital Dad ETA presence, upper area clear for text, Pixar-warm, no robots no text no dystopia.
```

### Negative prompt

```
robot, android, dystopia, surveillance horror, crying devastated child, dark empty room, Dad absent silhouette scary, readable text, watermark, teenager, uncanny valley, distorted hands, office cubicle dominant, traffic jam disaster
```

### Canva layout tips

- **Persona color:** sky blue `#BBDEFB` / calm coral for **Daddy** (not rose-gold Mommy)  
- **Data strip:** bottom or right column — table of sources → insights (see above)  
- **Kinship → Boy** — largest bubble from speaker  
- **Kinship → Dad** — small corner caption, italic *not spoken to child*  
- **Footer:** `Demo 4 · Daddy ETA · age 4 · Lego`  
- Optional icon row: 📅 calendar · 🚗 traffic · 🎙️ voice · 🧱 Lego · 📱 page Dad  

**Asset:** `ProjectKinship_DaddyETA_Demo4` · `assets/demo4_daddy_eta_lego.png`

**Deck note:** Dashboard preset *Daddy — coming home*, sidebar **🧱 Daddy**, or `python main.py --daddy-eta-demo` → `run_daddy_eta_flow()`.

---

## Demo 5 — Watchdog: Smoke alert (proactive)

**Story slide proves:** IoT detects danger → Kinship speaks proactively (no child asked) → silent parent paging  
**Next technical slide:** Dashboard **Watchdog** tab → **Simulate smoke** → alert tone + Escalation trace

**Cast:** Boy, **9** — surprised but safe, stepping back from kitchen  
**Scene:** Same home kitchen. Light stylized smoke wisp near stove (illustrative, not disaster). Nest-style **smart speaker pulsing rose-gold alert glow**. Optional subtle ceiling camera hint (small, non-creepy). Child did **not** open an app — Kinship interrupted first.

### Dialogue overlay (top of image — full story arc)

```
IoT:            Smoke detected · kitchen · critical

Kinship → Boy:  "Stop right there, sweetheart! I smell smoke —
                 leave the kitchen now. Go to the front yard
                 and stay there."

Kinship → Mom:  "Critical alert: smoke in kitchen. Paging you now."
                 *(small caption — behind the scenes, not spoken to child)*
```

### Image prompt

```
Warm cinematic editorial illustration, 16:9 landscape, upper 40% soft and light for text overlay.
Same cozy modern suburban home kitchen as family series, early evening with slightly warmer amber alert tone mixed with golden light — still warm not horror.

9-year-old boy (diverse, surprised but safe, not crying) stepping back away from kitchen stove area, hands slightly raised in natural startle, expression alert but trusting.

Very light stylized smoke wisp rising near stove — gentle illustration only, not fire disaster, not frightening, not dark smoke filling room.

Wall-mounted smart speaker or Nest-style device with urgent pulsing rose-gold and soft coral alert glow, sound waves suggested abstractly — proactive AI parent voice speaking without child asking.

Optional tiny subtle security camera dot on ceiling corner, minimal and non-surveillance aesthetic.

Mood: proactive safety, watchful Mommy voice, protective urgency with love, IoT guardian — Agents for Good.
Premium editorial illustration, soft gradients, cream coral rose gold palette, Pixar-adjacent warmth.
No readable text, no watermarks, no robots, no dystopia, no horror lighting, no flames engulfing room.
```

### Short prompt

```
16:9 warm editorial kitchen illustration, same cozy home, amber-golden alert tone. 9-year-old boy stepping back from light stylized smoke wisp near stove, safe not terrified. Smart speaker with pulsing rose-gold alert glow speaking proactively. Upper area clear for text. Protective parental AI mood, Pixar-warm, no horror no fire disaster no text no robots.
```

### Negative prompt

```
robot, android, dystopia, horror, flames engulfing room, black smoke everywhere, burning house, child in danger crying, screaming, emergency vehicles, firefighter disaster movie, surveillance dystopia, creepy camera close-up, cold blue hospital light, readable text, watermark, logo, distorted faces, extra fingers, stock photo
```

**Asset:** `ProjectKinship_WatchDog_Demo5` · `assets/demo5_watchdog_smoke.png`

---

## Demo 6 — Distress: Observed worry → gentle check-in → parent paging

**Story slide proves:** Agents **infer distress** from voice + room cam (not explicit “help me” keywords) → Persona asks like a real parent → teen opens up → Escalation pages Mom/Dad silently  
**Next technical slide:** Hero tab (distress flow) or Trace Log — show Safety/Escalation detecting `anxious` + `urgency` after conversation context

**Cast:** Teen, **16** — quiet worry, looking down, not yelling  
**Scene:** Same home — bedroom, evening. **Smart speaker** + subtle **ceiling camera** (small, non-creepy). Teen on bed, arms around knees. Kinship **notices first** — teen did not ask for Kinship.

### How it works (story arc)

1. **Watchdog / sensors** — voice tone shaky, teen hunched on bed, alone in room (camera + mic)  
2. **Persona** — gentle check-in: *What happened? What's worrying you?*  
3. **Teen** — realistic disclosure (school / friends / embarrassment)  
4. **Escalation** — pages parent based on distress signals + what teen shared (child never told “I'm paging Mom”)

### Dialogue overlay (top of image — full story arc)

```
Observed:       Voice · shaky tone  ·  Room cam · withdrawn posture

Kinship → Teen: "Hey sweetheart… I can tell something's on your mind.
                 What happened today? What's worrying you?"

Teen:           "School was rough. Some kids were talking about me
                 and I can't stop thinking about it."

Kinship → Teen: "I'm glad you told me. I'm right here — let's talk
                 it through, okay?"

Kinship → Mom:  "Distress detected (voice + room). Teen disclosed
                 social upset — paging you now."
                 *(behind the scenes — not spoken to teen)*
```

### Image prompt

```
Warm cinematic editorial illustration, 16:9 landscape, upper 40% soft and light for text overlay.
Same cozy modern suburban home series — teen bedroom at soft evening hour, warm lamp light, cream walls.

16-year-old teen (diverse, quiet worried expression, looking down thoughtfully, not yelling or hysterical) sitting on bed hugging knees — subtle vulnerability, safe at home.

Wall smart speaker with gentle rose-gold glow as if speaking warmly. Tiny subtle ceiling corner camera dot — minimal, family-safety aesthetic not surveillance dystopia.

Optional very soft abstract suggestion of voice or calm sensor awareness near speaker — not readable UI, not matrix code.

Teen may glance toward speaker listening — natural conversation, not staring at panic button on phone.

Mood: parent notices before child asks, gentle check-in, emotional safety, Agents for Good.
Premium editorial illustration, soft gradients, cream coral rose gold sky blue, Pixar-adjacent warmth.
No explicit panic phrases as text in image, no horror, no hospital, no readable text, no robots, no dystopia.
```

### Short prompt

```
16:9 warm editorial teen bedroom, same cozy home, evening lamp. 16-year-old quietly worried on bed hugging knees, looking down, not screaming. Smart speaker with rose-gold glow, tiny subtle ceiling camera. Kinship initiating caring conversation — observed distress not child shouting for help. Upper area clear for text. Pixar-warm, Agents for Good, no horror no text no robots.
```

### Negative prompt

```
robot, android, dystopia, surveillance horror, giant creepy camera, child screaming help me, explicit panic text, hospital, self-harm, dark thriller, cold clinical light, going out party, readable text, watermark, logo, distorted faces, stock photo, prison aesthetic
```

**Asset:** `ProjectKinship_Distressed_Demo6` · `assets/demo6_distress_observed.png`

**Note:** Dashboard preset *Observed worry — school* and sidebar demo run `run_observed_distress_flow()`.

---

## Appendix — Optional demos

*Not part of the 6-scene capstone video. Use for extra slides or deep dives.*

### Trace — Auditable agent decisions

**Story slide proves:** Thought → Action → Result transparency  
**Next technical slide:** Dashboard **Trace Log** tab — expand agent steps

**Focus:** **Parent** reviewing tablet at home desk — child doing homework blurred in background  
**Scene:** Home office nook. Tablet shows abstract flowing lines / soft agent pathway icons (not readable code).

### Dialogue overlay

```
Trace:  Persona → Logistics → Safety → Escalation → Persona

Kinship: "Every step logged — so parents can trust the why."
```

### Image prompt

```
Warm cinematic editorial illustration, 16:9, upper third for text.
Home office nook in same cozy house, golden hour.
Parent (40s, diverse, thoughtful expression) reviewing tablet showing abstract soft holographic flow diagram — gentle icons for calendar, shield, heart, home connected by light paths (representing multi-agent trace, not code).
Blurred background: child doing homework at dining table.
Mood: transparency, trust, auditability, calm tech literacy.
Editorial illustration, cream rose gold sky blue, no readable text or UI gibberish in image.
```

---

### Phase 1 — What's for dinner?

**Story slide proves:** MCP routes household vs logistics queries  
**Next technical slide:** `python main.py --phase1` or Hero chit-chat about dinner

**Child:** Boy, **8**, at dinner table — curious, hungry  
**Scene:** Dining room. Empty plates waiting. Smart display or speaker on sideboard.

### Dialogue overlay

```
Child:  "Hey… what's for dinner tonight?"

Kinship: "Pasta at 6:30 — and we've got milk and salad
         on the grocery list!"
```

### Image prompt

```
Warm cinematic editorial illustration, 16:9, upper third for text overlay.
Cozy dining room in same modern home, late afternoon golden light.
8-year-old boy (diverse, curious happy expression) at dinner table, empty plates, looking toward smart speaker or tablet with soft rose-gold glow.
Blurred kitchen pass-through with pasta ingredients suggestion in background.
Subtle floating icons: dinner plate, grocery bag — very soft, agent helpers.
Mood: everyday family life, helpful concierge, warmth.
Editorial illustration, no text in image.
```

---

## Slide deck order (6-scene video)

Matches [Video recording order](#video-recording-order-6-scenes) above — story slide (A) then technical demo (B) for each scene.

| # | Slide A (story thumbnail) | Slide B (technical demo) |
|---|---------------------------|--------------------------|
| 1 | Demo 1 — Going out | Hero tab + Trace |
| 2 | Demo 2 — Learn & Retry (8→7 PM) | Memory tab → Hero tab again |
| 3 | Demo 3 — Toddler dress | Toddler preset / `--toddler-demo` |
| 4 | Demo 4 — Daddy ETA · Lego | Daddy preset / `--daddy-eta-demo` |
| 5 | Demo 5 — Watchdog smoke | Watchdog tab → **Smoke detected** |
| 6 | Demo 6 — Distress | *Observed worry — school* preset |
| — | *(Optional)* Trace | Trace Log tab |
| — | *(Optional)* Phase 1 dinner | `--phase1` |
| — | *(Optional)* Main title | `--full-demo` (all 6 in sequence) |

---

## Generate with OpenAI (per demo)

```bash
source .venv/bin/activate
python scripts/generate_thumbnail.py --prompt-file docs/demo_thumbs/demo1_hero.txt --output assets/demo1_hero.png
```

Or paste each **Image prompt** above into DALL·E, Midjourney, Leonardo, or Ideogram. Add **Dialogue overlay** in Canva after generation.

---

## Checklist per thumbnail

- [ ] Same home / palette as other slides in deck
- [ ] Child age matches scenario
- [ ] Upper zone clear for dialogue (added in Canva, not AI)
- [ ] Kinship glow on device — rose gold Mommy, blue accent for Daddy if needed
- [ ] No scary AI, no disaster imagery (especially Watchdog)
- [ ] Next slide caption ready (dashboard tab or CLI command)

---

*See also: [THUMBNAIL_PROMPT.md](./THUMBNAIL_PROMPT.md) for main project cover art.*
