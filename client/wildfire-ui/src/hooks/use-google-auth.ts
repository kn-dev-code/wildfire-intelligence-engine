import { API } from "../ui/lib/api"


export const googleLoginAuth = async(credentials: string) => {
  try {
    const response = await API.post("/api/v1/users/google-auth", {
    credentials: credentials
  })
  return response.data;
  } catch(e) {
    console.error(`API ERROR: ${e}`)
  }
}

