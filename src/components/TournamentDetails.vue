<template>
  <div v-if="open" class="overlay" @click.self="$emit('close')" role="dialog" aria-modal="true" :aria-label="tournament?.name || 'Tournament details'">
    <div class="modal" ref="modal_ref">
      <div class="modal_header">
        <h2 class="modal_title">{{ tournament.name }}</h2>
        <div class="spacer"></div>
        <span v-if="tournament.pending_details" class="badge_outline">Pending</span>
        <span v-else class="badge_confirmed">Confirmed</span>
        <button class="close_btn" @click="$emit('close')" aria-label="Close">×</button>
      </div>

      <div class="hero">
        <div class="hero_img" :style="{ backgroundImage: `linear-gradient(180deg, rgba(0,0,0,.25), rgba(0,0,0,.55)), url('${tournament.image_url}')` }"></div>
        <div class="hero_meta">
          <div class="meta_item"><span class="label">Date</span><span>{{ tournament.date }}<span v-if="tournament.estimated" class="est"> (est)</span></span></div>
          <div class="meta_item" v-if="tournament.schedule_start"><span class="label">Start</span><span>{{ tournament.schedule_start }}<span v-if="tournament.estimated" class="est"> (est)</span></span></div>
          <div class="meta_item"><span class="label">Location</span><span>{{ tournament.location }}</span></div>
          <div class="meta_item" v-if="tournament.venue"><span class="label">Venue</span><span>{{ tournament.venue }}</span></div>
        </div>
      </div>

      <div class="grid">
        <!-- removed Featured section per request -->

        <section class="block" v-if="tournament.weigh_ins?.length">
          <h3>Weigh-ins</h3>
          <ul class="list">
            <li v-for="(wi, i) in tournament.weigh_ins" :key="i">{{ wi }}</li>
          </ul>
        </section>

        <section class="block" v-if="hasClasses">
          <h3>Weight Classes</h3>
          <div class="classes">
            <div v-if="tournament.men_classes">
              <div class="class_head">Men</div>
              <div class="class_body">{{ tournament.men_classes }}</div>
            </div>
            <div v-if="tournament.women_classes">
              <div class="class_head">Women</div>
              <div class="class_body">{{ tournament.women_classes }}</div>
            </div>
            <div v-if="tournament.masters_classes">
              <div class="class_head">Masters</div>
              <div class="class_body">{{ tournament.masters_classes }}</div>
            </div>
            <div v-if="tournament.kids_classes">
              <div class="class_head">Kids</div>
              <div class="class_body">{{ tournament.kids_classes }}</div>
            </div>
          </div>
          <div v-if="tournament.notes" class="fine_print">{{ tournament.notes }}</div>
        </section>

        <section class="block" v-if="tournament.entry_fees || tournament.spectator">
          <h3>Fees</h3>
          <div class="row" v-if="tournament.entry_fees"><span class="label">Entry</span><span>{{ tournament.entry_fees }}</span></div>
          <div class="row" v-if="tournament.spectator"><span class="label">Spectator</span><span>{{ tournament.spectator }}</span></div>
        </section>

        <section class="block" v-if="tournament.cash_prizes">
          <h3>Cash & Prizes</h3>
          <div class="row">{{ tournament.cash_prizes }}</div>
        </section>

        <section class="block" v-if="tournament.awards">
          <h3>Awards</h3>
          <div class="row">{{ tournament.awards }}</div>
        </section>

        <section class="block" v-if="tournament.benefiting">
          <h3>Benefiting</h3>
          <div class="row">{{ tournament.benefiting }}</div>
        </section>

        <section class="block" v-if="tournament.contacts?.length">
          <h3>Contacts</h3>
          <ul class="list">
            <li v-for="(c, i) in tournament.contacts" :key="i">{{ c }}</li>
          </ul>
        </section>
      </div>

      <div class="actions">
        <a v-if="tournament.link" class="primary_btn" :href="tournament.link" target="_blank" rel="noopener">View Event Website</a>
        <span v-else class="primary_btn disabled" aria-disabled="true">Event website pending</span>
        <button class="ghost_btn" @click="$emit('close')">Close</button>
      </div>

      <div v-if="tournament.pending_details" class="disclaimer">Tournament pending. Details are tentative and subject to change. Check back later for confirmation.</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TournamentDetails',
  props: {
    open: { type: Boolean, default: false },
    tournament: { type: Object, required: true },
  },
  computed:{
    hasClasses(){
      const t = this.tournament
      return !!(t.men_classes || t.women_classes || t.masters_classes || t.kids_classes)
    }
  }
}
</script>

