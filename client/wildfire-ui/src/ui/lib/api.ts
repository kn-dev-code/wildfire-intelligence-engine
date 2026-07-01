import axios from "axios"


export const API =
  axios.create({
    baseURL: "http://localhost:8000",
    withCredentials: true
  })


API.defaults.withCredentials = true;