import streamlit as st
from google import genai
from google.genai import types

# --- [重要] APIキーを設定 ---
API_KEY = st.secrets["GEMINI_API_KEY"]
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
    .stApp { background-color: #fdf5e6 !important; }
    .stHeading h1 {
        color: #4b2c20 !important;
        font-family: 'Hiragino Mincho ProN', 'serif';
        text-align: center;
    }
    div.stButton > button {
        background-color: #6f4e37 !important;
        color: white !important;
        border-radius: 20px !important;
        width: 100% !important;
    }
    .stForm {
        border: 2px solid #d3b19a !important;
        background-color: white;
        padding: 20px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.image("cafe_image.png", use_container_width=True)
st.title("☕ 性格診断バリスタ")

with st.form("diagnosis_form"):
    st.write("「外は凍えるような寒さですね。まずは、あなたのことを少しだけ教えていただけますか？」")
    
    q0 = st.radio("0. 散歩の途中で見つけたカフェ。もし空いていたら、どこに座りたいですか？", ["店の一番奥の落ち着く席", "店内が見渡せるカウンター席", "窓際の明るいテーブル席"], index=None)
    q1 = st.radio("1. ようこそ。今夜のこのお店、明かりはどのくらいが心地よいですか？", ["少し落とした静かな暗がり", "暖炉のような温かい光", "キラキラしたキャンドルの光"], index=None)
    q2 = st.radio("2. 窓の外で雪が降り始めました。それを見て、どう感じられますか？", ["「静まり返る世界に浸りたい」", "「暖かい家が恋しくなる」", "「少し特別な気分でワクワクする」"], index=None)
    q3 = st.radio("3. 冬の香りで、心にふっと残る好きなものはありますか？", ["薪が燃える煙の匂い", "焼きたてのパンの香り", "爽やかなシトラスの香り"], index=None)
    q4 = st.radio("4. 冬の夜、お手元に置きたい本はどんなものですか？", ["じっくり読み耽る長編ミステリー", "心が温まる優しいエッセイ", "ページを捲るのが楽しい華やかな画集"], index=None)
    q5 = st.radio("5. もし冬の休日、自分を存分に甘やかすなら何をしましょう？", ["誰にも邪魔されず一人で瞑想", "大切な友人とゆっくりお喋り", "お気に入りの服を着てお出かけ"], index=None)
    q6 = st.radio("6. お部屋のインテリア。どこに一番のこだわりを持っていますか？", ["重厚なアンティークの机", "飽きのこないシンプルなソファ", "お部屋を彩るお花やアート"], index=None)
    q7 = st.radio("7. お部屋でのルームウェア。一番重視するのはどこですか？", ["守られているような安心感", "動きやすさとリラックス感", "鏡を見た時に嬉しくなるデザイン"], index=None)
    q8 = st.radio("8. 普段、周りの方からはどんな性格だと言われることが多いですか？", ["「ミステリアスで芯が強い」", "「穏やかで親しみやすい」", "「明るくて華がある」"], index=None)
    q9 = st.radio("9. 大切な約束がある時。何分くらい前に到着されることが多いでしょう？", ["10分前には落ち着いていたい", "ちょうど良い時間に着きたい", "楽しみにしすぎて早く着きすぎる"], index=None)
    q10 = st.radio("10. もしあなたがバリスタなら、どんなお店を作ってみたいですか？", ["隠れ家のような静かな店", "誰でも気軽に立ち寄れる店", "センスのいいお洒落な店"], index=None)

    submitted = st.form_submit_button("バリスタに結果を伝える")

DEBUG_MODE = False

if submitted:
    # 未回答チェック
    answers = [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    if None in answers:
        st.warning("「申し訳ありません、まだお聞きできていない項目があるようです。もう少しだけ、お話を聞かせていただけますか？」")
    else:
        if DEBUG_MODE:
            st.success("【テスト中】診断完了！")
            st.markdown("""
            1.【あなたの性格タイプ】 落ち着いた読書家  
            2.【性格の分析】 一人の時間を大切にする深い思考の持ち主です。  
            3.【本日のおすすめ】 ブラジル  
            4.【抽出のこだわり】 低温でじっくり。  
            5.【バリスタの一言】 素敵な読書タイムを。  
            """)
        else:
            user_input = f"回答結果: {q0}, {q1}, {q2}, {q3}, {q4}, {q5}, {q6}, {q7}, {q8}, {q9}, {q10}"
            
            # 1. まず「空の器（placeholder）」を一つだけ作る
            image_placeholder = st.empty()

            # 2. その器の中に、考え中のバリスタを表示する
            with image_placeholder:
                # この「中」でレイアウト用のカラムを作るのがコツです
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image("おじ１.png", width=300)

            with st.spinner('そうですねえ...'):
                try:
                    # API呼び出し
                    response = client.models.generate_content(
                        model='gemini-2.5-flash', 
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.7,
                        ),
                        contents=user_input
                    )

                    # 3. 診断完了！画像を入れた器（placeholder）を丸ごと書き換える
                    with image_placeholder:
                        c1, c2, c3 = st.columns([1, 2, 1])
                        with c2:
                            st.image("おじ３.png", width=300)
                    
                    st.success("診断完了です…！")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")