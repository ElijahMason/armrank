import { createRouter, createWebHashHistory } from 'vue-router'

import LeaderboardsPage from './views/LeaderboardsPage.vue'
import TournamentsPage from './views/TournamentsPage.vue'
import ClubsPage from './views/ClubsPage.vue'

const routes = [
  { path: '/', redirect: '/leaderboards' },
  { path: '/leaderboards', name: 'leaderboards', component: LeaderboardsPage },
  { path: '/tournaments', name: 'tournaments', component: TournamentsPage },
  { path: '/clubs', name: 'clubs', component: ClubsPage },
]

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.afterEach((to)=>{
  if(to?.name){
    try{ localStorage.setItem(`last_seen.${to.name}`, String(Date.now())) }catch(e){}
  }
}) 