import VueCookies from "vue-cookies";

let host='http://127.0.0.1:8000/';

let post_code = function(url,params){
  let body = JSON.stringify(params);
  return fetch(host + url,{
    method:'POST',
    body:body,
    credentials:"include",   //fetch函数中带上cookie值
    headers:{
      'token':VueCookies.get('token'),   //前端在请求的时候，把session放在headers
    }
  }).then(response =>{
    return response.json()
  })
};

let get_code = function(url){
  return fetch(host + url,{
    method:'GET',
    credentials:"include",  //fetch函数中带上cookie值
    headers:{
      'token':VueCookies.get('token'),  // 前端在请求的时候，把session放在header
    }
  }).then(response =>{
    return response.json()
  })
};

export const register = function (name,pwd) {
  return post_code('interface/user/register',{name:name,pwd:pwd})
};

export const login = function (name,pwd) {
  return post_code('interface/user/login',{name:name,pwd:pwd})
};

export const get_user = function () {
  return get_code('interface/user/get')
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
