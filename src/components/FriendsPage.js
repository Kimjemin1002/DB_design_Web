import React, { useState, useEffect } from "react";
import axios from "axios";

const FriendsPage = () => {
  const [friends, setFriends] = useState([]);
  const [friendId, setFriendId] = useState("");

  const fetchFriends = async () => {
    try {
      const response = await axios.get("/api/friends"); // Django API 호출
      setFriends(response.data.friends);
    } catch (error) {
      console.error("Error fetching friends:", error);
    }
  };

  const addFriend = async () => {
    try {
      const response = await axios.post("/api/add-friend", {
        friend_id: friendId,
      });
      alert(response.data.message);
      setFriendId(""); // 입력 필드 초기화
      fetchFriends(); // 친구 추가 후 다시 목록 업데이트
    } catch (error) {
      console.error("Error adding friend:", error);
    }
  };

  useEffect(() => {
    fetchFriends();
  }, []);

  return (
    <div>
      <h1>Friends</h1>
      <div>
        <h3>Add Friend</h3>
        <input
          type="text"
          placeholder="Enter Friend ID"
          value={friendId}
          onChange={(e) => setFriendId(e.target.value)}
        />
        <button onClick={addFriend}>Add</button>
      </div>
      <ul>
        {friends.map((friend) => (
          <li key={friend.id}>
            {friend.username} - {friend.points} points
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FriendsPage;
