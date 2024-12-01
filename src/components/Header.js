import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false); // 메뉴 상태
  const navigate = useNavigate();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <header
      style={{
        display: "flex",
        justifyContent: "space-between",
        padding: "10px",
        borderBottom: "1px solid #ccc",
        position: "relative",
      }}
    >
      {/* 메뉴 버튼 (왼쪽 위) */}
      <div style={{ position: "relative", display: "inline-block" }}>
        <button onClick={toggleMenu}>Menu</button>
        {menuOpen && (
          <div
            className="menu-dropdown"
            style={{
              position: "absolute",
              top: "100%",
              left: "0",
              backgroundColor: "#fff",
              border: "1px solid #ccc",
              borderRadius: "4px",
              zIndex: 1000,
              width: "150px",
            }}
          >
            <ul style={{ listStyleType: "none", padding: "10px", margin: 0 }}>
              <li>
                <button
                  style={{ width: "100%", textAlign: "left" }}
                  onClick={() => navigate("/")}
                >
                  Main Page
                </button>
              </li>
              <li>
                <button
                  style={{ width: "100%", textAlign: "left" }}
                  onClick={() => navigate("/shop")}
                >
                  Shop
                </button>
              </li>
              <li>
                <button
                  style={{ width: "100%", textAlign: "left" }}
                  onClick={() => navigate("/friends")}
                >
                  Friends List
                </button>
              </li>
              <li>
                <button
                  style={{ width: "100%", textAlign: "left" }}
                  onClick={() => navigate("/rankings")}
                >
                  Rankings
                </button>
              </li>
            </ul>
          </div>
        )}
      </div>

      {/* 로그인 버튼 (오른쪽 위) */}
      <button
        onClick={() => navigate("/login")}
        style={{ alignSelf: "flex-end" }}
      >
        Login
      </button>
    </header>
  );
};

export default Header;
