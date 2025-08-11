<template>
  <main class="main_container">
    <section id="view_weights" class="panel" role="region" aria-label="Weight classes">
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
        <span id="sticky_label" class="sub_pill">{{ sticky_label }}</span>
      </div>

      <div class="wrap">
        <table id="weights_table" class="table">
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
            <tr v-else v-for="(row, i) in rows" :key="i" :class="row.row_class">
              <td class="athlete">{{ row.left_name }}</td>
              <td class="rank">{{ i + 1 }}</td>
              <td class="athlete">{{ row.right_name }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: 'MainContent',
  data() {
    const sheet_id_raw = 'https://docs.google.com/spreadsheets/d/1aD3ZFkMHCrg4lZe80lONyQz-MsEVStelCiCEyHb6-2Y/edit?usp=sharing'
    const sheet_id_match = String(sheet_id_raw).match(/\/d\/([a-zA-Z0-9-_]+)/)
    const sheet_id = sheet_id_match ? sheet_id_match[1] : String(sheet_id_raw).trim()

    return {
      // config
      sheet_id_raw,
      sheet_id,
      rankings_tab_name: 'Rankings',
      weights_tab_name: 'Weights',

      // ui state
      selected_class: '243+',
      combine_lower: true,
      loaded: false,
      load_error: false,

      // data
      classes: ['154', '176', '198', '220', '242', '243+'],
      left_list_raw: [],
      right_list_raw: [],
      weight_map: new Map(),
    }
  },
  computed: {
    sticky_label() {
      const cls = this.selected_class || '243+'
      const extra = this.combine_lower && cls !== '154' ? ' + lower' : ''
      return `${cls === '243+' ? '243+ lbs' : cls + ' lbs'}${extra}`
    },
    classes_to_combine() {
      const i = this.classes.indexOf(this.selected_class)
      return this.classes.slice(0, i + 1)
    },
    left_groups() {
      const index = new Map(this.left_list_raw.map((name, i) => [name, i + 1]))
      const map = new Map(this.classes.map(c => [c, []]))
      this.left_list_raw.forEach(name => {
        const cls = this.weight_map.get(name) || '243+'
        map.get(cls).push({ name, rank: index.get(name), cls })
      })
      this.classes.forEach(c => map.get(c).sort((a, b) => a.rank - b.rank))
      return map
    },
    right_groups() {
      const index = new Map(this.right_list_raw.map((name, i) => [name, i + 1]))
      const map = new Map(this.classes.map(c => [c, []]))
      this.right_list_raw.forEach(name => {
        const cls = this.weight_map.get(name) || '243+'
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
          row_class = 'shimmer ' + (rank === 1 ? 'top1' : rank === 2 ? 'top2' : 'top3')
        }
        out.push({ left_name, right_name, row_class })
      }
      return out
    },
  },
  methods: {
    selectClass(cls) {
      this.selected_class = cls
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
      if (lbs === '' || lbs === null || Number.isNaN(Number(lbs))) return '243+'
      const w = Number(lbs)
      if (w === -1) return '243+'
      if (w <= 154) return '154'
      if (w <= 176) return '176'
      if (w <= 198) return '198'
      if (w <= 220) return '220'
      if (w <= 242) return '242'
      return '243+'
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
  mounted() {
    this.load()
  },
  watch: {
    selected_class() {
      this.$nextTick(() => this.triggerSwapAnimation())
    },
    combine_lower() {
      this.$nextTick(() => this.triggerSwapAnimation())
    },
    rows() {
      this.$nextTick(() => this.triggerSwapAnimation())
    },
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
.wrap{overflow-x:hidden; overflow-y:auto}

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

/* Smooth swap animation */
@keyframes fadeSlide { from{opacity:0; transform:translateY(6px)} to{opacity:1; transform:none} }
tbody.swap{ animation: fadeSlide .22s ease both }
@media(prefers-reduced-motion:reduce){ tbody.swap{ animation:none } }

/* Shimmer for top 3 across entire row */
@keyframes shimmer{ 0%{background-position:-200% 0} 100%{background-position:200% 0} }
tr.shimmer{ position:relative; overflow:hidden }
tr.shimmer::after{ content:""; position:absolute; inset:0; pointer-events:none; background-size:200% 100%; animation: shimmer 2.8s linear infinite }
tr.top1.shimmer::after{ background-image: linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(215,180,58,.16) 20%, rgba(0,0,0,0) 40%) }
tr.top2.shimmer::after{ background-image: linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(192,192,192,.16) 20%, rgba(0,0,0,0) 40%) }
tr.top3.shimmer::after{ background-image: linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(205,127,50,.16) 20%, rgba(0,0,0,0) 40%) }

/* Mobile */
@media(max-width:760px){
  .chips{gap:4px}
  .chip{padding:6px 8px; font-size:0.92rem}
  thead{display:none}
  .table, .table tbody, .table tr, .table td{display:block;width:100%}
  .table tbody tr{margin:8px;border:1px solid var(--border);border-radius:10px;overflow:hidden}
  .table tbody td{display:flex;justify-content:space-between;gap:10px}
  .table tbody td::before{display:none}
  .sub_bar{top:0}
  /* three-column grid: Left | # | Right */
  #weights_table tbody tr{display:grid; grid-template-columns:minmax(0,1fr) 64px minmax(0,1fr); align-items:center}
  #weights_table td{display:block; padding:10px 8px}
  #weights_table td.rank{padding:10px 0 !important; justify-content:center; border-radius:6px; background:linear-gradient(180deg, rgba(20,130,150,.18), rgba(12,100,120,.16)) !important}
}
</style> 