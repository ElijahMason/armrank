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
          <label class="field">
            <span class="label">Hand</span>
            <select v-model="sm_hand" class="input" required>
              <option disabled value="">Select hand</option>
              <option value="RH">Right hand</option>
              <option value="LH">Left hand</option>
              <option value="Both">Both</option>
            </select>
          </label>
          <label class="field">
            <span class="label">Weight class</span>
            <input v-model="sm_weight" type="text" inputmode="text" placeholder="e.g. 198 lbs" class="input" />
          </label>
        </div>

        <div class="row two_cols">
          <label class="field">
            <span class="label">Date</span>
            <input v-model="sm_date" type="date" class="input" />
          </label>
          <label class="field">
            <span class="label">Location</span>
            <input v-model="sm_location" type="text" inputmode="text" placeholder="City / venue (optional)" class="input" />
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
            <span class="label">Score</span>
            <input v-model="sm_score" type="text" inputmode="text" placeholder="e.g. 3-1" class="input" />
          </label>
        </div>

        <label class="field">
          <span class="label">Notes</span>
          <textarea v-model="sm_notes" rows="4" placeholder="Event name, refs, match notes, link to video, etc." class="textarea"></textarea>
        </label>
        <div class="actions">
          <button type="submit" class="primary_btn" :disabled="is_sending_sm || !canSubmitSupermatch">
            {{ is_sending_sm ? 'Submitting…' : 'Submit supermatch' }}
          </button>
        </div>
      </form>
    </section>
    <section id="feedback" class="panel feedback_panel" role="region" aria-label="Feedback">
      <div class="panel_header">
        <h2 class="title">Feedback</h2>
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
      </form>
      <p class="footer_note">Or contact Peter Lalande or Elijah Mason directly.</p>
    </section>
  </main>

  <div v-if="toast_show" class="toast" :class="toast_type" role="status" aria-live="polite">{{ toast_msg }}</div>
