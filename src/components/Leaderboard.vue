<template>
  <main class="main_container">
    <section class="panel" role="region" aria-label="Weight classes">
      <div class="panel_header">
        <div class="chips" role="group" aria-label="Weight class">
          <button
            v-for="c in classes"
            :key="c"
            class="chip"
            :data-cls="c"
            :aria-pressed="String(selected_class === c)"
            @click="selectClass(c)"
          >
            {{ c }}
          </button>
        </div>
        <label class="opt">
          <input type="checkbox" v-model="combine_lower" />
          Combine with lower weight classes
        </label>
      </div>

      <div class="sub_bar">
        <span class="sub_pill">{{ sticky_prefix }}{{ sticky_label }}</span>
      </div>

      <div class="wrap">
        <table class="table">
          <thead>
            <tr>
              <th>Left</th>
              <th class="rank">#</th>
              <th>Right</th>
            </tr>
          </thead>
          <tbody ref="tbody_ref">
            <tr v-if="!loaded"><td colspan="3">Loading…</td></tr>
            <tr v-else-if="load_error"><td colspan="3">Failed to load Google Sheets data.</td></tr>

            <tr v-else v-for="(row, i) in first_rows" :key="'f'+i" :class="row.row_class">
              <td class="athlete">{{ row.left_name }}</td>
              <td class="rank">
                <span v-if="i < 3" class="trophy" :class="'trophy_' + (i+1)">
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/>
                  </svg>
                  <span class="trophy_num" aria-hidden="true">{{ i + 1 }}</span>
                </span>
                <span v-else>{{ i + 1 }}</span>
              </td>
              <td class="athlete">{{ row.right_name }}</td>
            </tr>
          </tbody>
        </table>

        <!-- toggle OUTSIDE the table to avoid mobile grid constraints -->
        <div
          v-if="is_collapsible"
          class="toggle_wrap"
          role="button"
          :aria-expanded="String(show_all)"
          aria-label="Toggle full list"
          @click="toggleShowAll"
        >
          <div class="show_more_button" :class="{ is_open: show_all }" aria-hidden="true">
            <svg class="toggle_icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>

        <!-- collapsed items OUTSIDE the table -->
        <div v-if="is_collapsible" class="collapse_wrap" :class="{ open: show_all }" ref="collapse_wrap_ref">
          <div class="rows_grid">
            <div class="row_grid" v-for="(row, j) in extra_rows" :key="'x'+j" :class="row.row_class">
              <div class="cell athlete">{{ row.left_name }}</div>
              <div class="cell rank">
                <span v-if="first_rows_count + j + 1 <= 3" class="trophy" :class="'trophy_' + (first_rows_count + j + 1)">
                  <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M19 3h-3V2H8v1H5a1 1 0 0 0-1 1v2a4 4 0 0 0 3 3.87A5 5 0 0 0 11 14v2H7v2h10v-2h-4v-2a5 5 0 0 0 4-4.13A4 4 0 0 0 20 6V4a1 1 0 0 0-1-1zm-1 3a2 2 0 0 1-2 2V5h2zm-12 0V5h2v3a2 2 0 0 1-2-2z"/>
                  </svg>
                  <span class="trophy_num" aria-hidden="true">{{ first_rows_count + j + 1 }}</span>
                </span>
                <span v-else>{{ first_rows_count + j + 1 }}</span>
              </div>
              <div class="cell athlete">{{ row.right_name }}</div>
            </div>
          </div>
        </div>
        
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: 'Leaderboard',
  props: {
    rankings_tab_name: { type: String, required: true },
    weights_tab_name: { type: String, required: true },
    classes: { type: Array, required: true },
    default_selected_class: { type: String, required: true },
    sticky_prefix: { type: String, default: '' },
    max_initial_rows: { type: Number, default: 10 },
  },
  data() {
    const sheet_id_raw = 'https://docs.google.com/spreadsheets/d/1aD3ZFkMHCrg4lZe80lONyQz-MsEVStelCiCEyHb6-2Y/edit?usp=sharing'
    const sheet_id_match = String(sheet_id_raw).match(/\/d\/([a-zA-Z0-9-_]+)/)
    const sheet_id = sheet_id_match ? sheet_id_match[1] : String(sheet_id_raw).trim()

    return {
      sheet_id_raw,
      sheet_id,

      selected_class: null,
      combine_lower: true,
      loaded: false,
      load_error: false,
      show_all: false,

      left_list_raw: [],
      right_list_raw: [],
      weight_map: new Map(),
    }
  },
  computed: {
    sticky_label() {
      const cls = this.selected_class || this.default_selected_class
      const base_top = this.classes[this.classes.length - 1]
      if (this.combine_lower && cls === base_top) {
        return 'Combined overall'
      }
      const plus_label = base_top && base_top.includes('+') ? `${base_top} lbs` : `${cls} lbs`
      const text = cls === base_top ? plus_label : `${cls} lbs`
      const extra = this.combine_lower && cls !== this.classes[0] ? ' + lower' : ''
      return `${text}${extra}`
    },
    classes_to_combine() {
      const i = this.classes.indexOf(this.selected_class)
      return this.classes.slice(0, i + 1)
    },
    left_groups() {
      const index = new Map(this.left_list_raw.map((name, i) => [name, i + 1]))
      const map = new Map(this.classes.map(c => [c, []]))
      this.left_list_raw.forEach(name => {
        const cls = this.weight_map.get(name) || this.classes[this.classes.length - 1]
        map.get(cls).push({ name, rank: index.get(name), cls })
      })
      this.classes.forEach(c => map.get(c).sort((a, b) => a.rank - b.rank))
      return map
    },
    right_groups() {
      const index = new Map(this.right_list_raw.map((name, i) => [name, i + 1]))
      const map = new Map(this.classes.map(c => [c, []]))
      this.right_list_raw.forEach(name => {
        const cls = this.weight_map.get(name) || this.classes[this.classes.length - 1]
        map.get(cls).push({ name, rank: index.get(name), cls })
      })
      this.classes.forEach(c => map.get(c).sort((a, b) => a.rank - b.rank))
      return map
    },
    left_list() {
      if (this.combine_lower) {
        return this.classes_to_combine
          .flatMap(c => this.left_groups.get(c) || [])
          .sort((a, b) => a.rank - b.rank)
      }
      return (this.left_groups.get(this.selected_class) || []).slice()
    },
    right_list() {
      if (this.combine_lower) {
        return this.classes_to_combine
          .flatMap(c => this.right_groups.get(c) || [])
          .sort((a, b) => a.rank - b.rank)
      }
      return (this.right_groups.get(this.selected_class) || []).slice()
    },
    rows() {
      const n = Math.max(this.left_list.length, this.right_list.length)
      const out = []
      for (let i = 0; i < n; i++) {
        const rank = i + 1
        const left_name = this.left_list[i]?.name || ''
        const right_name = this.right_list[i]?.name || ''
        let row_class = ''
        if (rank <= 3) {
          row_class = (rank === 1 ? 'top1' : rank === 2 ? 'top2' : 'top3')
        }
        out.push({ left_name, right_name, row_class })
      }
      return out
    },
    first_rows(){
      const limit = this.max_initial_rows
      return this.rows.slice(0, Math.min(limit, this.rows.length))
    },
    extra_rows(){
      const limit = this.max_initial_rows
      return this.rows.slice(limit)
    },
    is_collapsible(){
      return this.rows.length > this.max_initial_rows
    },
    first_rows_count(){
      return this.first_rows.length
    },
  },
  methods: {
    selectClass(cls) {
      this.selected_class = cls
    },
    toggleShowAll(){
      this.show_all = !this.show_all
    },
    gvizCsv(tab) {
      return `https://docs.google.com/spreadsheets/d/${this.sheet_id}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent(tab)}`
    },
    csvToRows(csv) {
      return csv
        .trim()
        .split(/\r?\n/)
        .map(line => {
          const out = []
          let cur = ''
          let q = false
          for (let i = 0; i < line.length; i++) {
            const ch = line[i]
            if (ch === '"') {
              q = !q
              continue
            }
            if (ch === ',' && !q) {
              out.push(cur)
              cur = ''
            } else {
              cur += ch
            }
          }
          out.push(cur)
          return out.map(s => s.trim())
        })
    },
    weightClass(lbs) {
      const top = this.classes[this.classes.length - 1]
      if (lbs === '' || lbs === null || Number.isNaN(Number(lbs))) return top
      const w = Number(lbs)
      if (w === -1) return top
      const thresholds = this.classes
        .filter(c => !c.includes('+'))
        .map(c => Number(c))
        .sort((a,b)=>a-b)
      for (const t of thresholds) {
        if (w <= t) return String(t)
      }
      return top
    },
    triggerSwapAnimation() {
      const el = this.$refs.tbody_ref
      if (!el) return
      el.classList.remove('swap')
      void el.offsetWidth
      el.classList.add('swap')
      el.addEventListener('animationend', () => el.classList.remove('swap'), { once: true })
    },
    async load() {
      try {
        const [rank_csv, wt_csv] = await Promise.all([
          fetch(this.gvizCsv(this.rankings_tab_name)).then(r => r.text()),
          fetch(this.gvizCsv(this.weights_tab_name)).then(r => r.text()),
        ])

        const r_rows = this.csvToRows(rank_csv)
        this.left_list_raw = r_rows.slice(1).map(r => r[0]).filter(Boolean)
        this.right_list_raw = r_rows.slice(1).map(r => r[2]).filter(Boolean)

        const w_rows = this.csvToRows(wt_csv)
        const map = new Map()
        w_rows.slice(1).forEach(r => {
          const name = (r[0] || '').trim()
          if (!name) return
          const lbs = r[1] !== undefined ? r[1] : ''
          map.set(name, this.weightClass(lbs))
        })
        this.weight_map = map

        this.loaded = true
        this.$nextTick(() => this.triggerSwapAnimation())
      } catch (e) {
        console.error(e)
        this.load_error = true
        this.loaded = true
      }
    },
  },
  created(){
    this.selected_class = this.default_selected_class
  },
  mounted() {
    this.load()
  },
  watch: {
    selected_class() {
      this.show_all = false
      this.$nextTick(() => this.triggerSwapAnimation())
    },
    combine_lower() {
      this.show_all = false
      this.$nextTick(() => this.triggerSwapAnimation())
    },
    rows() {
      this.$nextTick(() => this.triggerSwapAnimation())
    }
  },
}
</script>

