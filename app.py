import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pomodoro Timer", layout="centered")

# ヘッダーなどStreamlitデフォルトの上部エリアを非表示にするCSS
st.markdown(
    """
    <style>
    header {visibility: hidden;}
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
      background-color: #f0f0f0; /* 明るめグレー */
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
    <canvas id="clock" width="300" height="300"></canvas>
    <div id="button-container">
      <button id="start-btn" onclick="startTimer()">START</button>
      <button id="fs-btn" onclick="toggleFullScreen()">FullScreen</button>
    </div>
  </div>
  <script>
    // タイマー変数
    var elapsedSeconds = 0;
    var timerInterval = null;
    
    // キャンバス取得とコンテキスト
    var canvas = document.getElementById("clock");
    var ctx = canvas.getContext("2d");
    
    // 色の設定
    var workColor = "#1E88E5"; // 明るい紺色（作業セグメント）
    var breakColor = "#000000"; // 黒（休憩セグメント）
    
    // 時計描画関数（タイマーに合わせて描画）
    function drawClock() {
      // 全画面時はキャンバスサイズを調整
      if(document.fullscreenElement) {
        canvas.width = window.innerWidth * 0.5;
        canvas.height = window.innerWidth * 0.5;
      } else {
        canvas.width = 300;
        canvas.height = 300;
      }
      var width = canvas.width;
      var height = canvas.height;
      var radius = Math.min(width, height) / 2;
      
      // 描画前にクリア
      ctx.clearRect(0, 0, width, height);
      ctx.save();
      ctx.translate(width/2, height/2);
      
      // 現在の経過時間を1サイクル（60分＝3600秒）に対して計算
      var cycleSeconds = 3600;
      var t = elapsedSeconds % cycleSeconds;
      var minutes = t / 60;
      
      // 分を角度に変換する関数（0分が上部＝-90°）
      function minuteToAngle(min) {
        return (min * 6) * Math.PI / 180 - Math.PI/2;
      }
      
      // セグメント描画
      ctx.lineWidth = radius * 0.15;
      
      // 作業セグメント1：0～25分（明るい紺）
      ctx.beginPath();
      ctx.arc(0, 0, radius, minuteToAngle(0), minuteToAngle(25), false);
      ctx.strokeStyle = workColor;
      ctx.stroke();
      
      // 休憩セグメント1：25～30分（黒）
      ctx.beginPath();
      ctx.arc(0, 0, radius, minuteToAngle(25), minuteToAngle(30), false);
      ctx.strokeStyle = breakColor;
      ctx.stroke();
      
      // 作業セグメント2：30～55分（明るい紺）
      ctx.beginPath();
      ctx.arc(0, 0, radius, minuteToAngle(30), minuteToAngle(55), false);
      ctx.strokeStyle = workColor;
      ctx.stroke();
      
      // 休憩セグメント2：55～60分（黒）
      ctx.beginPath();
      ctx.arc(0, 0, radius, minuteToAngle(55), minuteToAngle(60), false);
      ctx.strokeStyle = breakColor;
      ctx.stroke();
      
      // 現在の経過時間を示す分針の描画
      var angle = minuteToAngle(minutes);
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(radius * 0.8 * Math.cos(angle), radius * 0.8 * Math.sin(angle));
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
    
    // タイマー更新関数（1秒ごとに呼ばれる）
    function updateTimer() {
      elapsedSeconds++;
      drawClock();
    }
    
    // STARTボタン押下時：タイマーをリセットしてスタート
    function startTimer() {
      elapsedSeconds = 0;
      if(timerInterval) {
        clearInterval(timerInterval);
      }
      timerInterval = setInterval(updateTimer, 1000);
      drawClock();
    }
    
    // FullScreenボタンのトグル処理
    function toggleFullScreen() {
      if(!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        if(document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }
    
    // ウィンドウサイズ変更時に再描画
    window.addEventListener("resize", drawClock);
    
    // 初期描画
    drawClock();
  </script>
</body>
</html>
"""

components.html(html_code, height=600)
