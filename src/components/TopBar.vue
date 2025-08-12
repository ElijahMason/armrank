<template>
  <header>
    <div class="top_bar">
      <div class="brand"><img class="brand_logo" :src="logo_src" alt="ArmRank crest" width="38" height="38" /> Oregon Arm Wrestling Rankings</div>
    </div>
  </header>
</template>

<script>
import logoUrl from '../assets/armrank-logo.svg'
export default {
  name: 'TopBar',
  computed: {
    logo_src(){
      return logoUrl
    }
  }
}
</script>

<style scoped>
header{position:sticky;top:0;z-index:20;backdrop-filter:blur(8px);background:linear-gradient(180deg, rgba(7,14,28,.92), rgba(7,14,28,.55));border-bottom:1px solid var(--border)}
.top_bar{display:flex;gap:14px;align-items:center;justify-content:space-between;padding:12px 24px}
.brand{display:flex;gap:12px;align-items:center;font-weight:800}
.brand_logo{width:38px;height:38px;border-radius:10px;box-shadow:var(--glow);display:block}
</style> 