<style scoped>
.main_container{width:min(1100px,100%);margin:0 auto;padding-inline:clamp(12px,3vw,24px);padding-block:24px}

.chips{display:flex;gap:6px;flex-wrap:wrap;margin:0}
.chip{border:1px solid var(--border);background:var(--panel);color:var(--muted);padding:6px 10px;border-radius:999px;font-weight:700;cursor:pointer;transition:.2s ease;line-height:1}
.chip:hover{color:var(--text)}
.chip[aria-pressed="true"]{color:#070e1c;background:linear-gradient(180deg,var(--accent),var(--accent-2));border-color:transparent;box-shadow:0 6px 18px rgba(215,180,58,.18)}

.opt{display:flex;align-items:center;gap:8px;color:var(--muted);font-weight:700}
.opt input{accent-color:var(--accent)}

.panel{background:linear-gradient(180deg, rgba(11,22,48,.94), rgba(8,18,40,.92));border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--glow);margin-top:18px;overflow:hidden}
.panel_header{display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;align-items:center;padding:14px 16px;border-bottom:1px solid var(--border)}
.sub_bar{position:sticky; top:0; z-index:5; background:var(--header-bg); border-bottom:1px solid var(--border); padding:10px 16px; display:flex; align-items:center; gap:12px}
.sub_pill{font-weight:800; border:1px solid rgba(215,180,58,.22); background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16)); color:var(--text); padding:6px 10px; border-radius:999px}
.wrap{overflow: visible !important; height: auto; max-height: none; margin-bottom:0; padding-bottom:0; -webkit-overflow-scrolling: auto; overscroll-behavior: auto; touch-action: auto}

