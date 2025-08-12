import { createRouter, createWebHashHistory } from 'vue-router'

import LeaderboardsPage from './views/LeaderboardsPage.vue'
import TournamentsPage from './views/TournamentsPage.vue'

const routes = [
  { path: '/', redirect: '/leaderboards' },
  { path: '/leaderboards', name: 'leaderboards', component: LeaderboardsPage },
  { path: '/tournaments', name: 'tournaments', component: TournamentsPage },
]

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
}) 