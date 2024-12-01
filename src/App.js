import React, { useContext } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import HomePage from "./components/HomePage";
import LoginPage from "./components/LoginPage";
import RegisterPage from "./components/RegisterPage";
import ShopPage from "./components/ShopPage";
import RankingsPage from "./components/RankingsPage";
import FriendsPage from "./components/FriendsPage";
import { AuthContext, AuthProvider } from "./context/AuthContext";

const AppContent = () => {
  const { user, logout } = useContext(AuthContext); // AuthContext에서 상태 가져오기

  return (
    <>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "10px",
          borderBottom: "1px solid #ccc",
        }}
      >
        {/* 메뉴 버튼 */}
        <div>
          <button onClick={() => (window.location.href = "/")}>Home</button>
          <button
            onClick={() => (window.location.href = "/shop")}
            style={{ marginLeft: "10px" }}
          >
            Shop
          </button>
          <button
            onClick={() => (window.location.href = "/friends")}
            style={{ marginLeft: "10px" }}
          >
            Friends
          </button>
          <button
            onClick={() => (window.location.href = "/rankings")}
            style={{ marginLeft: "10px" }}
          >
            Rankings
          </button>
        </div>

        {/* 로그인 / 로그아웃 버튼 */}
        <div>
          {user ? (
            <>
              <span style={{ marginRight: "10px" }}>{user.username}</span>
              <button onClick={logout}>Logout</button>
            </>
          ) : (
            <button onClick={() => (window.location.href = "/login")}>
              Login
            </button>
          )}
        </div>
      </header>

      <Routes>
        {/* 메인 페이지 */}
        <Route path="/" element={<HomePage />} />

        {/* 로그인 페이지 */}
        <Route
          path="/login"
          element={!user ? <LoginPage /> : <Navigate to="/" />}
        />

        {/* 회원가입 페이지 */}
        <Route
          path="/register"
          element={!user ? <RegisterPage /> : <Navigate to="/" />}
        />

        {/* 상점 페이지 */}
        <Route
          path="/shop"
          element={user ? <ShopPage /> : <Navigate to="/login" />}
        />

        {/* 랭킹 페이지 */}
        <Route
          path="/rankings"
          element={user ? <RankingsPage /> : <Navigate to="/login" />}
        />

        {/* 친구 페이지 */}
        <Route
          path="/friends"
          element={user ? <FriendsPage /> : <Navigate to="/login" />}
        />

        {/* 기본 경로 */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
};

export default App;
