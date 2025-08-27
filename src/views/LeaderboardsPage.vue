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
          <input v-model="submitter_name" @change="persistSubmitterName" @blur="persistSubmitterName" type="text" inputmode="text" placeholder="Who are you?" class="input" />
        </label>

        <div class="row two_cols">
          <label class="field">
            <span class="label">Competitor A</span>
            <input v-model="sm_a" type="text" inputmode="text" placeholder="Full name" class="input" required />
          </label>
          <label class="field">
            <span class="label">Competitor B</span>
            <input v-model="sm_b" type="text" inputmode="text" placeholder="Full name" class="input" required />
          </label>
        </div>

        <div class="row two_cols">
          <fieldset class="field radios" role="radiogroup" aria-label="Winner">
            <span class="label">Winner</span>
            <div class="radio_row">
              <label class="radio_opt"><input type="radio" name="sm_winner" value="A" v-model="sm_winner" /> <span>{{ sm_a || 'Competitor A' }}</span></label>
              <label class="radio_opt"><input type="radio" name="sm_winner" value="B" v-model="sm_winner" /> <span>{{ sm_b || 'Competitor B' }}</span></label>
            </div>
          </fieldset>
          <label class="field">
            <span class="label">Score ({{ scoreHint }})</span>
            <input v-model="sm_score" type="text" inputmode="numeric" placeholder="e.g. 3-1" class="input score_input" @input="onScoreInput" />
            <div class="error_hint" v-show="scoreError">(format: 3-0)</div>
          </label>
        </div>

        <div class="row two_cols">
          <fieldset class="field" role="group" aria-label="Hand">
            <span class="label">Hand</span>
            <HandSlider v-model="sm_hand" />
          </fieldset>
          <div class="spacer"></div>
        </div>

        <div class="adv_toggle_row">
          <button type="button" class="ghost_btn" @click="advanced_open = !advanced_open" :aria-expanded="String(advanced_open)">
            {{ advanced_open ? 'Hide' : 'Show' }} advanced fields
            <svg class="chev" viewBox="0 0 24 24" :class="{up: advanced_open}"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
        </div>

        <div class="advanced_drawer" :class="{ open: advanced_open }" aria-hidden="false">
          <div class="row two_cols">
            <label class="field">
              <span class="label">{{ sm_a || 'Competitor 1' }} weight (lbs)</span>
              <input v-model="sm_weight1" type="number" inputmode="numeric" step="1" min="0" placeholder="Enter weight in lbs" class="input" />
            </label>
            <label class="field">
              <span class="label">{{ sm_b || 'Competitor 2' }} weight (lbs)</span>
              <input v-model="sm_weight2" type="number" inputmode="numeric" step="1" min="0" placeholder="Enter weight in lbs" class="input" />
            </label>
          </div>
          <div class="row two_cols">
            <label class="field">
              <span class="label">Date</span>
              <input v-model="sm_date" type="date" class="input" :max="todayStr" />
            </label>
            <label class="field">
              <span class="label">Location</span>
              <input v-model="sm_location" type="text" inputmode="text" placeholder="City / venue" class="input" />
            </label>
          </div>
          <label class="field">
            <span class="label">Notes</span>
            <textarea v-model="sm_notes" rows="4" placeholder="Event name, refs, match notes, link to video, etc." class="textarea"></textarea>
          </label>
        </div>
        <div class="actions">
          <button type="submit" class="submit_btn gold" :disabled="is_sending_sm || !canSubmitSupermatch">
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
export default {
  name: 'LeaderboardsPage',
  components: { Leaderboard, HandSlider },
  data(){
    return {
      feedback_name: '',
      feedback_text: '',
      is_sending: false,
      // supermatch form
      sm_a: '',
      sm_b: '',
      sm_hand: '',
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
    scoreError(){
      const s = (this.sm_score || '').trim()
      if(!s) return false
      return !/^\d+-\d+$/.test(s)
    }
  },
  mounted(){
    try{ this.submitter_name = localStorage.getItem('armrank_submitter_name') || '' }catch{}
    this.fetchClientIp()
  },
  computed:{
    todayStr(){
      const d = new Date()
      const pad = n => String(n).padStart(2,'0')
      return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`
    },
    scoreHint(){
      const a = (this.sm_a || '').trim()
      const b = (this.sm_b || '').trim()
      const w = (this.sm_winner || '').trim()
      if(!a || !b || !w) return 'W - L'
      const first = s => s.split(/\s+/)[0] || s
      const winName = w === 'A' ? first(a) : first(b)
      const loseName = w === 'A' ? first(b) : first(a)
      return `${winName} - ${loseName}`
    }
  },
  methods:{
    onScoreInput(){
      // Enforce score pattern: int-int
      let v = String(this.sm_score || '')
      v = v.replace(/[^0-9-]/g,'')
      // Only keep one dash and split into two integer segments
      const parts = v.split('-').slice(0,2)
      const clean = parts.map(p => p.replace(/[^0-9]/g,'').replace(/^0+(\d)/,'$1'))
      this.sm_score = clean.join(parts.length > 1 ? '-' : '')
    },
    scoreIsValid(){
      const s = (this.sm_score || '').trim()
      if(!s) return true
      return /^\d+-\d+$/.test(s)
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
        const score = (this.sm_score || '').trim()
        const date = (this.sm_date || '').trim()
        const location = (this.sm_location || '').trim()
        const notes = (this.sm_notes || '').trim()

        const winnerName = winner === 'A' ? a : b
        const loserName = winner === 'A' ? b : a
        const handLabel = hand === 'RH' ? 'Right hand' : 'Left hand'
        const scoreLabel = score ? ` — Score: ${score}` : ''

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
        this.sm_hand = ''
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
.radio_opt{display:inline-flex;gap:8px;align-items:center;background:rgba(255,255,255,.02);border:1px solid var(--border);padding:8px 10px;border-radius:999px}
.segmented{display:inline-flex;gap:0;background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:999px;padding:4px}
.seg_btn{border:0;background:transparent;color:var(--muted);font-weight:800;padding:8px 12px;border-radius:999px;cursor:pointer}
.seg_btn[aria-pressed="true"]{color:#070e1c;background:linear-gradient(180deg,var(--accent),var(--accent-2));box-shadow:0 6px 18px rgba(215,180,58,.18)}
.adv_toggle_row{display:flex;justify-content:flex-end;padding-top:4px}
.ghost_btn{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;border:1px solid var(--border);color:var(--muted);background:transparent;cursor:pointer}
.chev{width:16px;height:16px;transition:transform .2s ease}
.chev.up{transform:rotate(180deg)}
.advanced_drawer{max-height:0;overflow:hidden;transition:max-height .28s ease}
.advanced_drawer.open{max-height:520px}
.feedback_form{display:grid;gap:12px;padding:14px 16px}
.field{display:grid;gap:6px}
.label{color:var(--muted);font-weight:700}
.input,.textarea{width:100%;border:1px solid var(--border);border-radius:10px;background:rgba(255,255,255,.02);color:var(--text);padding:10px 12px;font-family:inherit;font-size:14px}
.input:focus,.textarea:focus{outline:none;border-color:rgba(215,180,58,.35)}
.input.error{border-color:#e74c3c}
.error_hint{color:#e74c3c;font-weight:800;font-size:12px}
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
.hand_slider .track{position:relative;width:100%;max-width:520px;height:44px;background:rgba(255,255,255,.05);border:1px solid var(--border);border-radius:999px;overflow:hidden}
.hand_slider .thumb{position:absolute;top:3px;left:3px;width:calc(50% - 6px);height:38px;border-radius:999px;background:linear-gradient(180deg,var(--accent),var(--accent-2));box-shadow:0 10px 24px rgba(215,180,58,.18);transition:transform .22s ease}
.hand_slider .thumb.right{transform:translateX(100%)}
.hand_slider .hand_label{position:absolute;top:50%;transform:translateY(-50%);width:50%;text-align:center;color:var(--muted);font-weight:900;letter-spacing:.3px}
.hand_slider .hand_label.left{left:0}
.hand_slider .hand_label.right{right:0}
/* Less glowy, squarer submit button */
.submit_btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 16px;border-radius:10px;border:1px solid rgba(185,147,34,.55);background:rgba(215,180,58,1);color:#061626;font-weight:900}
.submit_btn.gold{background:linear-gradient(180deg,var(--accent),var(--accent-2));border-color:transparent}
.submit_btn[disabled]{opacity:1;cursor:not-allowed;background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.12);color:var(--muted)}
</style>