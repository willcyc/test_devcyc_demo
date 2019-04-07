import {post_code,put_code,get_code,delete_code} from "./common";
const services_path = 'interface/services/';

// 获取服务的树形结构
export const get_services_tree = function () {
  return get_code(services_path)
};

//创建服务
export const create_services = function (name,description,parent) {
  return post_code(services_path,{name:name,description:description,parent:parent})
};

//更新服务
export const update_services = function (service_id,name,description,parent) {
  return put_code(services_path + service_id,{name:name,description:description,parent:parent})
};

//删除服务
export const delete_services = function (service_id) {
  return delete_code(services_path + service_id)
};

//获取某个服务下面的服务接口列表
export const get_service_interfaces = function (service_id) {
  return get_code(services_path + service_id + '/interfaces')
}
