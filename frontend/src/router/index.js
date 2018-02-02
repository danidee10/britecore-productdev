import Vue from 'vue'
import Router from 'vue-router'
import Risk from '@/components/Risk'
import Risks from '@/components/Risks'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Risks',
      component: Risks
    },
    {
      path: '/:id/',
      name: 'Risk',
      component: Risk
    }
  ]
})
