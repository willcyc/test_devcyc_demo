<template>
  <div class="services-main">
    <div class="services-tree">
      <el-button type="primary" size="small" @click="init_root_service">创建根服务</el-button>
      <el-tree
        class="tree-padding"
        :data="services_tree"
        :props="default_props"
        node-key="id"
        default-expand-all
        draggable
        @node-drop="drop_service"
        @node-click="select_service"
        :expand-on-click-node="false">
        <span class="custom-tree-node" slot-scope="{ node, data }">
          <span>{{ node.label }}</span>
          <el-dropdown trigger="click" @command="handle_command">
            <span class="el-dropdown-link">
              <i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item :command="{'ops':'add','data':data}">创建</el-dropdown-item>
              <el-dropdown-item :command="{'ops':'edit','data':data}">编辑</el-dropdown-item>
              <el-dropdown-item :command="{'ops':'delete','data':data}">删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </span>
      </el-tree>
    </div>

    <div class="interface-tree">
      <interface_list @update="update_service_interfaces" :interfaces="service_interfaces" :service_id="service_id"></interface_list>
    </div>

    <el-dialog
      :title="edit_service.title"
      :visible.sync="edit_service.dialog_visible"
      width="35%">
      <el-form :model="edit_service" label-width="80px" :rules="edit_service_rule" ref="edit_service"
               label-position="left">
        <el-form-item label="父节点" prop="parent" v-if="0 !== edit_service.parent">
          {{edit_service.parent_name}}
        </el-form-item>
        <el-form-item label="节点名称" prop="name">
          <el-input v-model="edit_service.name"></el-input>
        </el-form-item>
        <el-form-item label="节点描述" prop="description">
          <el-input type="textarea" :rows="3" v-model="edit_service.description"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="edit_service.dialog_visible = false">取 消</el-button>
        <el-button type="primary" @click="submit_form">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import {
    create_services,
    get_services_tree,
    update_services,
    delete_services,
    get_service_interfaces} from "../../requests/service";
  import interface_list from '../interface/interface_list'

  export default {
    name: 'services',
    components:{
      interface_list
    },
    data () {
      return {
        services_tree:[

        ],
        default_props: {
          label: 'name'
        },
        edit_service:{
          dialog_visible:false,

          mode:'add',
          title:'创建服务',

          id:-1,
          name:'',
          description:'',

          parent:0,
          parent_name:'',

        },
        edit_service_rule:{
          name:[
            {required:true,message:'请输入服务名称',trigger:'blur'},
            {min:3,max:30,message:'长度在3到30个字符',trigger:'blur'}
          ],
          description:[
            {required:true,message:'请输入服务描述',trigger:'blur'},
          ]
        },

        service_interfaces:[],
        service_id:1,
      }
    },

  methods:{
    get_services_fun(){
      get_services_tree().then(data=>{
        if(true === data.success){
          this.services_tree = data.data;
        }else{
          this.$message.error(data.message);
        }
      });
    },
    submit_form(){
      this.$refs.edit_service.validate((valid) => {
        if(valid){
          if('add' === this.edit_service.mode){
            this.add_service_req();
          }else{
            this.update_service_req();
          }
        }else {
          console.log('error submit!!');
          return false
        }
      })
    },

    handle_command(command){
      let ops = command.ops;
      let data = command.data;

      switch (ops) {
        case 'add':
          this.init_children_service(data);
          break;
        case 'edit':
          this.init_edit_service(data);
          break;
        case 'delete':
          this.init_delete_service(data);
          this.delete_service_req();
          break;
      }
    },

    init_root_service(){
      this.edit_service.dialog_visible = true;
      this.edit_service.mode = 'add';
      this.edit_service.name = "";
      this.edit_service.description = "";
      this.edit_service.title = "创建服务";
      this.edit_service.parent = 0;
      this.edit_service.parent_name = '';
      this.edit_service.id = -1;
    },

    init_children_service(parent_data){
      this.init_root_service();
      this.edit_service.parent = parent_data.id;
      this.edit_service.parent_name = parent_data.name;
    },

    init_delete_service(data){
      this.edit_service.id = data.id;
    },

    init_edit_service(data){
      this.edit_service.dialog_visible = true;
      this.edit_service.mode = 'edit';
      this.edit_service.name = data.name;
      this.edit_service.description = data.description;
      this.edit_service.title = "编辑节点";
      this.edit_service.parent = data.parent;
      this.edit_service.parent_name = data.parent_name;
      this.edit_service.id = data.id;
    },

    init_drop_service(data1,data2){
      this.edit_service.parent = data2.id;
      this.edit_service.id = data1.id;
      this.edit_service.name = data1.name;
      this.edit_service.description = data1.description;
    },

    add_service_req(){
      create_services(this.edit_service.name,this.edit_service.description,this.edit_service.parent).then(data=>{
        if (true === data.success){
          this.get_services_fun();
          this.edit_service.dialog_visible = false;
        }else {
          this.$message.error('创建失败！');
        }
      })
    },

    update_service_req(){
      update_services(this.edit_service.id,this.edit_service.name,this.edit_service.description,this.edit_service.parent).then(data=>{
        if (true === data.success){
          this.get_services_fun();
          this.edit_service.dialog_visible = false;
        }else {
          this.$message.error('编辑失败！');
        }
      })
    },

    delete_service_req(){

      this.$confirm('此操作将永久删除该节点, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delete_services(this.edit_service.id).then(data=>{
          if (true === data.success){
            this.get_services_fun();
          }else {
            this.$message.error('删除失败！');
          }
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });

    },

    drop_service(node1,node2,position,event){
      this.init_drop_service(node1.data,node2.data);
      this.update_service_req();
    },

    select_service(data){
      this.service_id = data.id;
      this.get_interfaces_func();
    },

    get_interfaces_func(){
      get_service_interfaces(this.service_id).then(data=>{
        if(true === data.success){
          this.service_interfaces = data.data;
        }
      });
    },

    update_service_interfaces(){
      this.get_interfaces_func();
    },
  },

  mounted() {
    this.get_services_fun();
  }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .services-main{
    display: flex;
  }

  .services-tree{
    width: 25%;
    border-right: solid 1px #e6e6e6;
    padding: 10px 10px 0 5px;
    min-height: 500px;
  }

  .tree-padding{
    padding-top: 10px;
  }

  .interface-tree{
    width: 75%;
    padding: 10px 5px 0 10px;
  }
</style>
