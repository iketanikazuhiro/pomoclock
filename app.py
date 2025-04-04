import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pomodoro Clock", layout="centered")

# Streamlit全体の背景を設定
st.markdown(
    """
    <style>
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
      background-color: #f0f0f0; /* 背景：明るめのグレー */
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    canvas {
      background-color: #f0f0f0;
      /* 枠線など不要なら削除 */
    }
  </style>
</head>
<body>
  <canvas id="clock" width="300" height="300"></canvas>
  <script>
    // 時計の描画処理
    function drawClock() {
      var canvas = document.getElementById("clock");
      if (canvas.getContext) {
        var ctx = canvas.getContext("2d");
        var width = canvas.width;
        var height = canvas.height;
        var radius = width / 2;
        // 中心に移動
        ctx.translate(radius, radius);
        radius = radius * 0.90;
        
        // 背景をクリア
        ctx.clearRect(-canvas.width/2, -canvas.height/2, canvas.width, canvas.height);
        
        // 外周の白い円（時計のベース）
        ctx.beginPath();
        ctx.arc(0, 0, radius, 0, 2 * Math.PI);
        ctx.fillStyle = "#ffffff";
        ctx.fill();
        
        // 関数：分を角度（ラジアン）に変換
        // 時計では0分が上（-90°）になるよう調整
        function minuteToAngle(min) {
          return (min * 6) * Math.PI / 180 - Math.PI/2;
        }
        
        // セグメントを描画
        // 作業セグメント：緑系（例：#a0d468）、休憩セグメント：赤系（例：#ed5565）
        
        // 作業1：0～25分
        ctx.beginPath();
        ctx.arc(0, 0, radius, minuteToAngle(0), minuteToAngle(25), false);
        ctx.lineWidth = 15;
        ctx.strokeStyle = "#a0d468";
        ctx.stroke();
        
        // 休憩1：25～30分
        ctx.beginPath();
        ctx.arc(0, 0, radius, minuteToAngle(25), minuteToAngle(30), false);
        ctx.strokeStyle = "#ed5565";
        ctx.stroke();
        
        // 作業2：30～55分
        ctx.beginPath();
        ctx.arc(0, 0, radius, minuteToAngle(30), minuteToAngle(55), false);
        ctx.strokeStyle = "#a0d468";
        ctx.stroke();
        
        // 休憩2：55～60分
        ctx.beginPath();
        ctx.arc(0, 0, radius, minuteToAngle(55), minuteToAngle(60), false);
        ctx.strokeStyle = "#ed5565";
        ctx.stroke();
        
        // 現在の時刻の分針を描画
        var now = new Date();
        // 分と秒を考慮して、現在の分を小数で計算
        var min = now.getMinutes() + now.getSeconds() / 60;
        var angle = minuteToAngle(min);
        
        // 分針の描画（長さはradiusの80%）
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(radius * 0.8 * Math.cos(angle), radius * 0.8 * Math.sin(angle));
        ctx.lineWidth = 6;
        ctx.strokeStyle = "#555";
        ctx.stroke();
        
        // 中心の小さなドット
        ctx.beginPath();
        ctx.arc(0, 0, 5, 0, 2 * Math.PI);
        ctx.fillStyle = "#555";
        ctx.fill();
        
        // 毎回translateでずれないようにリセット
        ctx.setTransform(1, 0, 0, 1, 0, 0);
      }
    }
    
    // 初回描画
    drawClock();
    // 1秒ごとに更新
    setInterval(drawClock, 1000);
  </script>
</body>
</html>
"""

components.html(html_code, height=350)