.table{width:100%;max-width:100%;border-collapse:collapse;font-size:15px; table-layout:auto}
.table thead th{background:var(--header-bg);color:var(--muted);text-align:left;padding:10px 12px;border-bottom:1px solid var(--border)}
.table tbody td{padding:10px 12px;border-bottom:1px solid var(--border);min-width:0;word-break:break-word;background:transparent}
.table tbody tr:hover td{background:rgba(10,23,64,.35)}

/* perfectly centered # column with turquoise tint; remove any underlines */
th.rank, td.rank{width:64px; min-width:64px; text-align:center; vertical-align:middle}
td.rank{
  display:flex; align-items:center; justify-content:center;
  font-weight:900; color:var(--accent);
  background:linear-gradient(180deg, rgba(20,130,150,.18), rgba(12,100,120,.16)) !important;
  border-left:none !important; border-right:none !important;
  border-bottom:1px solid var(--border) !important;
  border-radius:6px;
  padding:10px 0 !important;
}
td.rank::before, td.rank::after, th.rank::before, th.rank::after{ content:none !important; display:none !important }

.athlete{min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap}

/* Smooth swap animation (disabled for show/hide) */
@keyframes fadeSlide { from{opacity:0; transform:translateY(6px)} to{opacity:1; transform:none} }
tbody.swap{ animation: fadeSlide .22s ease both }
@media(prefers-reduced-motion:reduce){ tbody.swap{ animation:none } }

