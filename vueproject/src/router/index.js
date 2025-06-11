import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/sizeCompress',
    name: 'sizeCompress',
    component:  () => import('../views/SizeCompress.vue')
  },
  {
    path: '/support',
    name: 'support',
    component:  () => import('../views/SupportView.vue')
  },
  {
    path: '/quality',
    name: 'quality',
    component:  () => import('../views/QualityView.vue')
  },
  {
    path: '/image',
    name: 'image',
    component:  () => import('../views/ImageView.vue')
  }

]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
