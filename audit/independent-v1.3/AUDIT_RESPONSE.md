# Response to the independent v1.3 verification

The verification ([Caesar_Solo_v1.3_Verification.md](Caesar_Solo_v1.3_Verification.md)) reviewed commit `7c0d65c`. It confirmed that R06 and R07 are closed and found no new defects. It listed limits it could not cover itself. Two of them can be checked here, and both now have their own evidence in [`developer-checks/`](developer-checks). No game code, bot rules, card text or results changed.

## 1. Fresh Chrome rebuild of the PDFs

All seven PDFs of release `7c0d65c` were rebuilt from source, twice, in separate copies of `print/`. The build used Chrome for Testing 153.0.8010.12, the same Chrome major version as the shipped files (Skia/PDF m153). `compare_pdfs.py` compared each rebuild with the shipped files using `pdftotext -layout` and `pdftoppm` at 100 dpi, greyscale.

| Check | Result |
|---|---|
| Page counts | Equal for all 7 files, 55 pages in total |
| Extracted text, page by page | Identical on all 55 pages |
| Rendered pixels, page by page | Identical on all 55 pages |
| Bytes | The packet was identical. The other six differed only in Chrome's creation and modification dates, plus a temporary file name used as the cards PDF title. With those masked, the bytes and lengths were identical. |

Evidence: `developer-checks/pdf-rebuild-v1.3-build.json`.

**Two small print-build fixes came out of this.** Neither changes any page.

* **Cards PDF title.** The cards PDF's title was a temporary file name, such as `tmp_6hfg19b.html`, and the packet had no title. PDF viewers show this title in the window or tab. They are now "Caesar Solo Bots — Directive Cards" and "Caesar Solo Bots — Print and Play v1.3".
* **Reproducible builds.** `build.py` now writes fixed creation and modification dates (`PDF_DATE`, the release date) into every PDF. A rebuild from the same sources with the same Chrome is now byte-identical, so a future check can compare SHA-256 hashes directly. Two independent rebuilds matched byte for byte on all 7 files. Compared with the audited `7c0d65c` PDFs, all 55 pages still have identical text and identical rendered pixels. The PDF structure tree is kept. Evidence: `developer-checks/pdf-rebuild-fixed-dates.json`.

To repeat this, run `python3 print/build.py` in two copies of the repository and compare with `sha256sum print/*.pdf`. Different Chrome versions lay out text slightly differently, so byte identity holds only for the same Chrome build.

## 2. Real-browser run of the Directive helper

`helper_browser.py` loads the unmodified `print/Caesar_Solo_Deck.html` in headless Google Chrome through Playwright. The browser's own `localStorage` is used, with no DOM or storage doubles. **All 37 checks pass, with no page errors or console errors or warnings.** Evidence: `developer-checks/helper-browser.json` and three screenshots.

* **Deck cycle.** Nine draws show each Imperator Directive exactly once. The empty deck says it will reshuffle, and the tenth draw starts a fresh deck. Over 180 resets, every Directive appeared as the first card.
* **Saving.**
  * A page reload restores the exact saved state.
  * A full browser restart with a persistent profile restores the session and its Undo history from real storage.
  * When storage refuses writes, the page keeps working and shows the not-saving warning.
* **Counters, levels and bonuses.**
  * Imperator and Concilium keep separate play counters and decks.
  * All ten level choices are saved.
  * The +1 AP bonus appears on plays 1–4 only for Imperator L2 and Concilium L5, on every play for Imperator L3–5, and never for Imperator L1 or Concilium L1–4.
* **Turns and Undo.** Turn 6 disables Next turn. Undo goes back across five turns, with each turn's plays and history intact. Undo of a draw restores the deck.
* **Damaged data.** A damaged saved session starts a new game, shows the notice and keeps the damaged copy. Damaged Undo history is dropped with a notice, and the surviving snapshot still works. Dismiss hides the notice.
* **Keyboard.** Tab reaches the side buttons, level selector, Draw, Next turn and Reset. Enter and Space each draw a card.
* **Phone and motion.**
  * A 390 px phone viewport with touch has no horizontal overflow, the main buttons are at least 40 px tall, and tapping draws a card.
  * The card's flip animation ends flat and fully opaque.
  * With reduced motion requested, there is no animation.

## Still open, unchanged

* The exact 2nd-edition Siege Table and card AP assignments are not transcribed. The simulation approximates the first and assumes the second, as the release discloses. Both affect only the simulation numbers, not the paper bots, which read the components in front of them.
* There is no complete clean-room implementation of the latest rules text. The clean-room test covered an earlier version of the text.
* There has been no physical tabletop playtest. [PLAYTEST.md](../../PLAYTEST.md) asks for one.
