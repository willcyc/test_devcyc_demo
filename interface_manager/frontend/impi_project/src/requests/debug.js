import {post_code} from "./common";
const user_path = 'interface/debug/';
export const debug = function (data) {
  return post_code(user_path,data)
};

