<template>
  <div v-if="open" class="overlay" @click.self="$emit('close')" @wheel="onOverlayWheel" @touchmove="onOverlayTouchMove" role="dialog" aria-modal="true" :aria-label="tournament?.name || 'Tournament details'">
    <div class="modal" ref="modal_ref">
      <div class="modal_header">
        <h2 class="modal_title">{{ tournament.name }}</h2>
        <div class="spacer"></div>
        <button v-if="dev && !edit_mode" class="icon_btn" @click="startEdit" aria-label="Edit">
          <svg viewBox="0 0 24 24" class="icon"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zm2.92 2.33H5v-.92l9.06-9.06.92.92L5.92 19.58zM20.71 7.04a1.003 1.003 0 0 0 0-1.42l-2.34-2.34a1.003 1.003 0 0 0-1.42 0l-1.83 1.83 3.75 3.75 1.84-1.82z"/></svg>
        </button>
        <span v-if="tournament.pending_details" class="badge_outline">Pending</span>
        <span v-else class="badge_confirmed">Confirmed</span>
        <button class="close_btn" @click="$emit('close')" aria-label="Close">×</button>
      </div>

      <div class="scroll_area">
      <div class="content" v-if="!edit_mode">
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
      </div>

      <div v-if="edit_mode" class="edit_panel">
        <div class="edit_grid">
          <label class="edit_field span2">
            <span class="ef_label">Name</span>
            <input v-model="draft.name" class="ef_input" />
          </label>
          <label class="edit_field">
            <span class="ef_label">Date</span>
            <input v-model="draft.date" class="ef_input" placeholder="YYYY-MM-DD" />
          </label>
          <label class="edit_field checkbox">
            <input type="checkbox" v-model="draft.estimated" />
            <span>Estimated date</span>
          </label>
          <label class="edit_field">
            <span class="ef_label">Start time</span>
            <input v-model="draft.schedule_start" class="ef_input" placeholder="e.g., 10:00am" />
          </label>
          <label class="edit_field">
            <span class="ef_label">Location</span>
            <input v-model="draft.location" class="ef_input" />
          </label>
          <label class="edit_field">
            <span class="ef_label">Venue</span>
            <input v-model="draft.venue" class="ef_input" />
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Weigh-ins (one per line)</span>
            <textarea v-model="weighInsText" class="ef_textarea auto_grow" rows="2"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Men classes</span>
            <textarea v-model="draft.men_classes" class="ef_textarea auto_grow" rows="1"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Women classes</span>
            <textarea v-model="draft.women_classes" class="ef_textarea auto_grow" rows="1"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Masters classes</span>
            <textarea v-model="draft.masters_classes" class="ef_textarea auto_grow" rows="1"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Kids classes</span>
            <textarea v-model="draft.kids_classes" class="ef_textarea auto_grow" rows="1"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Notes</span>
            <textarea v-model="draft.notes" class="ef_textarea auto_grow" rows="2"></textarea>
          </label>
          <label class="edit_field">
            <span class="ef_label">Entry fees</span>
            <textarea v-model="draft.entry_fees" class="ef_textarea auto_grow" rows="1"></textarea>
          </label>
          <label class="edit_field">
            <span class="ef_label">Spectator</span>
            <textarea v-model="draft.spectator" class="ef_textarea auto_grow" rows="1"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Cash & prizes</span>
            <textarea v-model="draft.cash_prizes" class="ef_textarea auto_grow" rows="1"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Awards</span>
            <textarea v-model="draft.awards" class="ef_textarea auto_grow" rows="1"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Benefiting</span>
            <textarea v-model="draft.benefiting" class="ef_textarea auto_grow" rows="1"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Contacts (one per line)</span>
            <textarea v-model="contactsText" class="ef_textarea auto_grow" rows="2"></textarea>
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Event website</span>
            <input v-model="draft.link" class="ef_input" />
          </label>
          <label class="edit_field span2">
            <span class="ef_label">Image URL</span>
            <input v-model="draft.image_url" class="ef_input" />
          </label>
        </div>
      </div>

      </div>

      <div class="actions">
        <div v-if="edit_mode" class="edit_actions">
          <button class="ghost_btn" @click="discardEdit">Discard</button>
          <button class="primary_btn" @click="saveEdit">Save</button>
        </div>
        <template v-else>
          <a v-if="tournament.link" class="primary_btn" :href="tournament.link" target="_blank" rel="noopener">View Event Website</a>
          <span v-else class="primary_btn disabled" aria-disabled="true">Event website pending</span>
          <button class="ghost_btn" @click="$emit('close')">Close</button>
        </template>
      </div>

      <div v-if="tournament.pending_details" class="disclaimer">Tournament pending. Details are tentative and subject to change. Check back later for confirmation.</div>
    </div>
  </div>
