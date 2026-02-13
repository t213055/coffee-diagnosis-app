import streamlit as st
from google import genai
from google.genai import types

# --- [重要] 新しいAPIキーをここに貼り付けてください ---
API_KEY = "AIzaSyAOLISt18dbhA9qr-Ta0dK-Uyo6xwn8Qrg"

# 最新のクライアント設定
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
あなたは性格診断バリスタです。ユーザーの回答から性格タイプを定義し、
「マンデリン・ブラジル・モカ」の中から1つを選んでください。
性別不問の表現を用い、以下のフォーマットで出力してください。
1.【あなたの性格タイプ】
2.【性格の分析】
3.【本日のおすすめ】
4.【抽出のこだわり】
5.【バリスタの一言】
"""

st.set_page_config(page_title="Coffee Diagnosis", page_icon="☕")
# --- [UI装飾] カフェ風カスタムCSS ---
st.markdown("""
    <style>
    /* 全体の背景色を温かみのあるベージュに */
    .stApp {
        background-color: #fdf5e6 !important;
    }
    /* タイトルの文字色をコーヒーブラウンに */
    .stHeading h1 {
        color: #4b2c20 !important;
        font-family: 'Hiragino Mincho ProN', 'serif';
        text-align: center;
        padding-bottom: 20px;
    }
    /* 診断ボタンをコーヒー色に */
    div.stButton > button {
        background-color: #6f4e37 !important;
        color: white !important;
        border-radius: 20px !important;
        height: 3em !important;
        width: 100% !important;
    }
    /* 4. ボタンにマウスを乗せた時（ホバー）の色も変えると本格的です */
    div.stButton > button:hover {
        background-color: #4b2c20 !important;
        color: #fdf5e6 !important;
    }
    /* フォームの枠線を少しお洒落に */
    .stForm {
        border: 2px solid #d3b19a !important;
        background-color: white;
        padding: 20px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ヘッダー画像を入れる（あれば）
st.image("cafe_image.png", use_container_width=True)
st.title("☕ 性格診断バリスタ")
st.write("バリスタとの会話の中で、あなたにおすすめの一杯を提供します")

with st.form("diagnosis_form"):
    q0 = st.radio("1. 休日の過ごし方は？", ["家で静かに読書", "友人とわいわい", "新しい場所へ冒険"])

    submitted = st.form_submit_button("バリスタに結果を伝える")
    
DEBUG_MODE = True

if submitted:
    if DEBUG_MODE:
        # UIテスト用のダミー回答(APIを消費しない)
        st.success("【テスト中】診断完了！")
        st.markdown("""
        1.【あなたの性格タイプ】 落ち着いた読書家
        2.【性格の分析】 一人の時間を大切にする深い思考の持ち主です。
        3.【本日のおすすめ】 ブラジル
        4.【抽出のこだわり】 低温でじっくり。
        5.【バリスタの一言】 素敵な読書タイムを。
        """)
    else:
        user_input = f"回答結果: {q0}"
        
        with st.spinner('バリスタが計算中...'):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.7,
                    ),
                    contents=user_input
                )
                st.success("診断完了！")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                # もしここでも404が出るなら、APIキー側の設定に問題があります
                st.error(f"エラーが発生しました: {e}")
                st.info("AI Studioで『Create API key in NEW project』を選択して、新しいプロジェクトでキーを作り直してみてください。")
