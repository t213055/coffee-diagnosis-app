import streamlit as st
from google import genai
from google.genai import types
import os
# --- [重要] 新しいAPIキーをここに貼り付けてください ---
API_KEY = st.secrets["GEMINI_API_KEY"]

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
# main.py の st.title の上あたりに追加
st.markdown("""
    <style>
    .main {
        background-color: #f5f5dc; /* カフェのようなベージュ色 */
    }
    .stButton>button {
        background-color: #4b2c20; /* コーヒーブラウン */
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("☕ AI性格診断バリスタ")

with st.form("diagnosis_form"):
    q1 = st.radio("1. 休日の過ごし方は？", ["家で静かに読書", "友人とわいわい", "新しい場所へ冒険"])
    q2 = st.radio("2. 好きなファッションは？", ["シックで落ち着いた服", "カジュアルで親しみやすい服", "個性的で華やかな服"])
    q10 = st.radio("10. 今、どんな刺激がほしい？", ["静寂と集中", "日常の癒やし", "新しい発見"])
    submitted = st.form_submit_button("診断を開始する")

if submitted:
    user_input = f"回答結果: {q1}, {q2}, {q10}"
    
    with st.spinner('バリスタが計算中...'):
        try:
            # 修正ポイント: model名を 'gemini-1.5-flash' に固定
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

