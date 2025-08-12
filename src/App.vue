<template>
  <TopBar />
  <router-view />
</template>
<script>
import TopBar from './components/TopBar.vue'
export default { name: 'App', components: { TopBar } }
</script>

<style>
/* page-level overrides can go here if needed */
</style>
