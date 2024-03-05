import axios, { AxiosHeaders } from 'axios';
import { env } from '~/src/env';

// axios.interceptors.request.use(
//   (config) => {
//     const token = localStorage.getItem('token');
//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`;
//     }
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

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