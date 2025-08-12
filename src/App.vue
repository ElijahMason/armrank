<template>
  <TopBar />
  <MainContent />
  <WomenSection />
</template>

<script>
import TopBar from './components/TopBar.vue'
import MainContent from './components/MainContent.vue'
import WomenSection from './components/WomenSection.vue'

export default {
  name: 'App',
  components: { TopBar, MainContent, WomenSection },
}
</script>