</template>

<script>
import { isDevMode } from '../utils/devMode'
export default {
  name: 'TournamentDetails',
  props: {
    open: { type: Boolean, default: false },
    tournament: { type: Object, required: true },
  },
  data(){
    return { dev:false, edit_mode:false, draft:null }
  },
  methods:{
    onOverlayWheel(evt){ try{ if(evt && evt.target === evt.currentTarget) evt.preventDefault() }catch{} },
    onOverlayTouchMove(evt){ try{ if(evt && evt.target === evt.currentTarget) evt.preventDefault() }catch{} },
    startEdit(){ this.edit_mode = true; this.draft = this.makeDraftFromTournament() },
    discardEdit(){ this.edit_mode = false; this.draft = this.makeDraftFromTournament() },
    saveEdit(){
      const d = this.draft || {}
      const t = this.tournament
      t.name = d.name
      t.date = d.date
      t.estimated = !!d.estimated
      t.schedule_start = d.schedule_start
      t.location = d.location
      t.venue = d.venue
      t.weigh_ins = Array.isArray(d.weigh_ins) ? d.weigh_ins.slice() : []
      t.men_classes = d.men_classes
      t.women_classes = d.women_classes
      t.masters_classes = d.masters_classes
      t.kids_classes = d.kids_classes
      t.notes = d.notes
      t.entry_fees = d.entry_fees
      t.spectator = d.spectator
      t.cash_prizes = d.cash_prizes
      t.awards = d.awards
      t.benefiting = d.benefiting
      t.contacts = Array.isArray(d.contacts) ? d.contacts.slice() : []
      t.link = d.link
      t.image_url = d.image_url
      this.edit_mode = false
    },
    makeDraftFromTournament(){
      const t = this.tournament || {}
      return {
        name: t.name || '',
        date: t.date || '',
        estimated: !!t.estimated,
        schedule_start: t.schedule_start || '',
        location: t.location || '',
        venue: t.venue || '',
        weigh_ins: Array.isArray(t.weigh_ins) ? t.weigh_ins.slice() : [],
        men_classes: t.men_classes || '',
        women_classes: t.women_classes || '',
        masters_classes: t.masters_classes || '',
        kids_classes: t.kids_classes || '',
        notes: t.notes || '',
        entry_fees: t.entry_fees || '',
        spectator: t.spectator || '',
        cash_prizes: t.cash_prizes || '',
        awards: t.awards || '',
        benefiting: t.benefiting || '',
        contacts: Array.isArray(t.contacts) ? t.contacts.slice() : [],
        link: t.link || '',
        image_url: t.image_url || '',
      }
    },
  },
  watch:{
    open(val){
      try{ const body = document && document.body; if(body){ body.style.overflow = val ? 'hidden' : '' } }catch{}
      if(val){ try{ this.dev = isDevMode() }catch{}; this.draft = this.makeDraftFromTournament() }
    }
  },
  computed:{
    hasClasses(){
      const t = this.tournament
      return !!(t.men_classes || t.women_classes || t.masters_classes || t.kids_classes)
    },
    weighInsText:{
      get(){ return Array.isArray(this.draft?.weigh_ins) ? this.draft.weigh_ins.join('\n') : '' },
      set(v){ if(!this.draft) this.draft = this.makeDraftFromTournament(); this.draft.weigh_ins = String(v||'').split(/\n/).map(s=>s.trim()).filter(Boolean) }
    },
    contactsText:{
      get(){ return Array.isArray(this.draft?.contacts) ? this.draft.contacts.join('\n') : '' },
      set(v){ if(!this.draft) this.draft = this.makeDraftFromTournament(); this.draft.contacts = String(v||'').split(/\n/).map(s=>s.trim()).filter(Boolean) }
    }
  }
}
</script>

