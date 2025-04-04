import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pomodoro Timer", layout="centered")

# Streamlitのデフォルトヘッダーなどを非表示にし、背景色を統一
st.markdown(
    """
    <style>
      header {visibility: hidden;}
      .stApp {
          background-color: #f0f0f0;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

html_code = """
<html>
<head>
  <style>
    body {
      margin: 0;
      background-color: #f0f0f0; /* 全体背景 */
      font-family: sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
    }
    #clock-container {
      text-align: center;
    }
    canvas {
      background-color: #f0f0f0;
      border: none;
    }
    #button-container {
      margin-top: 10px;
    }
    button {
      padding: 8px 16px;
      margin: 0 10px;
      font-size: 1em;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div id="clock-container">
    <canvas id="clock" width="350" height="350"></canvas>
    <div id="button-container">
      <button id="start-btn" onclick="startTimer()">START</button>
      <button id="fs-btn" onclick="toggleFullScreen()">FullScreen</button>
      <button id="soundtest-btn" onclick="playSoundTest()">SoundTest</button>
    </div>
  </div>
  <audio id="alert-sound" src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" preload="auto"></audio>
  <script>
    // タイマー変数
    var elapsedSeconds = 0;
    var timerInterval = null;
    
    var canvas = document.getElementById("clock");
    var ctx = canvas.getContext("2d");
    
    // 色の設定
    var workColor = "#1E88E5"; // 明るい紺色（作業セグメント）
    var breakColor = "#000000"; // 黒（休憩セグメント）
    
    // 時計描画関数
    function drawClock() {
      // 全画面の場合、キャンバスサイズをウィンドウ幅の50%に調整
      if(document.fullscreenElement) {
        canvas.width = window.innerWidth * 0.5;
        canvas.height = window.innerWidth * 0.5;
      } else {
        canvas.width = 350;
        canvas.height = 350;
      }
      
      var width = canvas.width;
      var height = canvas.height;
      // 半径と描画エリア（ライン幅の半分分の余白を確保）
      var radius = Math.min(width, height) / 2;
      var lineW = radius * 0.15;
      var effectiveRadius = radius - lineW / 2;
      
      // 画面クリア＆中心に移動
      ctx.clearRect(0, 0, width, height);
      ctx.save();
      ctx.translate(width/2, height/2);
      
      // 分を角度に変換する関数（0分＝上、-90°）
      function minuteToAngle(min) {
        return (min * 6) * Math.PI / 180 - Math.PI/2;
      }
      
      ctx.lineWidth = lineW;
      
      // 作業セグメント1：0～25分（明るい紺）
      ctx.beginPath();
      ctx.arc(0, 0, effectiveRadius, minuteToAngle(0), minuteToAngle(25), false);
      ctx.strokeStyle = workColor;
      ctx.stroke();
      
      // 休憩セグメント1：25～30分（黒）
      ctx.beginPath();
      ctx.arc(0, 0, effectiveRadius, minuteToAngle(25), minuteToAngle(30), false);
      ctx.strokeStyle = breakColor;
      ctx.stroke();
      
      // 作業セグメント2：30～55分（明るい紺）
      ctx.beginPath();
      ctx.arc(0, 0, effectiveRadius, minuteToAngle(30), minuteToAngle(55), false);
      ctx.strokeStyle = workColor;
      ctx.stroke();
      
      // 休憩セグメント2：55～60分（黒）
      ctx.beginPath();
      ctx.arc(0, 0, effectiveRadius, minuteToAngle(55), minuteToAngle(60), false);
      ctx.strokeStyle = breakColor;
      ctx.stroke();
      
      // 現在の経過時間に応じた分針の描画
      var cycleSeconds = 3600; // 1サイクル=60分
      var t = elapsedSeconds % cycleSeconds;
      var minutes = t / 60;
      var angle = minuteToAngle(minutes);
      
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(effectiveRadius * 0.8 * Math.cos(angle), effectiveRadius * 0.8 * Math.sin(angle));
      ctx.lineWidth = 4;
      ctx.strokeStyle = "#555";
      ctx.stroke();
      
      // 中心ドット
      ctx.beginPath();
      ctx.arc(0, 0, 5, 0, 2 * Math.PI);
      ctx.fillStyle = "#555";
      ctx.fill();
      
      ctx.restore();
    }
    
    // タイマー更新
    function updateTimer() {
      elapsedSeconds++;
      drawClock();
    }
    
    // STARTボタン：タイマーをゼロから開始
    function startTimer() {
      elapsedSeconds = 0;
      if(timerInterval) {
        clearInterval(timerInterval);
      }
      timerInterval = setInterval(updateTimer, 1000);
      drawClock();
    }
    
    // FullScreen切替
    function toggleFullScreen() {
      if(!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        if(document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }
    
    // SoundTestボタンで音を再生
    function playSoundTest() {
      document.getElementById("alert-sound").play();
    }
    
    // ウィンドウサイズ変更で再描画
    window.addEventListener("resize", drawClock);
    
    // 初期描画
    drawClock();
  </script>
</body>
</html>
"""

components.html(html_code, height=600)