</template>
<script>
import Leaderboard from '../components/Leaderboard.vue'
export default {
  name: 'LeaderboardsPage',
  components: { Leaderboard },
  data(){
    return {
      feedback_name: '',
      feedback_text: '',
      is_sending: false,
      // supermatch form
      sm_a: '',
      sm_b: '',
      sm_hand: '',
      sm_weight: '',
      sm_winner: '',
      sm_score: '',
      sm_date: '',
      sm_location: '',
      sm_notes: '',
      is_sending_sm: false,
      toast_show: false,
      toast_msg: '',
      toast_type: 'success',
      webhook_url: 'https://discord.com/api/webhooks/1404936162040217630/_29ERb9EONoLzbQxK4pabApD5M5K8sUi6ViHk3PDSmmejJIB5MKmT8UUkzZph6NNnDds',
    }
  },
  mounted(){
    if(this.$route?.query?.goto === 'feedback'){
      const scrollNow = ()=>{ document.getElementById('feedback')?.scrollIntoView({ behavior:'smooth', block:'start' }) }
      this.$nextTick(scrollNow)
      // Re-scroll a few times to compensate for late content height changes
      let attempts = 0
      const id = setInterval(()=>{
        scrollNow()
        attempts++
        if(attempts > 12) clearInterval(id)
      }, 150)
    }
  },
  methods:{
    canSubmitSupermatch(){
      const a = (this.sm_a || '').trim()
      const b = (this.sm_b || '').trim()
      const hand = (this.sm_hand || '').trim()
      const winner = (this.sm_winner || '').trim()
      return !!(a && b && hand && winner)
    },
    async submitSupermatch(){
      if(this.is_sending_sm || !this.canSubmitSupermatch()) return
      this.is_sending_sm = true
      try{
        const a = (this.sm_a || '').trim()
        const b = (this.sm_b || '').trim()
        const hand = (this.sm_hand || '').trim()
        const weight = (this.sm_weight || '').trim()
        const winner = (this.sm_winner || '').trim()
        const score = (this.sm_score || '').trim()
        const date = (this.sm_date || '').trim()
        const location = (this.sm_location || '').trim()
        const notes = (this.sm_notes || '').trim()

        const winnerName = winner === 'A' ? a : b
        const loserName = winner === 'A' ? b : a
        const handLabel = hand === 'Both' ? 'Both hands' : (hand === 'RH' ? 'Right hand' : 'Left hand')
        const weightLabel = weight ? ` ${weight}` : ''
        const scoreLabel = score ? ` — Score: ${score}` : ''

        const title = `Supermatch Result`
        const description = `🏆 ${winnerName} over ${loserName} • ${handLabel}${weightLabel}${scoreLabel}`
        const fields = []
        if(date) fields.push({ name: 'Date', value: date, inline: true })
        if(location) fields.push({ name: 'Location', value: location, inline: true })
        if(notes) fields.push({ name: 'Notes', value: notes, inline: false })

        const payload = {
          embeds: [{
            title,
            description,
            color: 10181046,
            fields,
            footer: { text: 'Submitted via ArmRank • Supermatch' }
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
        // reset form
        this.sm_a = ''
        this.sm_b = ''
        this.sm_hand = ''
        this.sm_weight = ''
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
        const payload = { embeds: [{ title, description: message, color: 3066993 }] }
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
.panel{background:linear-gradient(180deg, rgba(11,22,48,.94), rgba(8,18,40,.92));border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--glow);margin-top:18px;overflow:hidden}
.panel_header{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--border)}
.title{margin:0;font-size:18px}
.sm_form{display:grid;gap:12px;padding:14px 16px}
.row{display:grid;gap:12px}
.two_cols{grid-template-columns:1fr;}
@media (min-width:720px){ .two_cols{ grid-template-columns:1fr 1fr } }
.radios{border:0;padding:0;margin:0}
.radio_row{display:flex;gap:12px;align-items:center}
.radio_opt{display:inline-flex;gap:8px;align-items:center;background:rgba(255,255,255,.02);border:1px solid var(--border);padding:8px 10px;border-radius:999px}
.feedback_form{display:grid;gap:12px;padding:14px 16px}
.field{display:grid;gap:6px}
.label{color:var(--muted);font-weight:700}
.input,.textarea{width:100%;border:1px solid var(--border);border-radius:10px;background:rgba(255,255,255,.02);color:var(--text);padding:10px 12px;font-family:inherit;font-size:14px}
.input:focus,.textarea:focus{outline:none;border-color:rgba(215,180,58,.35)}
.actions{display:flex;justify-content:flex-end}
.primary_btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;border:1px solid rgba(215,180,58,.22);background:linear-gradient(180deg,rgba(215,180,58,.18),rgba(185,147,34,.16));color:var(--text);font-weight:800;text-decoration:none;cursor:pointer}
.primary_btn[disabled]{opacity:.6; cursor:not-allowed}
.footer_note{margin:0;padding:8px 16px 16px;color:var(--muted);font-size:12px}
.toast{position:fixed; left:50%; bottom:22px; transform:translateX(-50%); max-width:92vw; min-width:260px; text-align:center; line-height:1.35; padding:12px 16px; font-weight:800; z-index:50; animation: toastPop .28s ease; border-radius:999px; box-shadow:0 10px 30px rgba(0,0,0,.25); border:2px solid}
.toast.success{background:linear-gradient(180deg, rgba(46,204,113,.15), rgba(46,204,113,.12)); color:#dfffe9; border-color:#2ecc71}
.toast.error{background:linear-gradient(180deg, rgba(231,76,60,.18), rgba(231,76,60,.14)); color:#ffe6e3; border-color:#e74c3c}
@keyframes toastPop{ from{ opacity:0; transform:translateX(-50%) translateY(6px) scale(.98)} to{ opacity:1; transform:translateX(-50%) translateY(0) scale(1)} }
</style> 