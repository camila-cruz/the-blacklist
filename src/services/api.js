import axios from 'axios';

const api = axios.create({
    baseURL: process.env.REACT_APP_BASE_URL,
    // baseURL: 'http://localhost:5000/',
});

export default api;