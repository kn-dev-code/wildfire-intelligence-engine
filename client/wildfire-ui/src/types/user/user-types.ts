

export type RegisterType = {
  username: string;
  email: string;
  password: string;
}

export type LoginType = {
  email: string;
  password: string;
}

export interface UserType {
username: string;
email: string;
password: string;
is_active: boolean;
}