/* Collapsing area for extra rows */
.collapse_cell{ padding:0 !important; background:transparent !important; border-bottom:none !important }
.collapse_wrap{ max-height:0; overflow:hidden; transition:max-height .28s ease; will-change:max-height }
.collapse_wrap.open{ max-height:2000px }
.rows_grid{ display:block; width:100% }
.row_grid{ display:grid; grid-template-columns:minmax(0,1fr) 64px minmax(0,1fr); align-items:center }
.row_grid .cell{ padding:10px 12px; border-bottom:1px solid var(--border) }
.row_grid .cell.rank{ display:flex; align-items:center; justify-content:center; font-weight:900; color:var(--accent); background:linear-gradient(180deg, rgba(20,130,150,.18), rgba(12,100,120,.16)) !important; border-left:none !important; border-right:none !important; border-bottom:1px solid var(--border) !important; border-radius:6px; padding:10px 0 !important }

/* Trophy SVG (bigger) with number overlay */
.trophy{ position:relative; display:inline-flex; align-items:center; justify-content:center; width:34px; height:34px; transform: translateY(4px) }
.trophy svg{ width:34px; height:34px; display:block }
.trophy_1 svg{ fill: var(--accent) }
.trophy_2 svg{ fill: var(--silver) }
.trophy_3 svg{ fill: var(--bronze) }

/* Show more row replacement (outside table) */
.toggle_wrap{ display:flex; align-items:center; justify-content:center; padding:8px 0; background:linear-gradient(180deg, rgba(20,130,150,.10), rgba(12,100,120,.08)); border-top:1px solid var(--border); border-bottom:1px solid var(--border); cursor:pointer; -webkit-tap-highlight-color: transparent }
.show_more_button{ display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; border:1px solid rgba(215,180,58,.22); background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16)); color:var(--text); font-weight:800; border-radius:999px; transition:.18s ease; pointer-events:none }
.show_more_button:hover{ filter:brightness(1.06) }
.toggle_icon{ transition: transform .18s ease }
.show_more_button.is_open .toggle_icon{ transform: rotate(180deg) }

/* Sticky bottom toggle when expanded */
.bottom_sticky{ position:sticky; bottom:0; display:flex; justify-content:center; padding:4px 0; background:linear-gradient(180deg, rgba(11,22,48,0), rgba(11,22,48,.78)); border-top:1px solid var(--border) }

/* Prevent bottom border from peeking at the end of the list */
.table tbody tr:last-child td{ border-bottom:none !important }
.rows_grid .row_grid:last-child .cell{ border-bottom:none !important }
.wrap{ position:relative }
.wrap::after{ content:""; position:absolute; left:0; right:0; bottom:-2px; height:6px; background:linear-gradient(180deg, rgba(11,22,48,0), rgba(11,22,48,1)); pointer-events:none }

/* Static tints for top 3 rows */
tbody tr.top1 td{ background:linear-gradient(180deg, rgba(215,180,58,.14), rgba(185,147,34,.12)) !important }
tbody tr.top2 td{ background:linear-gradient(180deg, rgba(192,192,192,.16), rgba(170,170,170,.12)) !important }
tbody tr.top3 td{ background:linear-gradient(180deg, rgba(205,127,50,.16), rgba(175,107,40,.12)) !important }
.row_grid.top1 .cell{ background:linear-gradient(180deg, rgba(215,180,58,.14), rgba(185,147,34,.12)) }
.row_grid.top2 .cell{ background:linear-gradient(180deg, rgba(192,192,192,.16), rgba(170,170,170,.12)) }
.row_grid.top3 .cell{ background:linear-gradient(180deg, rgba(205,127,50,.16), rgba(175,107,40,.12)) }

/* Mobile */
@media(max-width:760px){
  /* No table-row hacks required now; collapsed UI already outside table */
}

/* Nudge trophy number slightly downward and center */
.trophy_num{
  position:absolute;
  inset:0;
  display:flex;
  align-items:center;
  justify-content:center;
  font-weight:900;
  font-size:14px;
  color:#0b1630;
  text-shadow:0 1px 0 rgba(255,255,255,.45);
  transform: translateY(-7px);
  pointer-events:none;
}
/* Slight horizontal tweak for 2 and 3 */
.trophy_2 .trophy_num,
.trophy_3 .trophy_num{ transform: translate(1px, -7px) }
</style> 