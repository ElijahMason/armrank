<template>
  <TopBar />
  <Leaderboard
    :rankings_tab_name="'Rankings'"
    :weights_tab_name="'Weights'"
    :classes="['154','176','198','220','242','243+']"
    :default_selected_class="'243+'"
    sticky_prefix=""
  />
  <Leaderboard
    :rankings_tab_name="'Rankings_F'"
    :weights_tab_name="'Weights_F'"
    :classes="['143','144+']"
    :default_selected_class="'144+'"
    sticky_prefix="Women • "
  />
</template>

<script>
import TopBar from './components/TopBar.vue'
import Leaderboard from './components/Leaderboard.vue'

export default {
  name: 'App',
  components: { TopBar, Leaderboard },
}
</script>

<style>
/* page-level overrides can go here if needed */
</style>
