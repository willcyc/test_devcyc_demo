import Vue from 'vue'
import Router from 'vue-router'
import index from '@/components/index'  //@号表示src目录
import test from '../components/test'    //..表示使用相对路径
import login from '@/components/login'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/index',
      name: 'index',
      component: index
    },
    {
      path: '/test',
      name: 'test',
      component: test
    },
    {
      path: '/login',
      name: 'login',
      component: login
    }
  ]
})
