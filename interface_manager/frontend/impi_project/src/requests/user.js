import {post_code,put_code,get_code} from "./common";
const user_path = 'interface/user';
export const register = function (name,pwd) {
  return post_code(user_path,{username:name,password:pwd})
};

export const login = function (name,pwd) {
  return put_code(user_path,{username:name,password:pwd})
};

export const get_user = function () {
  return get_code(user_path)
};

// export const register = function (name,pwd) {
//   return fetch(host + 'interface/user/register',{
//     method:'POST',
//     body:JSON.stringify({name:name,pwd:pwd})
//   }).then(response =>{
//     return response.json()
//   })
// }
//
// export const login = function (name,pwd) {
//   return fetch(host + 'interface/user/login',{
//     method:'POST',
//     body:JSON.stringify({name:name,pwd:pwd})
//   }).then(response =>{
//     return response.json()
//   })
// }
