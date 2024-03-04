import axios from 'axios';
import { z } from 'zod';
import { env } from '~/src/env';

interface TokenResponse {
  access_token: string,
  token_type: string,
}

export const LoginSchema = z.object({
  username: z.string().email({
    message: "Invalid email.",
  }),
  password: z.string().min(8, {
    message: "Password must be at least 8 character",
  }),
});

export const RegisterSchema = z.object({
  type: z.union([z.literal("user"), z.literal("teacher")]),
  name: z.string().min(5, {
    message: "Your name must be at least 5 character",
  }),
  email: z.string().email({
    message: "Invalid email.",
  }),
  password: z.string().min(8, {
    message: "Password must be at least 8 character",
  }),
});

const api = axios.create({
  baseURL: env.NEXT_PUBLIC_BACKEND_URL
});

export async function login(data: z.infer<typeof LoginSchema>): Promise<boolean> {
  try {
    const formData = new FormData();
    formData.append('username', data.username)
    formData.append('password', data.password)
  
    const response = await api.post<TokenResponse>('/login', formData);
  
    if (response.status == 200) {
      localStorage.setItem('token', response.data.access_token);
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
    return false;
  }
}

export async function register(data: z.infer<typeof RegisterSchema>): Promise<boolean> {
  try {
    const response = await api.post<TokenResponse>('/register', data);
    
    if (response.status == 200) {
      localStorage.setItem('token', response.data.access_token);
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
    return false;
  }
}