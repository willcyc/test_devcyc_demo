<template>
  <div id="app">
    <!--<img src="./assets/logo.png">-->
    <div class="main-head">

      <div class="head-img">
        <img :src="head_img" hegiht="50px" width="50px"/>
        <span>接口测试系统</span>
      </div>

      <div>
        <i class="el-icon-info icon-color"></i> 关于
      </div>

    </div>
    <router-view/>
  </div>
</template>

<script>
  import interface_jpg from './assets/interface.jpg'

  export default {
    name: 'App',
    data(){
      return{
        head_img:interface_jpg,
      }
    }
  }
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /*margin-top: 60px;*/
}
  body{
    margin: 0
  }

  .main-head{
    background:#eff4fa;
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
  }

  .head-img{
    display: flex;
    align-items: center;
  }

  .head-img span{
    font-size:20px;
    margin-left: 10px;
  }

  .icon-color{
    color: #5a98de;
  }
</style>
