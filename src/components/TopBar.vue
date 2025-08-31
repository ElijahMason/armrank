<template>
  <header>
    <div class="top_bar">
      <div class="brand"><div class="crest"></div> Oregon Arm Wrestling Rankings</div>
      <nav class="nav">
        <router-link class="nav_link" to="/leaderboards">Leaderboards <span v-if="has_update('leaderboards')" class="notif_dot" aria-label="New"></span></router-link>
        <router-link class="nav_link" to="/tournaments">Tournaments <span v-if="has_update('tournaments')" class="notif_dot" aria-label="New"></span></router-link>
        <router-link class="nav_link" to="/clubs">Clubs <span v-if="has_update('clubs')" class="notif_dot" aria-label="New"></span></router-link>
        <router-link v-if="dev" class="nav_link" to="/admin">Admin</router-link>
      </nav>
    </div>
  </header>
</template>

<script>
import { updates, newness_window_ms } from '../updates'
import { isDevMode } from '../utils/devMode'
export default {
  name: 'TopBar',
  data(){
    return { dev: false }
  },
  mounted(){ this.dev = isDevMode() },
  methods:{
    has_update(page){
      try{
        const last_updated = updates[page]
        if(!Number.isFinite(last_updated)) return false
        const now = Date.now()
        if(now - last_updated > newness_window_ms) return false
        const seen_raw = localStorage.getItem(`last_seen.${page}`)
        const seen = Number(seen_raw || 0)
        return !(Number.isFinite(seen) && seen >= last_updated)
      }catch(e){ return false }
    }
  }
}
</script>

<style scoped>
header{position:sticky;top:0;z-index:20;backdrop-filter:blur(8px);background:linear-gradient(180deg, rgba(7,14,28,.92), rgba(7,14,28,.55));border-bottom:1px solid var(--border)}
.top_bar{display:flex;gap:14px;align-items:center;justify-content:space-between;padding:12px 24px}
.brand{display:flex;gap:12px;align-items:center;font-weight:800}
.brand_logo{width:38px;height:38px;border-radius:10px;box-shadow:var(--glow);display:block}
.nav{display:flex;gap:12px;flex-wrap:wrap}
.nav_link{color:var(--muted);text-decoration:none;font-weight:800;padding:6px 8px;border-radius:8px;white-space:nowrap;position:relative;display:inline-flex;align-items:center}
.nav_link.router-link-active{color:#070e1c;background:linear-gradient(180deg,var(--accent),var(--accent-2))}
.notif_dot{position:absolute;top:-2px;right:-4px;display:inline-block;width:10px;height:10px;border-radius:999px;background:linear-gradient(180deg, rgba(215,180,58,.95), rgba(185,147,34,.92));box-shadow:0 0 0 2px rgba(0,0,0,.45);margin-left:0;transform:none;pointer-events:none}
@media(max-width:520px){
  .top_bar{gap:8px;padding:10px 12px}
  .brand{font-size:14px}
  .nav{gap:8px}
  .nav_link{padding:6px 6px}
}
</style> 