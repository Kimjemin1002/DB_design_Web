import React, { createContext, useState, useEffect } from "react";
import axios from "../api/axios";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // 사용자 상태
  const [loading, setLoading] = useState(true); // 로딩 상태

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    const token = localStorage.getItem("userToken");

    if (storedUser && token) {
      // 로컬 스토리지에서 사용자 정보와 토큰 가져오기
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      setUser(JSON.parse(storedUser));
    }
    setLoading(false); // 로딩 상태 해제
  }, []);

  const logout = () => {
    // 로그아웃 시 상태와 로컬 스토리지 초기화
    localStorage.removeItem("user");
    localStorage.removeItem("userToken");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, setUser, loading, logout }}>
      {!loading && children} {/* 로딩 중일 때는 화면을 렌더링하지 않음 */}
    </AuthContext.Provider>
  );
};
