
import axios from "axios";
export const key = "78505cc75524121e1571c6dc86a1ec14c1a6aa4d";

const api = axios.create({
    baseURL: 'https://api-ssl.bitly.com/v4/',
    headers:{
        'Authorization': `Bearer ${key}` 
    }
 })

 export default api;