# HERPATH — Women's Symptom-to-Care Navigator
Women's symptom-to-care navigator: record symptoms, see how they change, and prepare for appointments.
HERPATH helps people record symptoms, see how they change, and prepare for conversations with healthcare professionals. It does **not** diagnose, score risk or give medical advice.

## Run it
No install, build step or internet connection is needed (plain HTML/CSS/JavaScript, no dependencies).
1. Extract the ZIP.
2. Double-click `index.html` (or serve the folder: `python3 -m http.server`, then open http://localhost:8000).

The project already *is* the static build: all charts, icons, illustrations and the PDF writer are bundled in `js/`. Nothing is loaded from a CDN.

## Journey
Landing page → **Get Started** → choose access (Continue Privately / Create local profile / Open local profile) → dashboard → features. Routes are hash based (`#/`, `#/start`, `#/app/<view>`), so refresh and back/forward work. `#/app/...` redirects to the access screen until a mode is chosen.

## Implemented features
- **Landing page:** sticky responsive nav (all links scroll to real sections), hero with custom SVG illustration, feature showcase with interactive previews (expandable timeline rows, hover chart tooltips, live Care Passport section toggles), 4-step journey, privacy & safety, Care Passport preview, clearly labelled *illustrative* scenarios (not testimonials), FAQ accordion, About, footer.
- **Header icons (landing + app):** profile popover (Sign In / Create Profile / Continue Privately, or profile info), notification popover, quick-settings popover (theme, text size).
- **Access:** private mode or a local profile (display name only), both saved on this device. No online accounts exist.
- **Dashboard:** sidebar (drawer + bottom navigation on mobile), search/quick navigation (pages, entries, articles), welcome, quick log, stats, timeline preview, severity chart, Care Passport card, recent activity, library shortcuts, first-visit empty state with *Add First Entry*.
- **Symptom Timeline:** month-grouped timeline, severity colours + labels, search, category/severity/date filters, expandable details, edit, delete (with confirmation), chart of the filtered entries.
- **Log a Symptom:** 5-step guided wizard (category → when → severity slider → context → review), validation, category-specific optional questions, save confirmation, edit flow.
- **Pattern Explorer:** date-range and category filters, frequency chart, severity trend, comparison with the previous period (only with ≥3 entries in each period, no significance claims), "based on N entries" captions, rule-based prompts with *Why am I seeing this?*, urgent-warning box.
- **Care Passport:** protected cover (passport ID, QR access code, security status) → passcode → the existing builder (section toggles, per-entry include/exclude, period selector, editable text, live preview, PDF, print). See *Care Passport & secure access* below.
- **Appointment Preparation:** select timeline entries, concerns, neutral question suggestions, summary (copy / PDF / add to Care Passport), plus after-visit notes.
- **Health Library:** search, categories, bookmarks, read progress, article dialogs with source links and an educational-use note.
- **Profile, Notifications, Settings:** display name; notification centre; a global **Settings dialog** (gear icon) for theme (Dark default / Light), language (English / हिन्दी) and text size; reduced motion; optional in-app reminder; data review, JSON export, clear local data.
- Accessible markup (labels, roles, focus rings, keyboard-operable popovers/cards, aria-live toasts), reduced-motion support, responsive layouts.

## Care Passport & secure access
Flow: **cover** (ID, QR, status) → *View Care Passport* → passcode (set on first use) → builder. Locks again after 10 minutes or when you leave the page.
- **QR code:** generated in-browser (`js/qr.js`). It encodes only a URL ending in a random 24-character token (`…#/access/<token>`). No names, entries, allergies or other health data are ever placed in the QR or URL. The token is not derived from any user ID.
- **Approval gate:** opening the link shows what *would* be shared and for how long. Nothing is displayed until the owner enters the passcode; approved views are read-only, limited to the sections selected in the builder, last 5, 15 or 60 minutes and end automatically (or via *End access*).
- **Revocation:** *Secure access → Replace code* issues a new token immediately; the old QR/link then reports "isn't valid".
- **Scanner:** *Scan a code* uses the camera only after you press *Start camera* (requires a browser with `BarcodeDetector`, e.g. Chrome/Edge; otherwise a message is shown). A paste-a-link fallback always works. States: invalid code, access not enabled, too many attempts (30 s lock-out), expired, approved.
- **Passcode storage:** salted PBKDF2-SHA-256 hash (150,000 iterations) via Web Crypto; on pages without Web Crypto (some `file://` contexts) a weaker fallback hash is used.

### Security model: please read
HERPATH has **no backend**. The passcode hash, access token and all entries sit in this browser's `localStorage`, which is not encrypted and can be read or reset by anyone who controls the browser profile (the *Forgot passcode?* path simply resets it). The passcode therefore deters casual viewing on a shared device; it is **not** genuine authentication, and the QR link only resolves in the browser that created it. Approval happens on the same device; there is no remote owner approval.
A production version would need: user accounts with real authentication (e.g. OIDC + MFA), server-side encrypted storage of records, server-issued single-use or time-limited share tokens with audit logs, owner approval delivered to the owner's own device, server-side revocation, and TLS.

## Honest limitations
- **Storage:** `localStorage` only (key `herpath_v1`), not encrypted, not synced, may be lost if browser data is cleared.
- **Health Library:** short plain-language summaries for general education. The interface makes no claim of clinical verification, because the text has not been clinically reviewed. Only one source page (NHS "Period pain") was located and checked; other entries link to organisation home pages. Have a clinician review the text and add exact source pages before wider release.
- **Pattern prompts** are simple rules and are not clinically validated.
- **Care Passport content** is limited to what the app collects (symptom entries, impact, notes, questions, visit notes). Blood group, allergies, medications, conditions, vaccinations and an emergency contact can be added by you under *Health details (optional)* in the builder. They are blank until you enter them, appear only when the *Health details* section is ticked, and are never placed in the QR code or access link.
- **Hindi** covers navigation, settings, Care Passport/access screens, landing headings, FAQ questions and common buttons. Long explanatory paragraphs, article text and user-entered data stay in English. The PDF uses Helvetica, so Hindi characters in a name or note print as `?`.
- Reminders only appear inside the app; no push or email notifications.
- Camera scanning needs a browser with `BarcodeDetector` and camera permission.

## Files
`index.html` · `css/styles.css` + `css/polish.css` (theme refinements, settings panel, passport) · `js/store.js` (state/storage) · `data.js` · `i18n.js` (Hindi dictionary + translation pass) · `ui.js` · `pdf.js` · `qr.js` (QR encoder) · `landing.js` · `views.js` · `passport.js` (passport cover, passcode, access gate, scanner) · `settings-panel.js` (settings dialog) · `app.js` (router/actions) · `data/*.json` (reference copies) · `tests/e2e.py`.

## Optional: run the automated test
`pip install playwright opencv-python-headless && playwright install chromium && python3 tests/e2e.py` (37 checks: theme/language persistence, passport flow, QR decoding, access states, mobile overflow, all views).

## Sample data (preloaded demonstration profile)
On the **first visit in a browser** HERPATH loads a fictional demonstration profile ("Aanya Rao") so every dashboard is populated immediately: 17 symptom entries over ~87 days (Timeline, Pattern Explorer, Overview, Appointment Preparation, Care Passport), 2 after-visit notes (one with an upcoming follow-up date), 4 notifications, drafted appointment questions, optional Care Passport health details, and library read/saved progress. All of it is fictional and is not real medical information. The existing app has no medication or prescription page, so none was added.
- **Source:** `data/sample-symptoms.json`, `sample-appointments.json`, `sample-notifications.json`, `sample-profile.json`. Dates are stored as "days ago" and resolved to real dates at first load, so the history always looks recent.
- **Why a .js file too:** browsers block `fetch()` of local JSON when a page is opened from `file://`. `data/seed-data.js` is a generated copy of the four JSON files, loaded by a normal script tag, so the site works by double-clicking `index.html` with no server. After editing any JSON, run `python3 tools/build-seed.py`.
- **Seeding rules:** runs once (flag `settings.seeded` in the existing `herpath_v1` storage); refreshes never duplicate or overwrite your changes; added, edited and deleted entries persist. If a browser already holds your own entries, nothing is added. "Clear local data" in Privacy & Settings removes everything including the samples and does not re-seed.
- **Reset to the sample data (testing):** open `index.html#/reset-sample` (or run `resetSampleData()` in the console). Theme, language and text size are kept. No reset control is shown in the normal interface.
- Charts, patterns, prompts and passport summaries are computed from these entries by the existing code; nothing is stored as pre-computed results.

## Illustrations
`js/art.js` holds custom inline SVG illustrations (Health Library categories, Appointment Preparation, Pattern Explorer). They follow the dark/light theme and need no network, so they cannot fail to load.
