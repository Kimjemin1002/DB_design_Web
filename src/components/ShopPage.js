import React, { useEffect, useState } from "react";
import axios from "axios";

const ShopPage = () => {
  const [items, setItems] = useState([]); // 아이템 목록 상태
  const [error, setError] = useState(""); // 에러 메시지 상태
  const [message, setMessage] = useState(""); // 성공 메시지 상태

  const fetchItems = async () => {
    const token = localStorage.getItem("userToken");
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/shop-items", {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      if (response.status === 200) {
        setItems(response.data.items);
      } else {
        setError("Failed to load items.");
      }
    } catch (error) {
      setError(error.response?.data?.message || "An error occurred.");
    }
  };

  const purchaseItem = async (itemId) => {
    const token = localStorage.getItem("userToken");
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/purchase-item",
        { item_id: itemId },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
        }
      );
      if (response.status === 200) {
        setMessage(response.data.message);
        fetchItems(); // 구매 후 데이터 새로고침
      }
    } catch (error) {
      setError(error.response?.data?.message || "Failed to purchase item.");
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Shop</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {message && <p style={{ color: "green" }}>{message}</p>}
      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px" }}>
        {items.length > 0 ? (
          items.map((item) => (
            <div
              key={item.id}
              style={{
                border: "1px solid #ccc",
                borderRadius: "10px",
                padding: "10px",
                width: "200px",
              }}
            >
              <h3>{item.name}</h3>
              <p>{item.description}</p>
              <p>Price: {item.base_price} points</p>
              <button onClick={() => purchaseItem(item.id)}>Buy</button>
            </div>
          ))
        ) : (
          <p>No items available in the shop.</p>
        )}
      </div>
    </div>
  );
};

export default ShopPage;
