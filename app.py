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
      background-color: #f0f0f0; /* 全体背景：明るめグレー */
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
    /* キャンバスとボタンの間に1行分の余白 */
    #spacer {
      height: 1em;
    }
    #button-container {
      margin-top: 0.5em;
      display: flex;
      justify-content: center;
      gap: 1em;
    }
    button {
      padding: 8px 16px;
      font-size: 1em;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div id="clock-container">
    <canvas id="clock" width="350" height="350"></canvas>
    <div id="spacer"></div>
    <div id="button-container">
      <button id="start-btn" onclick="startTimer()">START</button>
      <button id="fs-btn" onclick="toggleFullScreen()">FullScreen</button>
      <button id="soundtest-btn" onclick="playSoundTest()">SoundTest</button>
    </div>
  </div>
  <audio id="alert-sound" src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" preload="auto"></audio>
  <script>
    // タイマー状態変数
    var elapsedSeconds = 0;
    var timerInterval = null;
    var timerStarted = false;  // STARTを押すまで false

    var canvas = document.getElementById("clock");
    var ctx = canvas.getContext("2d");

    // 色の設定
    var workColor = "#0D47A1"; // START後の作業セグメント（0～25分）の紺色
    var defaultColor = "#000000"; // 初期状態は全て黒

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
      var radius = Math.min(width, height) / 2;
      var lineW = radius * 0.15;
      var effectiveRadius = radius - lineW / 2;

      ctx.clearRect(0, 0, width, height);
      ctx.save();
      ctx.translate(width/2, height/2);

      // 分を角度に変換する関数（0分＝上、-90°）
      function minuteToAngle(min) {
        return (min * 6) * Math.PI / 180 - Math.PI/2;
      }

      ctx.lineWidth = lineW;

      // 作業セグメント1：0～25分
      ctx.beginPath();
      ctx.arc(0, 0, effectiveRadius, minuteToAngle(0), minuteToAngle(25), false);
      // タイマー開始済みなら作業セグメントを紺色、それ以外は黒
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

      // 現在の経過時間に合わせた分針の描画
      var cycleSeconds = 3600; // 1サイクル＝60分
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

    // タイマー更新
    function updateTimer() {
      elapsedSeconds++;
      // 各節目到来時にサウンドアラートを鳴らす例（ここでは0～25分の開始のみ）
      // ※ 実装例：例えば25分に差し掛かったときに再生など、必要に応じて条件を調整してください
      // if(elapsedSeconds == 25*60) { document.getElementById("alert-sound").play(); }
      drawClock();
    }

    // STARTボタン：タイマーをゼロから開始し、タイマー状態を変更
    function startTimer() {
      elapsedSeconds = 0;
      timerStarted = true;
      if(timerInterval) { clearInterval(timerInterval); }
      timerInterval = setInterval(updateTimer, 1000);
      drawClock();
    }

    // FullScreenボタン
    function toggleFullScreen() {
      if(!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        if(document.exitFullscreen) { document.exitFullscreen(); }
      }
    }

    // SoundTestボタン
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
