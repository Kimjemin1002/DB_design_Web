import React, { useState, useEffect } from "react";
import axios from "axios";

const RankingsPage = () => {
  const [rankings, setRankings] = useState([]);

  const fetchRankings = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/top-rankings"
      ); // Updated API endpoint for top 10 rankings
      setRankings(response.data.rankings);
    } catch (error) {
      console.error("Error fetching rankings:", error);
    }
  };

  useEffect(() => {
    fetchRankings();
  }, []);

  return (
    <div>
      <h1>Top 10 Rankings</h1>
      <ol>
        {rankings.map((player, index) => (
          <li key={player.id}>
            {index + 1}. {player.username} - {player.points} points
          </li>
        ))}
      </ol>
    </div>
  );
};

export default RankingsPage;