<style scoped>
.overlay{position:fixed; inset:0; background:rgba(0,0,0,.6); display:flex; align-items:flex-start; justify-content:center; --ovPad:12px; padding:var(--ovPad); z-index:100; overflow:hidden}
.modal{width:100%; max-width:min(860px, calc(100vw - (var(--ovPad) * 2))); background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.96)); border:1px solid var(--border); border-radius:16px; box-shadow:var(--glow); display:flex; flex-direction:column; overflow:hidden; max-height:calc(100dvh - (var(--ovPad) * 2))}
.scroll_area{flex:1; overflow:auto; -webkit-overflow-scrolling:touch}
.content{padding:0 16px 0 16px}
.content{ scrollbar-width: none; -ms-overflow-style: none }
.content::-webkit-scrollbar{ width:0; height:0 }
.modal_header{display:flex; align-items:center; justify-content:flex-start; gap:10px; padding:14px 16px; border-bottom:1px solid var(--border)}
.modal_title{margin:0}
.spacer{flex:1}
.icon_btn{background:transparent; color:var(--muted); border:1px solid var(--border); border-radius:8px; padding:6px; cursor:pointer}
.icon_btn .icon{width:18px; height:18px; display:block; fill:currentColor}
.icon_btn:hover{color:var(--text)}
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
.grid{display:grid; grid-template-columns:repeat(auto-fit, minmax(260px,1fr)); gap:14px; padding:0 0 16px}
.edit_grid{ grid-template-columns:1fr }
@media(max-width:520px){ .overlay{ --ovPad:8px } }
.edit_panel{padding:0 16px 16px}
.edit_grid{display:grid; grid-template-columns:repeat(auto-fit, minmax(220px,1fr)); gap:10px}
.edit_field{display:flex; flex-direction:column; gap:6px}
.edit_field.checkbox{flex-direction:row; align-items:center}
.edit_field.span2{grid-column:span 2}
.ef_label{color:var(--muted); font-weight:800; font-size:12px}
.ef_input{background:#0e1a34; color:var(--text); border:1px solid var(--border); border-radius:8px; padding:8px 10px; font-weight:800}
.ef_textarea{background:#0e1a34; color:var(--text); border:1px solid var(--border); border-radius:8px; padding:8px 10px; min-height:80px; font-weight:700}
.auto_grow{resize:vertical; width:100%; overflow:auto}
.block{background:rgba(255,255,255,.02); border:1px solid var(--border); border-radius:12px; padding:12px}
.block h3{margin:0 0 8px 0}
.classes{display:grid; gap:10px}
.class_head{font-weight:800; color:var(--muted)}
.class_body{font-weight:600}
.fine_print{color:var(--muted); font-size:12px; margin-top:8px}
.list{margin:0; padding-left:18px}
.actions{display:flex; gap:10px; padding:12px 16px; border-top:1px solid var(--border); justify-content:flex-end}
.edit_actions{margin-right:auto; display:flex; gap:8px}
.primary_btn{display:inline-flex; align-items:center; justify-content:center; padding:10px 14px; border-radius:999px; border:1px solid rgba(215,180,58,.22); background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16)); color:var(--text); font-weight:800; text-decoration:none}
.primary_btn.disabled{background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.08); color:var(--muted); cursor:not-allowed}
.ghost_btn{display:inline-flex; align-items:center; justify-content:center; padding:10px 14px; border-radius:999px; border:1px solid var(--border); color:var(--muted); background:transparent}
.disclaimer{padding:8px 16px 14px; font-size:12px; color:var(--accent); font-weight:800; border-top:1px dashed rgba(215,180,58,.35)}
@media(max-width:720px){
  .hero{grid-template-columns:1fr}
}
</style> 