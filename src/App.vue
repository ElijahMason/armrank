<template>
  <TopBar />
  <MainContent />
</template>

<script>
import TopBar from './components/TopBar.vue'
import MainContent from './components/MainContent.vue'

export default {
  name: 'App',
  components: { TopBar, MainContent },
}
</script>
