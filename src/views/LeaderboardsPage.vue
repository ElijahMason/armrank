<template>
  <Leaderboard
    :rankings_tab_name="'Rankings'"
    :weights_tab_name="'Weights'"
    :classes="['154','176','198','220','242','243+']"
    :default_selected_class="'243+'"
    sticky_prefix="Men • "
  />
  <Leaderboard
    :rankings_tab_name="'Rankings_F'"
    :weights_tab_name="'Weights_F'"
    :classes="['143','144+']"
    :default_selected_class="'144+'"
    sticky_prefix="Women • "
  />

  <main class="main_container">
    <section id="supermatch" class="panel supermatch_panel" role="region" aria-label="Supermatch Result">
      <div class="panel_header">
        <h2 class="title">Submit Supermatch Result</h2>
      </div>
      <form class="sm_form" @submit.prevent="submitSupermatch" novalidate>
        <label class="field">
          <span class="label">Your name</span>
          <input v-model="submitter_name" @change="persistSubmitterName" @blur="persistSubmitterName; submitter_blurred = true" type="text" inputmode="text" placeholder="Who are you?" class="input" :class="{ valid: submitter_blurred && !!(submitter_name || '').trim() }" />
        </label>

        <div class="row two_cols">
          <label class="field">
            <span class="label">Competitor A</span>
            <AthleteSelect v-model="sm_a" :options="known_names" placeholder="Full name" :blurred="sm_a_blurred" idBase="sm-a" @blur="sm_a_blurred = true" />
          </label>
          <label class="field">
            <span class="label">Competitor B</span>
            <AthleteSelect v-model="sm_b" :options="known_names" placeholder="Full name" :blurred="sm_b_blurred" idBase="sm-b" @blur="sm_b_blurred = true" />
          </label>
        </div>

        <div class="row two_cols">
          <fieldset class="field radios" role="radiogroup" aria-label="Winner">
            <span class="label">Winner</span>
            <div class="radio_row">
              <label class="radio_opt" :class="{ selected: sm_winner === 'A' }"><input type="radio" name="sm_winner" value="A" v-model="sm_winner" /> <span>{{ sm_a || 'Competitor A' }}</span></label>
              <label class="radio_opt" :class="{ selected: sm_winner === 'B' }"><input type="radio" name="sm_winner" value="B" v-model="sm_winner" /> <span>{{ sm_b || 'Competitor B' }}</span></label>
            </div>
          </fieldset>
          <label class="field" :class="{ error: scoreShowErrorBorder, valid: scoreValidAfterBlur }">
            <span class="label">Score ({{ scoreHint }})</span>
            <input
              v-model="sm_score"
              type="text"
              inputmode="numeric"
              placeholder="e.g. 3-1"
              class="input score_input"
              :class="{ error: scoreShowErrorBorder, valid: scoreValidAfterBlur }"
              @input="onScoreInput"
              @focus="onScoreFocus"
              @blur="onScoreBlur"
              :aria-invalid="String(scoreInvalid)"
            />
            <div class="error_hint" v-show="scoreShowErrorText">Enter number-number eg. 3-2</div>
          </label>
        </div>

        <div class="row two_cols">
          <fieldset class="field no_border" role="group" aria-label="Hand">
            <span class="label">Hand</span>
            <HandSlider v-model="sm_hand" />
          </fieldset>
          <div class="spacer"></div>
        </div>

        <div class="adv_toggle_row">
          <button type="button" class="ghost_btn dividerless" @click="advanced_open = !advanced_open" :aria-expanded="String(advanced_open)">
            {{ advanced_open ? 'Hide' : 'Show' }} advanced fields
            <svg class="chev" viewBox="0 0 24 24" :class="{up: advanced_open}"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
        </div>
        <div class="divider"></div>

        <div class="advanced_drawer" :class="{ open: advanced_open }" aria-hidden="false">
          <div class="row two_cols">
            <label class="field">
              <span class="label">{{ sm_a || 'Competitor 1' }} weight (lbs)</span>
              <input v-model="sm_weight1" type="number" inputmode="numeric" step="1" min="0" placeholder="Enter weight in lbs" class="input" @input="onWeightInput(1, $event)" @blur="sm_weight1_blurred = true" :class="{ valid: sm_weight1_blurred && !!String(sm_weight1).trim() }" />
            </label>
            <label class="field">
              <span class="label">{{ sm_b || 'Competitor 2' }} weight (lbs)</span>
              <input v-model="sm_weight2" type="number" inputmode="numeric" step="1" min="0" placeholder="Enter weight in lbs" class="input" @input="onWeightInput(2, $event)" @blur="sm_weight2_blurred = true" :class="{ valid: sm_weight2_blurred && !!String(sm_weight2).trim() }" />
            </label>
          </div>
          <div class="row two_cols">
            <label class="field">
              <span class="label">Date</span>
              <input v-model="sm_date" type="date" class="input" :max="todayStr" @blur="sm_date_blurred = true" :class="{ valid: sm_date_blurred && !!(sm_date || '').trim() }" />
            </label>
            <label class="field">
              <span class="label">Location</span>
              <input v-model="sm_location" type="text" inputmode="text" placeholder="City / venue" class="input" @blur="sm_location_blurred = true" :class="{ valid: sm_location_blurred && !!(sm_location || '').trim() }" />
            </label>
          </div>
          <label class="field">
            <span class="label">Notes</span>
            <textarea v-model="sm_notes" rows="4" placeholder="Event name, refs, match notes, link to video, etc." class="textarea" @blur="sm_notes_blurred = true" :class="{ valid: sm_notes_blurred && !!(sm_notes || '').trim() }"></textarea>
          </label>
        </div>
        <div class="divider" v-show="advanced_open"></div>
        <div class="actions with_summary">
          <div class="summary" aria-live="polite">{{ summaryText }}</div>
          <button type="submit" class="submit_btn" :class="{ gold: !submitDisabled }" :disabled="submitDisabled">
            {{ is_sending_sm ? 'Submitting…' : 'Submit' }}
          </button>
        </div>
      </form>
    </section>
  </main>

  <button class="feedback_tab" @click="feedback_open = true" aria-controls="feedback_sheet" :aria-expanded="String(feedback_open)">Feedback</button>

  <section id="feedback_sheet" class="feedback_sheet" :class="{ open: feedback_open }" role="dialog" aria-modal="true" aria-label="Feedback">
    <div class="sheet_header">
      <h2 class="title">Feedback</h2>
      <button class="close_btn" @click="feedback_open = false" aria-label="Close">×</button>
    </div>
    <form class="feedback_form" @submit.prevent="submitFeedback" novalidate>
      <label class="field">
        <span class="label">Name</span>
        <input
          v-model="feedback_name"
          type="text"
          inputmode="text"
          autocomplete="name"
          placeholder="Your name (optional)"
          class="input"
        />
      </label>
      <label class="field">
        <span class="label">Suggest features / rank changes</span>
        <textarea
          v-model="feedback_text"
          rows="5"
          placeholder="Suggest features / rank changes / club updates / etc."
          class="textarea"
          required
        ></textarea>
      </label>
      <div class="actions">
        <button type="submit" class="primary_btn" :disabled="is_sending || !feedback_text.trim()">
          {{ is_sending ? 'Sending…' : 'Send feedback' }}
        </button>
      </div>
      <p class="footer_note">Or contact Peter Lalande or Elijah Mason directly.</p>
    </form>
  </section>

  <div v-if="toast_show" class="toast" :class="toast_type" role="status" aria-live="polite">{{ toast_msg }}</div>
