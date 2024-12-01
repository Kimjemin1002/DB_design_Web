import React, { useState, useContext } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext"; // 인증 상태 관리 Context

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { setUser, setToken } = useContext(AuthContext); // 인증 상태 업데이트 함수

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login", {
        email,
        password,
      });

      console.log("Login response:", response.data);

      const { user, token } = response.data; // 토큰 포함 여부 확인
      if (user && token) {
        localStorage.setItem("user", JSON.stringify(user)); // 사용자 정보 저장
        localStorage.setItem("userToken", token); // 토큰 저장
        alert("Login successful!");
        navigate("/"); // 홈으로 리디렉션
      } else {
        setError("Login failed. User data or token is missing.");
      }
    } catch (error) {
      console.error("Login error:", error);

      if (error.response) {
        setError(error.response.data.message || "Login failed.");
      } else if (error.request) {
        setError("No response from server. Please try again later.");
      } else {
        setError("An unexpected error occurred.");
      }
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        textAlign: "center",
      }}
    >
      <h1>Login</h1>
      <form onSubmit={handleLogin} style={{ width: "300px" }}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ marginBottom: "10px", width: "100%" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ marginBottom: "10px", width: "100%" }}
        />
        <button type="submit" style={{ width: "100%" }}>
          Login
        </button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button
        onClick={() => navigate("/register")}
        style={{ marginTop: "10px" }}
      >
        Go to Register
      </button>
    </div>
  );
};

export default LoginPage;
