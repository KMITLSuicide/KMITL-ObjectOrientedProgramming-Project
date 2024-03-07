import axios, { AxiosHeaders } from 'axios';
import { env } from '~/src/env';

function getHeaders(): AxiosHeaders {
  if (typeof window !== 'undefined') {
    const token = window.localStorage.getItem('token');
    if (token) {
      const headers: AxiosHeaders = new AxiosHeaders({
        'Authorization': `Bearer ${token}`
      })
      return headers;
    }
  }
  return new AxiosHeaders();
}



const api = axios.create({
  baseURL: env.NEXT_PUBLIC_BACKEND_URL,
  headers: getHeaders()
});

export default api;