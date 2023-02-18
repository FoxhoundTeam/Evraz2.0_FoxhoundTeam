// Composables
import { createRouter, createWebHistory } from 'vue-router'
import MainView from "@/views/MainView.vue"
import ExhausterView from "@/views/ExhausterView.vue"
import PlotView from "@/views/PlotView.vue"

const routes = [
  {
    path: '/',
    name: 'MainView',
    component: MainView,
  },
  {
    path: '/exhauster',
    name: 'ExhausterView',
    component: ExhausterView,
  },
  {
    path: '/plot',
    name: 'PlotView',
    component: PlotView,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
