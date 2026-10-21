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

## Addendum (21.10.2026): Bricolage Grotesque variable and Noto Sans SC slices

Served unchanged as Google Fonts serves them (WOFF2 from fonts.gstatic.com, Bricolage Grotesque v9 with the full weight axis 200-800 and optical size 12-96; Noto Sans SC v41, weight axis 400-700), fetched once at build time and kept here, so that no visitor's browser contacts Google. Licence: SIL Open Font License 1.1 (OFL-BricolageGrotesque.txt, OFL-NotoSansSC.txt). Only the Noto Sans SC slices whose unicode-range covers a character of the Chinese texts of this site, the portal and Orbit 37 are kept (20 of 101); the Bricolage slices are latin, latin-ext and vietnamese. The earlier files bricolage-grotesque-latin.woff2 (weights 600-700) and noto-sans-sc-subset.woff2 are replaced.

| File | SHA-256 |
|---|---|
| bricolage-grotesque-latin-ext.woff2 | 776f6dcaf03636cd69a5802c94808cc8896c0a66c8e9ce0fe147231b6ee01957 |
| bricolage-grotesque-latin.woff2 | a79fdb52d4a5c76552452f69202add96e287401fff03d3e8c0e38b4dcb5a99cd |
| bricolage-grotesque-vietnamese.woff2 | b50a9d90a5264f20d1e45be0b948fe947ddb3644557f1e85ef5d3bd06427c944 |
| noto-sans-sc-cjk101.woff2 | a33308bf652e64ac2884bfe830996e933322b939b915bb823fd47383580664ad |
| noto-sans-sc-cjk102.woff2 | 4ea85e144cb385ce086b21b307730d3fdb70a587aaf350b12d0c4c2f13e66d27 |
| noto-sans-sc-cjk103.woff2 | 1bfdb1f001006c62434577b60064c3ec0562e4a68191acbc7feeba4b303bf095 |
| noto-sans-sc-cjk104.woff2 | 1e716b78655e396075808be52a9e749df1b6b5d17bd0ccedc6dcb89586903737 |
| noto-sans-sc-cjk105.woff2 | ade910a27a4bd65baed59a8a86a3a6a80f6083daa7123bb9ff32da15e56fda9d |
| noto-sans-sc-cjk106.woff2 | d31c838eb0e43043109bd6ddc23c295c340fc50f9a2f2381076ae8c0fa7f980b |
| noto-sans-sc-cjk107.woff2 | d8d9b5fd2b266fdf3f6855444e7769e54f39806e48994e7fe5e0c4ace9553c81 |
| noto-sans-sc-cjk108.woff2 | 12fcc1175cb6370acb056743f4fea7fdde85b6376ada2f15dfbab59f02b45988 |
| noto-sans-sc-cjk109.woff2 | 85ebc9985c665dd55346ebc78b93f8d8ef6ff972d78afc288b75d697a242d780 |
| noto-sans-sc-cjk110.woff2 | 51785f4a4d2a011d877052cab1bc4c36cabcc4e186ed0176214061c174b7f024 |
| noto-sans-sc-cjk111.woff2 | aaa67a70f5e8b351c558e32345093fdfd86f089726b3b86d84b58de6a2475104 |
| noto-sans-sc-cjk112.woff2 | 34e76675ceffd89824fb130d7649dc92df9e57843a73b9996d405baa2ff9ecff |
| noto-sans-sc-cjk113.woff2 | 40290d98d5c121bdbb1909e39c9c0242eae3a5a88f1bbe302857e525b90056df |
| noto-sans-sc-cjk114.woff2 | c49b2eb658a0c2d76de9a279945de30bf32acd8fdd6d56cf84aea9c6b14aacae |
| noto-sans-sc-cjk115.woff2 | 6c0cda055b31066fb60058ac30ede37f6f9ca02265c2e1a84aee81175f567fa8 |
| noto-sans-sc-cjk116.woff2 | 002e502515bee8b9efa1b17abf7e52b51d4cfa20538ae2b2bd82ac52e1153f5e |
| noto-sans-sc-cjk117.woff2 | 3d7ced7101c03dfa9bf0e60460a1b91fc6f1166fb33f718506e8110bb12e74a7 |
| noto-sans-sc-cjk118.woff2 | f26330ce4056382832c0f2a0d7f411e0b4140fc87937e8865d91664410cfb98c |
| noto-sans-sc-cjk119.woff2 | 09b9fa5a9521fbeccb8267a5abe7443c83cbe25b32eb15b00de316d913235525 |
| noto-sans-sc-cjk24.woff2 | fc59757db66129052cd8e4248045f92f8273b37f719be2a058a55859de190a0e |
