import Vue from 'vue'
import Router from 'vue-router'
import index from '@/components/index'  //@号表示src目录
import test from '../components/test'    //..表示使用相对路径
import login from '@/components/login'
import edit_interface from '../components/interface/edit_interface'

Vue.use(Router)

export default new Router({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'default',
      redirect:'/index/1'  //自动重定向
    },
    {
      path: '/index/:tab',
      name: 'index',
      component: index,
      props:true,  //必须写，才能把tab参数传进组件index里面
    },
    {
      path: '/add/interface',
      name: 'add_interface',
      component: edit_interface,
      props:true,  //必须写，才能把tab参数传进组件index里面
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
