import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="140字書いて投稿するFocusScribe", layout="wide")

# Streamlit全体の背景色をグレーに設定するCSS
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
      overflow: hidden;
      background-color: #f0f0f0; /* 明るめのグレー */
      font-family: sans-serif;
    }
    /* コンテナは画面全体を占め、中央揃え */
    #editor-container {
      width: 100%;
      height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    /* アプリタイトル（FocusScribe）：入力欄の上部に配置 */
    #app-title {
      font-size: 2em;
      color: #555;
      margin-bottom: 0.5em;
    }
    /* テキストエリア：横22.5%、縦25vh */
    #editor {
      width: 22.5%;
      height: 25vh;
      font-size: 1.2em;
      line-height: 1.5em;
      padding: 1em;
      border: none;
      resize: none;
      overflow: auto;
      background-color: #f0f0f0;
    }
    #editor:focus {
      outline: none;
      box-shadow: none;
    }
    /* ボタンコンテナ：入力欄と同じ幅、等間隔に中央揃え */
    #button-container {
      width: 22.5%;
      margin-top: 0.5em;
      display: flex;
      justify-content: space-evenly;
    }
    /* STARTボタン（全画面切替用）：初期状態は下線付き */
    #fullscreen-btn {
      padding: 0.5em 1em;
      font-size: 1em;
      background: none;
      border: none;
      color: #555;
      cursor: pointer;
      text-decoration: underline;
    }
    /* POSTおよびCLEARボタン：下線なし */
    #share-btn, #clear-btn {
      padding: 0.5em 1em;
      font-size: 1em;
      cursor: pointer;
      background: none;
      border: none;
      color: #555;
      text-decoration: none;
    }
    /* 残り文字数表示：ボタン列の下に配置 */
    #char-count {
      margin-top: 2em;
      font-size: 1em;
      color: #555;
    }
    /* モバイル向けの調整 */
    @media (max-width: 600px) {
      #editor {
        width: 90%;
        height: 20vh;
      }
      #button-container {
        width: 90%;
      }
    }
  </style>
</head>
<body>
  <div id="editor-container">
    <div id="app-title">FocusScribe</div>
    <textarea id="editor"></textarea>
    <div id="button-container">
      <button id="fullscreen-btn" onclick="toggleFullScreen()">START</button>
      <button id="share-btn" onclick="shareToTwitter()">POST</button>
      <button id="clear-btn" onclick="clearEditor()">CLEAR</button>
    </div>
    <div id="char-count">あと 140 字</div>
  </div>
  <script>
    const editor = document.getElementById("editor");
    const charCount = document.getElementById("char-count");
    const fullscreenBtn = document.getElementById("fullscreen-btn");
    const shareBtn = document.getElementById("share-btn");
    const appTitle = document.getElementById("app-title");
    const maxChars = 140;
    
    // 初期状態設定：STARTボタンに下線付き
    fullscreenBtn.style.textDecoration = "underline";
    
    // 残り文字数を更新する関数
    function updateCharCount() {
      const count = editor.value.length;
      const remaining = maxChars - count;
      if (remaining >= 0) {
        charCount.textContent = "あと " + remaining + " 字";
        charCount.style.color = "#555";
      } else {
        charCount.textContent = "+ " + (-remaining) + " 字";
        charCount.style.color = "red";
      }
    }
    
    // 入力イベントで文字カウント更新と自動スクロール
    editor.addEventListener("input", function() {
      updateCharCount();
      let height = editor.clientHeight;
      editor.scrollTop = editor.scrollHeight - height;
    });
    
    // ツイッターへのシェア処理
    function shareToTwitter() {
      let text = editor.value;
      if (!text) {
        alert("投稿するテキストが空です。");
        return;
      }
      let twitterUrl = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(text);
      window.open(twitterUrl, "_blank");
    }
    
    // CLEARボタンで入力欄をクリアする処理
    function clearEditor() {
      editor.value = "";
      updateCharCount();
    }
    
    // 全画面切替処理
    function toggleFullScreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }
    
    // 全画面状態の変化に合わせたボタンとタイトルの表示更新
    document.addEventListener("fullscreenchange", () => {
      if (document.fullscreenElement) {
        fullscreenBtn.textContent = "OFF";
        fullscreenBtn.style.textDecoration = "none";
        shareBtn.style.textDecoration = "underline";
        appTitle.style.display = "none";
        editor.focus();
      } else {
        fullscreenBtn.textContent = "START";
        fullscreenBtn.style.textDecoration = "underline";
        shareBtn.style.textDecoration = "none";
        appTitle.style.display = "block";
      }
    });
    
    updateCharCount();
  </script>
</body>
</html>
"""

components.html(html_code, height=600)
