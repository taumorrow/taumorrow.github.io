# Sources of the fonts (loaded 21.10.2026, built with portal/build_fonts.py, fontTools 4.67.0 + brotli; the build is reproducible: two runs, same bytes)

Source: repository github.com/google/fonts at commit `47d54ca1ebb14fd864695f1d39dc734f39017c33` (the files Google Fonts serves; upstream repositories named in each OFL text).

| Built file | Source file (TTF, variable) | Version (name ID 5) | SHA-256 of the source | Size built | SHA-256 built |
|---|---|---|---|---|---|
| `bricolage-grotesque-latin.woff2` | https://raw.githubusercontent.com/google/fonts/47d54ca1ebb14fd864695f1d39dc734f39017c33/ofl/bricolagegrotesque/BricolageGrotesque%5Bopsz,wdth,wght%5D.ttf | 1.001 | `413e7357809ddd12fd80a96a8a396de0e401638d4acd3cb3e37532f0472ac682` | 80488 bytes | `9897cf1909a94bd0547b1e56c82eb3aff6ac3b95a306e76d64226a055ff25055` |
| `source-sans-3.woff2` | https://raw.githubusercontent.com/google/fonts/47d54ca1ebb14fd864695f1d39dc734f39017c33/ofl/sourcesans3/SourceSans3%5Bwght%5D.ttf | 3.052 | `042fe2cc0b933e328410d7acbd0aa6a1873dca5aef81875f4bc214b08825c7b9` | 169416 bytes | `707229357fb90c9c5da177826aac06c6da031f569a9a520bfa7fcca5cd03355a` |
| `jetbrains-mono-latin-cyrillic.woff2` | https://raw.githubusercontent.com/google/fonts/47d54ca1ebb14fd864695f1d39dc734f39017c33/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf | 2.211 | `48715a42ec242c21e9f02692891e147d022299a52e48d5e413e1a942193ffeda` | 37284 bytes | `266baf0fda61faa55506c062765ade9afc2c16172e4201a1f896d548b38b4de0` |
| `noto-sans-thai.woff2` | https://raw.githubusercontent.com/google/fonts/47d54ca1ebb14fd864695f1d39dc734f39017c33/ofl/notosansthai/NotoSansThai%5Bwdth,wght%5D.ttf | 2.002 | `5a1c559bb539583c8a1fd99d1c5b9491e5e14478c9cd2bd0970d5c3096cc9ef8` | 24528 bytes | `5a8536b67602a03e5ec71c761dc60923644fd7c32630da363d5f8fc2e47414cc` |
| `noto-sans-sc-subset.woff2` | https://raw.githubusercontent.com/google/fonts/47d54ca1ebb14fd864695f1d39dc734f39017c33/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf | 2.004 | `a3041811a78c361b1de50f953c805e0244951c21c5bd412f7232ef0d899af0da` | 223844 bytes | `23ab7f9651f879ce24ed77c8567473c13b52ae78e91ca55555c262b4a696e0fa` |

Noto Sans SC is cut to 625 characters (616 Han) found in: crates/games-portal/web/texts.js; tau-games web/texts.js, games/wheel/web/board.js, games/wheel/RULES.zh.md, web/template.html (state 21.10.2026) — plus ASCII and CJK/full-width punctuation. After a change of zh texts, run the build again (missing characters fall back to a system font).

Rebuild: `python3 portal/build_fonts.py <dir with the five TTF files> [~/dev/tau-games]` (needs `pip install fonttools brotli`).
