import axios from 'axios';

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_FUNCTIONS_BASE_URL || process.env.REACT_APP_BASE_URL,
    // baseURL: process.env.REACT_APP_BASE_URL,
    // baseURL: 'http://localhost:5000/',
});

export default api;