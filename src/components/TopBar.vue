<template>
  <header>
    <div class="top_bar">
      <div class="brand"><div class="crest"></div> Oregon Arm Wrestling Rankings</div>
      <nav class="nav">
        <router-link class="nav_link" to="/leaderboards">Leaderboards</router-link>
        <router-link class="nav_link" to="/tournaments">Tournaments</router-link>
      </nav>
    </div>
  </header>
</template>

<script>
export default { name: 'TopBar' }
</script>

<style scoped>
header{position:sticky;top:0;z-index:20;backdrop-filter:blur(8px);background:linear-gradient(180deg, rgba(7,14,28,.92), rgba(7,14,28,.55));border-bottom:1px solid var(--border)}
.top_bar{display:flex;gap:14px;align-items:center;justify-content:space-between;padding:12px 24px}
.brand{display:flex;gap:12px;align-items:center;font-weight:800}
.brand_logo{width:38px;height:38px;border-radius:10px;box-shadow:var(--glow);display:block}
.nav{display:flex;gap:12px;flex-wrap:wrap}
.nav_link{color:var(--muted);text-decoration:none;font-weight:800;padding:6px 8px;border-radius:8px;white-space:nowrap}
.nav_link.router-link-active{color:#070e1c;background:linear-gradient(180deg,var(--accent),var(--accent-2))}
@media(max-width:520px){
  .top_bar{gap:8px;padding:10px 12px}
  .brand{font-size:14px}
  .nav{gap:8px}
  .nav_link{padding:6px 6px}
}
</style> 