</template>
<script>
import Leaderboard from '../components/Leaderboard.vue'
import HandSlider from '../components/HandSlider.vue'
import AthleteSelect from '../components/AthleteSelect.vue'
export default {
  name: 'LeaderboardsPage',
  components: { Leaderboard, HandSlider, AthleteSelect },
  data(){
    const sheet_id_raw = 'https://docs.google.com/spreadsheets/d/1aD3ZFkMHCrg4lZe80lONyQz-MsEVStelCiCEyHb6-2Y/edit?usp=sharing'
    const sheet_id_match = String(sheet_id_raw).match(/\/d\/([a-zA-Z0-9-_]+)/)
    const sheet_id = sheet_id_match ? sheet_id_match[1] : String(sheet_id_raw).trim()
    return {
      feedback_name: '',
      feedback_text: '',
      is_sending: false,
      // supermatch form
      sm_a: '',
      sm_b: '',
      known_names: [],
      sm_hand: 'RH',
      sm_weight1: '',
      sm_weight2: '',
      sm_winner: '',
      sm_score: '',
      sm_date: '',
      sm_location: '',
      sm_notes: '',
      is_sending_sm: false,
      advanced_open: false,
      submitter_name: '',
      client_ip: '',
      feedback_open: false,
      toast_show: false,
      toast_msg: '',
      toast_type: 'success',
      webhook_url: 'https://discord.com/api/webhooks/1404936162040217630/_29ERb9EONoLzbQxK4pabApD5M5K8sUi6ViHk3PDSmmejJIB5MKmT8UUkzZph6NNnDds',
      sheet_id_raw,
      sheet_id,
      // ui state
      sm_a_blurred: false,
      sm_b_blurred: false,
      sm_score_blurred: false,
      scoreFocused: false,
      scoreHasInvalidBlur: false,
      submitter_blurred: false,
      sm_weight1_blurred: false,
      sm_weight2_blurred: false,
      sm_date_blurred: false,
      sm_location_blurred: false,
      sm_notes_blurred: false,
    }
  },
  computed:{
    scoreHint(){
      const a = (this.sm_a || '').trim()
      const b = (this.sm_b || '').trim()
      const w = (this.sm_winner || '').trim()
      if(!a || !b || !w) return 'W - L'
      const first = s => s.split(/\s+/)[0] || s
      const winName = w === 'A' ? first(a) : first(b)
      const loseName = w === 'A' ? first(b) : first(a)
      return `${winName} - ${loseName}`
    },
    scoreInvalid(){
      const s = (this.sm_score || '').trim()
      if(!s) return false
      if(!/^\d+-\d+$/.test(s)) return true
      const [l,r] = s.split('-').map(n => Number(n))
      if(!Number.isFinite(l) || !Number.isFinite(r)) return true
      return l === r
    },
    scoreShowErrorText(){
      // Only show error text after an invalid blur; keep it visible until valid
      return this.scoreHasInvalidBlur && this.scoreInvalid
    },
    scoreShowErrorBorder(){
      // Red border only when not focused and invalid and we have blurred invalid at least once
      return !this.scoreFocused && this.scoreHasInvalidBlur && this.scoreInvalid
    },
    scoreValidAfterBlur(){
      // Teal border on blur if filled and valid
      const hasValue = !!(this.sm_score || '').trim()
      return this.sm_score_blurred && hasValue && !this.scoreInvalid
    },
    summaryText(){
      const a = (this.sm_a || '').trim()
      const b = (this.sm_b || '').trim()
      const w = (this.sm_winner || '').trim()
      if(!a || !b || !w) return ''
      const winnerName = w === 'A' ? a : b
      const loserName = w === 'A' ? b : a
      const scored = (this.sm_score || '').trim()
      let score = '3-0'
      if(/^\d+-\d+$/.test(scored)){
        const [l,r] = scored.split('-').map(n=>Number(n))
        if(Number.isFinite(l) && Number.isFinite(r)){
          const hi = Math.max(l,r)
          const lo = Math.min(l,r)
          score = `${hi}-${lo}`
        }
      }
      return `${winnerName} beat ${loserName} ${score}`
    },
    submitDisabled(){
      const a = (this.sm_a || '').trim()
      const b = (this.sm_b || '').trim()
      const hand = (this.sm_hand || '').trim()
      const winner = (this.sm_winner || '').trim()
      const ok = !!(a && b && hand && winner)
      return this.is_sending_sm || !(ok && this.scoreIsValid())
    },
    todayStr(){
      const d = new Date()
      const pad = n => String(n).padStart(2,'0')
      return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`
    }
  },
  mounted(){
    try{
      this.submitter_name = localStorage.getItem('armrank_submitter_name') || ''
      if((this.submitter_name || '').trim()) this.submitter_blurred = true
    }catch{}
    this.fetchClientIp()
    this.loadKnownNames()
  },
  methods:{
    gvizCsv(tab){
      return `https://docs.google.com/spreadsheets/d/${this.sheet_id}/gviz/tq?tqx=out:csv&sheet=${encodeURIComponent(tab)}`
    },
    csvToRows(csv) {
      return String(csv || '')
        .trim()
        .split(/\r?\n/)
        .map(line => {
          const out = []
          let cur = ''
          let q = false
          for (let i = 0; i < line.length; i++) {
            const ch = line[i]
            if (ch === '"') { q = !q; continue }
            if (ch === ',' && !q) { out.push(cur); cur = '' } else { cur += ch }
          }
          out.push(cur)
          return out.map(s => s.trim())
        })
    },
    async loadKnownNames(){
      try{
        const [rankM, rankW, wtM, wtW, clubs] = await Promise.all([
          fetch(this.gvizCsv('Rankings')).then(r=>r.text()).catch(()=>''),
          fetch(this.gvizCsv('Rankings_F')).then(r=>r.text()).catch(()=>''),
          fetch(this.gvizCsv('Weights')).then(r=>r.text()).catch(()=>''),
          fetch(this.gvizCsv('Weights_F')).then(r=>r.text()).catch(()=>''),
          fetch(this.gvizCsv('Clubs')).then(r=>r.text()).catch(()=>''),
        ])
        const seen = new Set()
        const acc = []
        const add = (s)=>{
          const t = String(s || '').trim()
          if(!t) return
          const k = t.toLowerCase()
          if(seen.has(k)) return
          seen.add(k)
          acc.push(t)
        }
        const rM = this.csvToRows(rankM)
        const rW = this.csvToRows(rankW)
        rM.slice(1).forEach(r=>{ add(r[0]); add(r[2]) })
        rW.slice(1).forEach(r=>{ add(r[0]); add(r[2]) })
        const wM = this.csvToRows(wtM)
        const wW = this.csvToRows(wtW)
        wM.slice(1).forEach(r=>add(r[0]))
        wW.slice(1).forEach(r=>add(r[0]))
        const cR = this.csvToRows(clubs)
        cR.slice(1).forEach(row=>{ row.forEach(cell=>add(cell)) })
        acc.sort((a,b)=>a.localeCompare(b))
        this.known_names = acc
      }catch(e){ this.known_names = [] }
    },
    onWeightInput(which, evt){
      const raw = String(evt?.target?.value ?? '')
      const digits = raw.replace(/[^0-9]/g, '')
      if(which === 1) this.sm_weight1 = digits
      else if(which === 2) this.sm_weight2 = digits
    },
    onScoreInput(){
      // Enforce score pattern: int-int
      let v = String(this.sm_score || '')
      v = v.replace(/[^0-9-]/g,'')
      // Only keep one dash and split into two integer segments
      const parts = v.split('-').slice(0,2)
      const clean = parts.map(p => p.replace(/[^0-9]/g,'').replace(/^0+(\d)/,'$1'))
      this.sm_score = clean.join(parts.length > 1 ? '-' : '')
      // If value becomes valid while editing, clear prior error text
      if(!this.scoreInvalid) this.scoreHasInvalidBlur = false
    },
    onScoreFocus(){
      this.scoreFocused = true
    },
    onScoreBlur(){
      this.scoreFocused = false
      this.sm_score_blurred = true
      // If invalid after blur, enable persistent error text
      this.scoreHasInvalidBlur = this.scoreInvalid
    },
    scoreIsValid(){
      const s = (this.sm_score || '').trim()
      if(!s) return true
      if(!/^\d+-\d+$/.test(s)) return false
      const [l,r] = s.split('-').map(n => Number(n))
      if(!Number.isFinite(l) || !Number.isFinite(r)) return false
      return l !== r
    },
    canSubmitSupermatch(){
      const a = (this.sm_a || '').trim()
      const b = (this.sm_b || '').trim()
      const hand = (this.sm_hand || '').trim()
      const winner = (this.sm_winner || '').trim()
      const ok = !!(a && b && hand && winner)
      return ok && this.scoreIsValid()
    },
    toggleHand(){
      if(this.sm_hand === 'RH') this.sm_hand = 'LH';
      else this.sm_hand = 'RH'
    },
    persistSubmitterName(){
      try{ localStorage.setItem('armrank_submitter_name', this.submitter_name || '') }catch{}
    },
    async fetchClientIp(){
      try{
        const res = await fetch('https://api.ipify.org?format=json')
        if(res.ok){
          const j = await res.json()
          this.client_ip = String(j?.ip || '')
        }
      }catch(e){ /* noop */ }
    },
    async submitSupermatch(){
      if(this.is_sending_sm || !this.canSubmitSupermatch()) return
      this.is_sending_sm = true
      try{
        const a = (this.sm_a || '').trim()
        const b = (this.sm_b || '').trim()
        const hand = (this.sm_hand || '').trim()
        const weight1 = (this.sm_weight1 || '').trim()
        const weight2 = (this.sm_weight2 || '').trim()
        const winner = (this.sm_winner || '').trim()
        const scoreRaw = (this.sm_score || '').trim()
        const date = (this.sm_date || '').trim()
        const location = (this.sm_location || '').trim()
        const notes = (this.sm_notes || '').trim()

        const winnerName = winner === 'A' ? a : b
        const loserName = winner === 'A' ? b : a
        const handLabel = hand === 'RH' ? 'Right hand' : 'Left hand'
        // Normalize score to winner-loser high-low if provided
        let scoreLabel = ''
        if(scoreRaw){
          const m = scoreRaw.match(/^(\d+)-(\d+)$/)
          if(m){
            let left = Number(m[1])
            let right = Number(m[2])
            if(Number.isFinite(left) && Number.isFinite(right)){
              if(left < right){ const tmp = left; left = right; right = tmp }
              scoreLabel = ` — Score: ${left}-${right}`
            }
          }
        }

        const title = `Supermatch Result`
        const description = `🏆 ${winnerName} over ${loserName} • ${handLabel}${scoreLabel}`
        const fields = []
        if(date) fields.push({ name: 'Date', value: date, inline: true })
        if(location) fields.push({ name: 'Location', value: location, inline: true })
        if(weight1) fields.push({ name: `${a || 'Competitor 1'} weight`, value: weight1, inline: true })
        if(weight2) fields.push({ name: `${b || 'Competitor 2'} weight`, value: weight2, inline: true })
        if(notes) fields.push({ name: 'Notes', value: notes, inline: false })
        const footerBits = []
        footerBits.push(`Submitter: ${ (this.submitter_name || 'Anonymous').trim() || 'Anonymous' }`)
        if(this.client_ip) footerBits.push(`IP: ${this.client_ip}`)
        const footerText = `Submitted via ArmRank • Supermatch • ${footerBits.join(' • ')}`
        const payload = {
          embeds: [{
            title,
            description,
            color: 10181046,
            fields,
            footer: { text: footerText }
          }]
        }

        const res = await fetch(this.webhook_url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
        if(res.status < 200 || res.status >= 300) throw new Error('Non-2xx response')
        this.toast_type = 'success'
        this.toast_msg = 'Supermatch submitted successfully!'
        this.toast_show = true
        // persist name, reset form
        this.persistSubmitterName()
        this.sm_a = ''
        this.sm_b = ''
        this.sm_hand = 'RH'
        this.sm_weight1 = ''
        this.sm_weight2 = ''
        this.sm_winner = ''
        this.sm_score = ''
        this.sm_date = ''
        this.sm_location = ''
        this.sm_notes = ''
        setTimeout(()=>{ this.toast_show = false }, 4600)
      }catch(e){
        this.toast_type = 'error'
        this.toast_msg = 'Failed to submit supermatch. Please try again later.'
        this.toast_show = true
        setTimeout(()=>{ this.toast_show = false }, 4600)
      }finally{
        this.is_sending_sm = false
      }
    },
    async submitFeedback(){
      const message = this.feedback_text.trim()
      if(!message || this.is_sending) return
      this.is_sending = true
      try{
        const title = this.feedback_name?.trim() || 'Anonymous'
        const footerBits = []
        footerBits.push(`Submitter: ${title}`)
        if(this.client_ip) footerBits.push(`IP: ${this.client_ip}`)
        const footerText = `Submitted via ArmRank • Feedback • ${footerBits.join(' • ')}`
        const payload = { embeds: [{ title, description: message, color: 3066993, footer: { text: footerText } }] }
        const res = await fetch(this.webhook_url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
        // Discord webhooks typically return 204 No Content on success, treat any 2xx as success
        if(res.status < 200 || res.status >= 300) throw new Error('Non-2xx response')
        this.toast_type = 'success'
        this.toast_msg = "Success! I've received your feedback and I might read it one day."
        this.toast_show = true
        this.feedback_name = ''
        this.feedback_text = ''
        this.feedback_open = false
        setTimeout(()=>{ this.toast_show = false }, 4600)
      }catch(e){
        this.toast_type = 'error'
        this.toast_msg = 'Something went wrong... I swear it was working a second ago'
        this.toast_show = true
        setTimeout(()=>{ this.toast_show = false }, 4600)
      }finally{
        this.is_sending = false
      }
    }
  }
}
</script>
<style scoped>
.main_container{width:min(1100px,100%);margin:0 auto;padding-inline:clamp(12px,3vw,24px);padding-block:24px}
.panel{background:linear-gradient(180deg, rgba(11,22,48,.94), rgba(8,18,40,.92));border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--glow);margin-top:18px;overflow:hidden}
.panel_header{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--border)}
.title{margin:0;font-size:18px}
.req{color:#e67e22;margin-left:6px}
.sm_form{display:grid;gap:12px;padding:14px 16px}
.row{display:grid;gap:12px}
.two_cols{grid-template-columns:1fr;}
@media (min-width:720px){ .two_cols{ grid-template-columns:1fr 1fr } }
.radios{border:0;padding:0;margin:0}
.radio_row{display:flex;gap:12px;align-items:center}
.radio_opt{display:inline-flex;gap:0;align-items:center;justify-content:center;min-height:36px;min-width:0;background:transparent;border:2px solid var(--border);padding:8px 14px;border-radius:999px}
.radio_opt > input[type="radio"]{appearance:none;-webkit-appearance:none;width:0;height:0;margin:0;padding:0;border:0}
.radio_opt span{display:inline-block;width:100%;text-align:center}
.radio_opt.selected{background:transparent;color:#dfffe9;border-color:transparent;position:relative}
.radio_opt.selected::before{content:"";position:absolute;inset:0;border-radius:999px;padding:2px;background:linear-gradient(180deg,#20c997,#17a2b8);-webkit-mask:linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}
.segmented{display:inline-flex;gap:0;background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:999px;padding:4px}
.seg_btn{border:0;background:transparent;color:var(--muted);font-weight:800;padding:8px 12px;border-radius:999px;cursor:pointer}
.seg_btn[aria-pressed="true"]{color:#070e1c;background:linear-gradient(180deg,var(--accent),var(--accent-2));box-shadow:0 6px 18px rgba(215,180,58,.18)}
.adv_toggle_row{display:flex;justify-content:flex-end;padding-top:4px}
.ghost_btn{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;border:1px solid var(--border);color:var(--muted);background:transparent;cursor:pointer}
.ghost_btn.dividerless{border-color:transparent;padding-left:0;padding-right:0}
.divider{height:1px;background:rgba(255,255,255,.08);width:100%}
.sm_form > .divider{margin-left:-16px;margin-right:-16px;width:auto}
.chev{width:16px;height:16px;transition:transform .2s ease}
.chev.up{transform:rotate(180deg)}
.advanced_drawer{max-height:0;overflow:hidden;transition:max-height .28s ease}
.advanced_drawer.open{max-height:520px}
.feedback_form{display:grid;gap:12px;padding:14px 16px}
.field{display:grid;gap:6px}
.field.no_border{border:0}
.label{color:var(--muted);font-weight:700}
.input,.textarea{width:100%;border:1px solid var(--border);border-radius:10px;background:rgba(255,255,255,.02);color:var(--text);padding:10px 12px;font-family:inherit;font-size:14px}
.input:focus,.textarea:focus{outline:none;border-color:rgba(215,180,58,.55)}
.input.valid{border-color:rgba(23,162,184,.55);background-image:none;background-color:inherit}
.textarea.valid{border-color:rgba(23,162,184,.55);background-image:none;background-color:inherit}
.input.error{border-color:#e74c3c}
.field.error .input{border-color:#e74c3c}
.field.error .label{color:#ff9b91}
.error_hint{color:#e74c3c;font-weight:600;font-size:12px}
.actions{display:flex;justify-content:flex-end}
.primary_btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;border:1px solid rgba(215,180,58,.22);background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16));color:var(--text);font-weight:800;text-decoration:none;cursor:pointer}
.primary_btn[disabled]{opacity:.6; cursor:not-allowed}
.footer_note{margin:0;padding:8px 16px 16px;color:var(--muted);font-size:12px}
.toast{position:fixed; left:50%; bottom:22px; transform:translateX(-50%); max-width:92vw; min-width:260px; text-align:center; line-height:1.35; padding:12px 16px; font-weight:800; z-index:50; animation: toastPop .28s ease; border-radius:999px; box-shadow:0 10px 30px rgba(0,0,0,.25); border:2px solid}
.toast.success{background:linear-gradient(180deg, rgba(46,204,113,.15), rgba(46,204,113,.12)); color:#dfffe9; border-color:#2ecc71}
.toast.error{background:linear-gradient(180deg, rgba(231,76,60,.18), rgba(231,76,60,.14)); color:#ffe6e3; border-color:#e74c3c}
@keyframes toastPop{ from{ opacity:0; transform:translateX(-50%) translateY(6px) scale(.98)} to{ opacity:1; transform:translateX(-50%) translateY(0) scale(1)} }

/* Feedback bottom sheet */
.feedback_tab{position:fixed;left:12px;bottom:0;z-index:40;padding:8px 14px 6px 14px;border-radius:8px 8px 0 0;border:1px solid rgba(30,144,255,.35);background:linear-gradient(180deg, rgba(30,144,255,.85), rgba(30,144,255,.8));color:#061626;font-weight:900;cursor:pointer}
.feedback_sheet{position:fixed;left:50%;bottom:0;transform:translateX(-50%) translateY(100%);width:min(720px,100%);background:linear-gradient(180deg, rgba(11,22,48,.98), rgba(8,18,40,.98));border:1px solid var(--border);border-radius:14px 14px 0 0;box-shadow:0 -12px 40px rgba(0,0,0,.35);z-index:45;transition:transform .28s ease}
.feedback_sheet.open{transform:translateX(-50%) translateY(0)}
.sheet_header{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--border)}
.close_btn{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--muted);font-weight:800;cursor:pointer}
/* Hand slider */
.hand_slider{display:flex;justify-content:center;padding:2px 0}
.hand_slider .track{position:relative;width:100%;max-width:520px;height:44px;background:transparent;border:0;border-radius:999px;overflow:hidden}
.hand_slider .thumb{position:absolute;top:3px;left:3px;width:calc(50% - 6px);height:38px;border-radius:999px;background:linear-gradient(180deg,#20c997,#17a2b8);box-shadow:0 10px 24px rgba(23,162,184,.18);transition:transform .22s ease}
.hand_slider .thumb.right{transform:translateX(100%)}
.hand_slider .hand_label{position:absolute;top:50%;transform:translateY(-50%);width:50%;text-align:center;color:var(--muted);font-weight:900;letter-spacing:.3px}
.hand_slider .hand_label.left{left:0}
.hand_slider .hand_label.right{right:0}
/* Less glowy, squarer submit button */
.actions.with_summary{display:flex;align-items:center;justify-content:space-between;gap:12px}
.summary{color:var(--muted);font-weight:700}
.submit_btn{display:inline-flex;align-items:center;justify-content:center;padding:14px 22px;border-radius:12px;border:1px solid rgba(23,162,184,.55);background:transparent;color:#061626;font-weight:900;font-size:16px}
.submit_btn.gold{background:linear-gradient(180deg,#20c997,#17a2b8);border-color:transparent;color:#061626}
.submit_btn[disabled]{opacity:1;cursor:not-allowed;background:transparent;border-color:rgba(255,255,255,.12);color:var(--muted)}
</style>