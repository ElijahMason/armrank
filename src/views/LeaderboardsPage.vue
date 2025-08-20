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