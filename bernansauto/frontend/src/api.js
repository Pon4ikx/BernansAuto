import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  withCredentials: true,
});

const getCookie = (name) => {
  const matches = document.cookie.match(new RegExp(`(?:^|; )${name.replace(/([.$?*|{}()[\]\\/+^])/g, '\\$1')}=([^;]*)`));
  return matches ? decodeURIComponent(matches[1]) : '';
};

api.interceptors.request.use((config) => {
  const method = (config.method || 'get').toLowerCase();
  const isSafeMethod = ['get', 'head', 'options', 'trace'].includes(method);
  if (!isSafeMethod) {
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
  }
  return config;
});
