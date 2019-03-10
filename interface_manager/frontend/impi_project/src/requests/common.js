import VueCookies from "vue-cookies";

export const host='http://127.0.0.1:8000/';

export const post_code = function(url,params){
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

export const put_code = function(url,params){
  let body = JSON.stringify(params);
  return fetch(host + url,{
    method:'PUT',
    body:body,
    credentials:"include",   //fetch函数中带上cookie值
    headers:{
      'token':VueCookies.get('token'),   //前端在请求的时候，把session放在headers
    }
  }).then(response =>{
    return response.json()
  })
};

export const get_code = function(url){
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
