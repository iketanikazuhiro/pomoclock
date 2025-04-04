import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pomodoro Timer", layout="centered")

# Streamlitのデフォルトヘッダーを非表示にし、背景色を統一
st.markdown(
    """
    <style>
      header {visibility: hidden;}
      .stApp {
          background-color: #f0f0f0;
      }
      body {
          margin: 0;
          display: flex;
          align-items: center;
          justify-content: center;
          height: 100vh;
          background-color: #f0f0f0;
          font-family: sans-serif;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

html_code = """
<html>
<head>
  <style>
    /* コンテナ：時計とボタンを中央に配置 */
    #clock-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    canvas {
      background-color: #f0f0f0;
      border: none;
    }
    /* キャンバスとボタンの間に1行分の余白（必要なら調整） */
    #spacer {
      height: 1em;
    }
    /* ボタンコンテナ：横並びで中央揃え */
    #button-container {
      display: flex;
      justify-content: center;
      gap: 1em;
    }
    button {
      padding: 8px 16px;
      font-size: 1em;
      cursor: pointer;
      background: none;
      border: none;
      outline: none;
      /* 下線は各ボタンごとに個別で設定（JSで動的に変更） */
    }
  </style>
</head>
<body>
  <div id="clock-container">
    <canvas id="clock" width="350" height="350"></canvas>
    <div id="spacer"></div>
    <div id="button-container">
      <button id="start-btn" onclick="startTimer()" style="text-decoration: underline;">START</button>
      <button id="fs-btn" onclick="toggleFullScreen()">FullScreen</button>
      <button id="soundtest-btn" onclick="playSoundTest()">SoundTest</button>
    </div>
  </div>
  <!-- 音源：ここでは穏やかなbeep_short.oggを使用 -->
  <audio id="alert-sound" src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" preload="auto"></audio>
  <script>
    var elapsedSeconds = 0;
    var timerInterval = null;
    var timerStarted = false;

    var canvas = document.getElementById("clock");
    var ctx = canvas.getContext("2d");

    // 色設定
    var workColor = "#0D47A1"; // START後、作業セグメント0～25分に使用する紺色
    var defaultColor = "#000000"; // 初期状態およびその他は黒

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
      var radius = Math.min(width, height) / 2;
      var lineW = radius * 0.15;
      var effectiveRadius = radius - lineW / 2;

      ctx.clearRect(0, 0, width, height);
      ctx.save();
      ctx.translate(width/2, height/2);

      function minuteToAngle(min) {
        return (min * 6) * Math.PI / 180 - Math.PI/2;
      }

      ctx.lineWidth = lineW;

      // 作業セグメント1：0～25分
      ctx.beginPath();
      ctx.arc(0, 0, effectiveRadius, minuteToAngle(0), minuteToAngle(25), false);
      ctx.strokeStyle = timerStarted ? workColor : defaultColor;
      ctx.stroke();

      // 休憩セグメント1：25～30分
      ctx.beginPath();
      ctx.arc(0, 0, effectiveRadius, minuteToAngle(25), minuteToAngle(30), false);
      ctx.strokeStyle = defaultColor;
      ctx.stroke();

      // 作業セグメント2：30～55分
      ctx.beginPath();
      ctx.arc(0, 0, effectiveRadius, minuteToAngle(30), minuteToAngle(55), false);
      ctx.strokeStyle = defaultColor;
      ctx.stroke();

      // 休憩セグメント2：55～60分
      ctx.beginPath();
      ctx.arc(0, 0, effectiveRadius, minuteToAngle(55), minuteToAngle(60), false);
      ctx.strokeStyle = defaultColor;
      ctx.stroke();

      // 現在の経過時間に応じた分針の描画
      var cycleSeconds = 3600;
      var t = elapsedSeconds % cycleSeconds;
      var minutes = t / 60;
      var angle = minuteToAngle(minutes);

      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(effectiveRadius * 0.8 * Math.cos(angle), effectiveRadius * 0.8 * Math.sin(angle));
      ctx.lineWidth = 4;
      ctx.strokeStyle = "#555";
      ctx.stroke();

      // 中心のドット
      ctx.beginPath();
      ctx.arc(0, 0, 5, 0, 2 * Math.PI);
      ctx.fillStyle = "#555";
      ctx.fill();

      ctx.restore();
    }

    function updateTimer() {
      elapsedSeconds++;
      drawClock();
      // セグメントの節目でサウンドを鳴らす例（必要に応じて条件設定）
      // 例：START後25分の境目
      // if(elapsedSeconds == 25 * 60) { document.getElementById("alert-sound").play(); }
    }

    function startTimer() {
      elapsedSeconds = 0;
      timerStarted = true;
      if(timerInterval) { clearInterval(timerInterval); }
      timerInterval = setInterval(updateTimer, 1000);
      drawClock();
    }

    function toggleFullScreen() {
      if(!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        if(document.exitFullscreen) { document.exitFullscreen(); }
      }
    }

    function playSoundTest() {
      document.getElementById("alert-sound").play();
    }

    window.addEventListener("resize", drawClock);
    drawClock();
  </script>
</body>
</html>
"""

components.html(html_code, height=600)
