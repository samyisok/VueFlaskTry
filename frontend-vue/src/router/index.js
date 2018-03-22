import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Registration from '@/components/Registration.vue'
import Signin from '@/components/Signin.vue'
import Test from '@/components/Test.vue'
import Messages from '@/components/Messages.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/registration',
      name: 'Registration',
      component: Registration
    },
    {
      path: '/login',
      name: 'login',
      component: Signin
    },
    {
      path: '/test',
      name: 'test',
      component: Test
    },
    {
      path: '/messages',
      name: 'Messages',
      component: Messages
    }
  ],
  mode: 'history'
})
