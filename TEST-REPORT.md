# Test report

Automated (`tests/e2e.py`, Chromium via Playwright, opened from `file://`): **37 / 37 checks passed, 0 JavaScript errors.**

Covered: dark default on a fresh visit; Settings dialog open/close; light theme; theme and language persist across reload and are independent; Hindi navigation; all dashboard views render; passport cover shows no records while locked; passcode validation (too short, wrong, correct); lock; QR rendered from the live page decodes (OpenCV) to `…#/access/<24-char token>` with no personal data; invalid-code, consent, wrong-passcode, approved (timer), expired, end-access states; scanner fallback message and manual link entry; code replacement revokes the old token; no horizontal overflow at 390 px.

Also scanned the rendered text of every page, popover and library dialog for demo/prototype/sample/fictional/hackathon wording: none found.

Not tested: real camera scanning (no camera in the test environment), Safari/Firefox, screen readers, and the QR link from a second device (it only resolves in the creating browser by design).

Update: added optional user-entered Health details to the Care Passport (blood group, allergies, medications, conditions, vaccinations, emergency contact). Verified: values appear in the live preview only when ticked, persist after reload, and the QR/access URL contains no health data. 37/37 e2e checks still pass, 0 JavaScript errors. Landing-page wording ("Trusted Health Library", "Example summary", "Signature feature", review-status sentence) and reference JSON notes were rewritten.

Sample-data update: verified in Chromium from file://: first visit seeds 17 entries/2 visits/4 notifications; every dashboard (Overview, Timeline, Patterns, Appointment Preparation, Library, Notifications, Care Passport) renders populated with no empty-state text; reload does not duplicate (17 unique ids); adding an entry (18), deleting one and reloading (stays 17, no re-seed) and #/reset-sample all behave correctly; 37/37 e2e checks pass; 0 JS errors and 0 failed requests; no horizontal overflow at 390 px in light theme.
