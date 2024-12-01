import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8000"; // 백엔드 API 기본 URL

axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("userToken");
    if (token) {
      config.headers.Authorization = `Token ${token}`; // Token 형식으로 수정
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default axios;
