<template>
  <div class="login-main-context">
    <div class="login-title">
      账号登录
    </div>
    <el-form :model="rule_form" :rules="rules" ref="ruleForm" label-width="100px" class="login-ruleForm">
      <el-form-item label="用户账号" prop="name">
        <el-input v-model="rule_form.name"></el-input>
      </el-form-item>

      <el-form-item label="用户密码" prop="pwd">
        <el-input type="password" v-model="rule_form.pwd"></el-input>
      </el-form-item>
    </el-form>

    <div class="login-button-class">
      <el-button type="success" @click="login">登录</el-button>
      <el-button type="danger" @click="register">注册</el-button>
    </div>
  </div>

</template>

<script>
  import {register,login} from "@/requests/user"
  import VueCookies from 'vue-cookies'

  export default {
    name: 'login',
    data () {
      return {
        rule_form:{
          name:'',
          pwd:'',
        },
        rules:{
          name:[
            {required:true,message:'请输入用户名',trigger:'blur'},
            {min:3,max:20,message:'长度在3到20个字符',trigger:'blur'}
          ],
          pwd:[
            {required:true,message:'请输入密码',trigger:'blur'},
            {min:3,max:20,message:'长度在3到20个字符',trigger:'blur'}
          ],
        }
      }
    },
    methods:{
      login(){
        this.$refs.ruleForm.validate((valid) => {
          if (valid) {
            login(this.rule_form.name,this.rule_form.pwd).then(data=>{
              if(true === data.success){
                //this.$message.info('login success')
                let session = data.data.session;
                VueCookies.set('token',session,1209600);
                console.log("cookie:",document.cookie);
                this.$router.push('/index')   //登录成功后重定向到首页，window.location='/index'也可以，但不如该方法快
              }else {
                this.$message.error('login failed')
              }
            })
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      register(){
        this.$refs.ruleForm.validate((valid) => {
          if (valid) {
            register(this.rule_form.name,this.rule_form.pwd).then(data=>{
              if(true === data.success){
                //this.$message.info('register success')
                let session = data.data.session;
                VueCookies.set('token',session,1209600);
                // console.log(document.cookie)
                this.$router.push('/index')   //注册成功后重定向到首页
              }else {
                this.$message.error('register failed')
              }
            })
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .login-main-context{
    width:400px;
    margin-left: auto;
    margin-right: auto;
    min-height: 100px;
    border: 1px solid black;
    padding: 20px 30px 20px 5px; /*分别为框的：上、右、下、左 四个位置*/
    border-radius: 5px;  /*框的边角改为圆角*/
    border:1px solid #a0b1c4;  /*框边的颜色*/
    margin-top: 50px;
  }

  .login-ruleForm{
    margin-top: 20px;
  }

  .login-button-class{
    display: flex;
    justify-content: space-between;
    padding-left: 25px;
  }

  .login-title{
    text-align: center;
  }
</style>
