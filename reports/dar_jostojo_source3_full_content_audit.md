# Dar Jostojo — full-content audit: Final-C vs 41-part site source

## Rules

- Final-C is read-only in this audit.
- The 41-part source is read-only.
- Whole supplemental files are copied only into `extracted/`; they are NOT merged into Final-C.
- Paragraph differences in mapped lessons are candidates, not automatic truth: formalized site wording and conversational Final-C wording can paraphrase the same idea.

## Inventory

- Final-C present: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30]
- Site source present: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 18, 20, 21, 22, 23, 25, 26, 27, 28, 30, 31, 32, 33, 35, 37, 38, 40, 41]
- Site downloads missing: [11, 13, 19, 24, 29, 34, 36, 39]
- Final-C lesson 21 present: False

## Whole files outside the current Final-C lesson set

- Site 1: 664 words → preserved whole as supplemental/unmatched.
- Site 2: 242 words → preserved whole as supplemental/unmatched.
- Site 3: 327 words → preserved whole as supplemental/unmatched.
- Site 4: 195 words → preserved whole as supplemental/unmatched.
- Site 5: 640 words → preserved whole as supplemental/unmatched.
- Site 6: 800 words → preserved whole as supplemental/unmatched.
- Site 7: 410 words → preserved whole as supplemental/unmatched.
- Site 8: 271 words → preserved whole as supplemental/unmatched.
- Site 9: 648 words → preserved whole as supplemental/unmatched.
- Site 10: 573 words → preserved whole as supplemental/unmatched.
- Site 26: 1932 words → preserved whole as supplemental/unmatched.

## Missing core lesson recovery

- Site 32 preserved separately as candidate Final-C 21 (1261 words).

## Mapped lesson full-content comparison

| Site | Final-C | site words | final words | size S/F | site likely-covered | final likely-covered | site candidate-extra words | result |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | 1 | — | 4208 | — | — | — | — | site file not downloaded |
| 12 | 2 | 2002 | 3975 | 0.50× | 51% | 20% | 93 | Final-C materially larger |
| 13 | 3 | — | 1823 | — | — | — | — | site file not downloaded |
| 14 | 4 | 1437 | 2594 | 0.55× | 60% | 25% | 71 | Final-C materially larger |
| 15 | 5 | 1714 | 3496 | 0.49× | 39% | 15% | 0 | Final-C materially larger |
| 16 | 6 | 1102 | 1918 | 0.57× | 85% | 28% | 0 | Final-C materially larger |
| 17 | 7 | 1143 | 2236 | 0.51× | 51% | 13% | 0 | Final-C materially larger |
| 18 | 8 | 1337 | 2886 | 0.46× | 43% | 16% | 100 | Final-C materially larger |
| 19 | 9 | — | 3327 | — | — | — | — | site file not downloaded |
| 20 | 10 | 1150 | 2649 | 0.43× | 56% | 19% | 63 | Final-C materially larger |
| 21 | 11 | 619 | 1161 | 0.53× | 77% | 25% | 0 | Final-C materially larger |
| 22 | 12 | 1178 | 2341 | 0.50× | 58% | 16% | 97 | Final-C materially larger |
| 23 | 13 | 1011 | 2557 | 0.40× | 46% | 11% | 113 | Final-C materially larger |
| 24 | 14 | — | 1799 | — | — | — | — | site file not downloaded |
| 25 | 15 | 1184 | 2740 | 0.43× | 28% | 8% | 171 | Final-C materially larger |
| 27 | 16 | 825 | 1320 | 0.62× | 45% | 18% | 64 | Final-C materially larger |
| 28 | 17 | 1548 | 3244 | 0.48× | 43% | 13% | 75 | Final-C materially larger |
| 29 | 18 | — | 3165 | — | — | — | — | site file not downloaded |
| 30 | 19 | 794 | 1404 | 0.57× | 54% | 35% | 0 | Final-C materially larger |
| 31 | 20 | 1289 | 3557 | 0.36× | 36% | 9% | 138 | Final-C materially larger |
| 32 | 21 | 1261 | — | — | — | — | whole file preserved | Final-C missing |
| 33 | 22 | 1155 | 2186 | 0.53× | 68% | 25% | 61 | Final-C materially larger |
| 34 | 23 | — | 1648 | — | — | — | — | site file not downloaded |
| 35 | 24 | 1230 | 2970 | 0.41× | 14% | 4% | 61 | Final-C materially larger |
| 36 | 25 | — | 3183 | — | — | — | — | site file not downloaded |
| 37 | 26 | 2042 | 4532 | 0.45× | 44% | 11% | 306 | Final-C materially larger |
| 38 | 27 | 1581 | 2586 | 0.61× | 55% | 31% | 105 | Final-C materially larger |
| 39 | 28 | — | 2836 | — | — | — | — | site file not downloaded |
| 40 | 29 | 1906 | 2668 | 0.71× | 93% | 56% | 33 | Final-C materially larger |
| 41 | 30 | 686 | 1100 | 0.62× | 80% | 49% | 43 | Final-C materially larger |

## Interpretation guardrails

- `site candidate-extra words` counts low-overlap paragraphs; it is a screening signal, not proof of unique knowledge.
- A site file smaller than Final-C is strong evidence that Final-C is not losing material at the gross-content level, but wording can still differ.
- Files 1–10 and 26 are intentionally preserved whole because they do not map cleanly to a current Final-C lesson.
- Site 32 is intentionally preserved whole as the missing lesson-21 recovery candidate.
- When the missing site files 11, 13, 19, 24, 29, 34, 36, 39 become available, rerun this audit to complete coverage.
