import type { LoginType, RegisterType } from "../types/user/user-types";
import {useQuery, useMutation, useQueryClient} from "@tanstack/react-query"
import { API } from "../ui/lib/api";

export type UpdateType = {
username?: string;
email?: string;
password?: string;
role?: User["role"];
}

interface User {
  _id: string;
  username: string;
  email: string;
  password?: string;
  isLoggingIn: false;
  isRegistering: false;
  role: 'user' | 'admin'
}

{/* Admin Functions Only */}

export const useGetAllUsers = () => {
  return useQuery<User[]>({
    queryKey: ['users', 'list'],
    queryFn: async() => {
      const {data} = await API.get('/get-all-users')
      return data
    }
  })
}

export const useDeleteAllUsers = () => {
  const queryClient = useQueryClient(); 
  return useMutation({
    mutationFn: async () => {
      const { data } = await API.delete('/delete-all-users');
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users', 'list'] });
    }
  });
};

export const useUpdateAllUsers = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async() => {
      const {data} = await API.patch('/update-all-users');
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({queryKey: ['users', 'list']})
    }
  })
}



{/* User Functions Only */}
export const useRegisterUser = () => {
  return useMutation({
    mutationFn: async (credentials: RegisterType) => {
      const {data} = await API.post("/register", credentials)
      return data;
    }
  })
}

export const useLogUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async(credentials: LoginType) => {
      const {data} = await API.post("/login", credentials)
      return data;
    },
    onSuccess: (userData) => {
      queryClient.setQueryData(['users', 'profile'], userData)
    }
  })
}

export const useUpdateUser = (userId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async(credentials: UpdateType) => {
      const {data} = await API.patch(`/update/${userId}`, credentials)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({queryKey: ['users', 'profile']})
    }
  })
}

// isUpdating, isLoggingOut, isSigningUp, isLoggingIn
// isModelPredicting, isRetrieving