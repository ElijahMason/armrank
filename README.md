# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).

### Updating Clubs Data

- Edit `docs/clubs.json` directly on GitHub (or locally and push). The app loads this at runtime; no rebuild is required for changes to appear.
- Supported fields per club:
  - `name`, `city`, `region`, `leaders` (array), `verified` (bool), `image_url`, `training` (array), `out_of_state` (bool)
  - `members_count`, `avg_practice_size`
  - `leader_footer` (string OR object `{ "num": "4x", "tail": " World Champion" }`)
  - `city_medal_rank`, `medals_this_year`, `supermatches_hosted`
  - Footer overrides: `members_footer_accent`, `members_footer_tail`, `avg_practice_footer_accent`, `avg_practice_footer_tail`, `medals_footer_accent`, `medals_footer_tail`
- Example object:
```json
{
  "name": "Brute Squad",
  "city": "Portland",
  "region": "Portland Metro",
  "leaders": ["Mark Owen"],
  "verified": true,
  "image_url": "https://...",
  "training": ["Weekly practice"],
  "members_count": 80,
  "avg_practice_size": 17,
  "leader_footer": { "num": "4x", "tail": " World Champion" },
  "city_medal_rank": 1,
  "medals_this_year": 159,
  "supermatches_hosted": 13,
  "members_footer_accent": "+53%",
  "members_footer_tail": " than state average",
  "avg_practice_footer_accent": "+24%",
  "avg_practice_footer_tail": " from last year",
  "medals_footer_accent": "#1",
  "medals_footer_tail": " in the state"
}
```
- Notes:
  - The app first tries `docs/clubs.json` and falls back to `clubs.json` (same folder) if needed.
  - Builds won’t clear `docs/` (configured), so `docs/clubs.json` persists across deploys.
