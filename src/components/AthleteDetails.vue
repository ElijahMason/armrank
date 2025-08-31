<template>
  <div v-if="open" class="overlay" @click.self="$emit('close')" role="dialog" aria-modal="true" :aria-label="athlete || 'Athlete details'">
    <div class="modal">
      <div class="modal_header">
        <h2 class="modal_title">{{ athlete }}</h2>
        <div class="spacer"></div>
        <button class="close_btn" @click="$emit('close')" aria-label="Close">×</button>
      </div>

      <div class="content">
        <div class="hero">
          <div class="stat">
            <div class="label">Skill Points</div>
            <div class="value"><span class="accent">{{ points }}</span></div>
          </div>
          <div class="stat">
            <div class="label">Division</div>
            <div class="value">{{ division }}</div>
          </div>
          <div class="stat">
            <div class="label">Weight Class</div>
            <div class="value">{{ weight }} lbs</div>
          </div>
          <div class="stat" v-if="club">
            <div class="label">Club</div>
            <div class="value">{{ club }}</div>
          </div>
        </div>

        <div class="grid">
          <section class="block">
            <h3>Overall Ranks</h3>
            <div class="rows">
              <div class="row"><span class="label">Right Hand</span><span class="val">{{ formatRank(rh_rank) }}</span></div>
              <div class="row"><span class="label">Left Hand</span><span class="val">{{ formatRank(lh_rank) }}</span></div>
            </div>
          </section>
          <section class="block">
            <h3>Highlights</h3>
            <ul class="list">
              <li v-if="isTopThree">Top 3 in current division</li>
              <li v-if="club">Leader or featured member of {{ club }}</li>
              <li>Active competitor in {{ division }} division</li>
            </ul>
          </section>
        </div>
      </div>

      <div class="actions">
        <button class="ghost_btn" @click="$emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AthleteDetails',
  props: {
    open: { type: Boolean, default: false },
    athlete: { type: String, default: '' },
    division: { type: String, default: '' },
    weight: { type: String, default: '' },
    rh_rank: { type: [String, Number], default: '' },
    lh_rank: { type: [String, Number], default: '' },
    club: { type: String, default: '' },
    points: { type: [String, Number], default: 48 },
  },
  computed: {
    isTopThree(){
      const r = Number(this.rh_rank)
      const l = Number(this.lh_rank)
      const vals = [r, l].filter(n => Number.isFinite(n) && n > 0)
      if(vals.length === 0) return false
      return Math.min(...vals) <= 3
    }
  },
  methods:{
    formatRank(r){
      if(r === '' || r === null || r === undefined) return '—'
      const n = Number(r)
      return Number.isFinite(n) && n > 0 ? `#${n}` : '—'
    }
  }
}
</script>

<style scoped>
.overlay{position:fixed; inset:0; background:rgba(0,0,0,.6); display:flex; align-items:flex-start; justify-content:center; padding:16px; z-index:100; overflow:auto; -webkit-overflow-scrolling:touch}
.modal{width:min(720px,100%); background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.96)); border:1px solid var(--border); border-radius:16px; box-shadow:var(--glow); overflow:auto; max-height:calc(100vh - 32px)}
.modal_header{display:flex; align-items:center; justify-content:flex-start; gap:10px; padding:14px 16px; border-bottom:1px solid var(--border)}
.modal_title{margin:0}
.spacer{flex:1}
.close_btn{background:transparent; color:var(--muted); border:1px solid var(--border); border-radius:8px; padding:4px 10px; cursor:pointer; font-size:22px; line-height:1}
.close_btn:hover{color:var(--text)}
.content{padding:12px 16px}
.hero{display:grid; grid-template-columns:repeat(auto-fit, minmax(140px,1fr)); gap:10px; margin-bottom:10px}
.stat{background:rgba(255,255,255,.04); border:1px solid var(--border); border-radius:10px; padding:10px}
.label{color:var(--muted); font-weight:700}
.value{font-weight:900}
.accent{color:var(--accent)}
.grid{display:grid; grid-template-columns:repeat(auto-fit, minmax(260px,1fr)); gap:14px}
.block{background:rgba(255,255,255,.02); border:1px solid var(--border); border-radius:12px; padding:12px}
.block h3{margin:0 0 8px 0}
.rows{display:flex; flex-direction:column; gap:8px}
.row{display:flex; gap:10px; align-items:center; justify-content:space-between}
.row .label{color:var(--muted); font-weight:700}
.list{margin:0; padding-left:18px}
.actions{display:flex; gap:10px; padding:12px 16px; border-top:1px solid var(--border); justify-content:flex-end}
.ghost_btn{display:inline-flex; align-items:center; justify-content:center; padding:10px 14px; border-radius:999px; border:1px solid var(--border); color:var(--muted); background:transparent}
</style>

