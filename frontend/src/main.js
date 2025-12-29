import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import AppSquare from './views/AppSquare.vue'
import './style.css'

const routes = [
  {
    path: '/',
    name: 'QAAgent',
    component: AppSquare
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

createApp(App).use(router).mount('#app')

