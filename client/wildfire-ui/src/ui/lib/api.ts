import axios from "axios"


export const API =
  axios.create({
    baseURL: "/api",
    withCredentials: true
  })


API.defaults.withCredentials = true;