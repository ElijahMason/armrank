<template>
  <header>
    <div class="top_bar">
      <div class="brand"><div class="crest"></div> Oregon Arm Wrestling Rankings</div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'TopBar',
}
</script>

<style scoped>
header{position:sticky;top:0;z-index:20;backdrop-filter:blur(8px);background:linear-gradient(180deg, rgba(7,14,28,.92), rgba(7,14,28,.55));border-bottom:1px solid var(--border)}
.top_bar{display:flex;gap:14px;align-items:center;justify-content:space-between;padding:12px 24px}
.brand{display:flex;gap:12px;align-items:center;font-weight:800}
.crest{width:38px;height:38px;border-radius:10px;background:conic-gradient(from 220deg,var(--accent),var(--accent) 50%,var(--accent-2) 50%,var(--accent-2));box-shadow:var(--glow)}
</style> 