import React, { useState, useEffect } from "react";
import axios from "axios";
import coinImageDefault from "./images/coin.jpg"; // 기본 동전 이미지
import coinHeadImage from "./images/coin_head.png"; // HEADS 이미지
import coinTailImage from "./images/coin_tail.png"; // TAILS 이미지

const HomePage = () => {
  const [probability, setProbability] = useState(50); // 기본 성공 확률
  const [userPoints, setUserPoints] = useState(0); // 현재 포인트
  const [result, setResult] = useState(""); // 결과 메시지
  const [currentImage, setCurrentImage] = useState(coinImageDefault); // 현재 동전 이미지
  const [isFlipping, setIsFlipping] = useState(false); // 동전 애니메이션 상태

  // 초기 데이터 가져오기
  useEffect(() => {
    fetchGameData();
  }, []);

  // 공통 요청 헤더 생성
  const getAuthHeaders = () => {
    const token = localStorage.getItem("userToken");
    console.log("Token used in request:", token); // 디버깅 로그
    if (!token) {
      setResult("No token found. Please log in again.");
      return null;
    }
    return {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    };
  };

  // 백엔드에서 성공 확률 및 사용자 포인트 가져오기
  const fetchGameData = async () => {
    const token = localStorage.getItem("userToken");
    console.log("Token being sent:", `Token ${token}`); // 디버깅 로그

    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/get-game-data",
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`, // "Token" 형식을 유지
          },
        }
      );
      console.log("Response:", response.data);
      setUserPoints(response.data.ranking.points);
      setProbability(response.data.probability);
    } catch (error) {
      console.error("Error fetching game data:", error);
    }
  };

  // API 요청 오류 처리 함수
  const handleApiError = (error, context) => {
    if (error.response && error.response.status === 401) {
      console.error(`Authentication failed while ${context}.`);
      setResult("Authentication failed. Please log in again.");
    } else {
      console.error(`Error occurred while ${context}:`, error);
      setResult("An error occurred. Please try again later.");
    }
  };

  // 동전 던지기 함수
  const flipCoin = async () => {
    console.log("Coin flip initiated"); // 함수 호출 여부 확인
    setIsFlipping(true); // 애니메이션 시작
    setCurrentImage(coinImageDefault); // 기본 동전 이미지 설정
    setResult(""); // 이전 결과 초기화

    setTimeout(async () => {
      const headers = getAuthHeaders();
      if (!headers) {
        setIsFlipping(false);
        return;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/flip-coin",
          {}, // POST 요청에 빈 데이터 전송
          { headers }
        );

        if (response.status === 200) {
          console.log("a:", response.data);
          // 성공 여부에 따라 이미지 및 메시지 설정
          setCurrentImage(
            response.data.result.result == "HEADS"
              ? coinHeadImage
              : coinTailImage
          );
          setResult(
            response.data.result.result == "HEADS" ? "성공!" : "실패..."
          );
          setUserPoints(response.data.ranking.points); // 포인트 업데이트
          setProbability(response.data.probability);
          console.log("Response received:", response.data); // 디버깅 로그
          fetchGameData();
        } else {
          console.error("Unexpected response:", response.status);
          setResult("Unexpected error occurred.");
        }
      } catch (error) {
        console.error("Error during coin flip:", error);
        handleApiError(error, "flipping coin");
      } finally {
        setIsFlipping(false); // 애니메이션 종료
      }
    }, 2000); // 애니메이션 지연
  };

  return (
    <div
      style={{
        textAlign: "center",
        marginTop: "50px",
      }}
    >
      <h2>현재 확률: {probability}%</h2>
      <h3>현재 포인트: {userPoints}점</h3>
      <img
        src={currentImage}
        alt="Coin"
        style={{
          width: "150px",
          cursor: isFlipping ? "not-allowed" : "pointer", // 애니메이션 중 클릭 비활성화
          transition: "transform 2s",
          transform: isFlipping ? "rotateY(360deg)" : "none", // 회전 애니메이션
        }}
        onClick={!isFlipping ? flipCoin : null} // 애니메이션 중 중복 클릭 방지
      />
      <p>{result}</p>
    </div>
  );
};

export default HomePage;