<style scoped>
.overlay{position:fixed; inset:0; background:rgba(0,0,0,.6); display:flex; align-items:flex-start; justify-content:center; padding:16px; z-index:100; overflow:auto; -webkit-overflow-scrolling:touch}
.modal{width:min(860px,100%); background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.96)); border:1px solid var(--border); border-radius:16px; box-shadow:var(--glow); overflow:auto; max-height:calc(100vh - 32px)}
.modal_header{display:flex; align-items:center; justify-content:flex-start; gap:10px; padding:14px 16px; border-bottom:1px solid var(--border)}
.modal_title{margin:0}
.spacer{flex:1}
.badge_outline{font-weight:900; font-size:12px; padding:4px 8px; border-radius:999px; border:2px solid var(--accent); color:var(--text); background:transparent}
.badge_confirmed{font-weight:900; font-size:12px; padding:4px 8px; border-radius:999px; border:2px solid #2ecc71; color:var(--text); background:transparent}
.close_btn{background:transparent; color:var(--muted); border:1px solid var(--border); border-radius:8px; padding:4px 10px; cursor:pointer; font-size:22px; line-height:1}
.close_btn:hover{color:var(--text)}
.hero{display:grid; grid-template-columns:220px 1fr; gap:14px; padding:14px 16px; align-items:stretch}
.hero_img{border-radius:10px; background-size:cover; background-position:center; min-height:140px}
.hero_meta{display:flex; flex-direction:column; gap:8px}
.meta_item{display:flex; gap:10px}
.meta_item .label{color:var(--muted); min-width:70px; font-weight:700}
.est{color:var(--muted); font-weight:700}
.row{display:flex; gap:10px; align-items:center}
.row .label{color:var(--muted); min-width:70px; font-weight:700}
.grid{display:grid; grid-template-columns:repeat(auto-fit, minmax(260px,1fr)); gap:14px; padding:0 16px 16px}
.block{background:rgba(255,255,255,.02); border:1px solid var(--border); border-radius:12px; padding:12px}
.block h3{margin:0 0 8px 0}
.classes{display:grid; gap:10px}
.class_head{font-weight:800; color:var(--muted)}
.class_body{font-weight:600}
.fine_print{color:var(--muted); font-size:12px; margin-top:8px}
.list{margin:0; padding-left:18px}
.actions{display:flex; gap:10px; padding:12px 16px; border-top:1px solid var(--border); justify-content:flex-end}
.primary_btn{display:inline-flex; align-items:center; justify-content:center; padding:10px 14px; border-radius:999px; border:1px solid rgba(215,180,58,.22); background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16)); color:var(--text); font-weight:800; text-decoration:none}
.primary_btn.disabled{background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.08); color:var(--muted); cursor:not-allowed}
.ghost_btn{display:inline-flex; align-items:center; justify-content:center; padding:10px 14px; border-radius:999px; border:1px solid var(--border); color:var(--muted); background:transparent}
.disclaimer{padding:8px 16px 14px; font-size:12px; color:var(--accent); font-weight:800; border-top:1px dashed rgba(215,180,58,.35)}
@media(max-width:720px){
  .hero{grid-template-columns:1fr}
}
</style> 