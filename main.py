import streamlit as st
from google import genai
from google.genai import types

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
    st.write("「外は凍えるような寒さですね。まずは、あなたのことを少しだけ教えていただけますか？」")
    
    # 流れ1：出会いと今の空気感
    q0 = st.radio("0. 散歩の途中で見つけたカフェ。もし空いていたら、どこに座りたいですか？", ["店の一番奥の落ち着く席", "店内が見渡せるカウンター席", "窓際の明るいテーブル席"], index=None)
    q1 = st.radio("1. ようこそ。今夜のこのお店、明かりはどのくらいが心地よいですか？", ["少し落とした静かな暗がり", "暖炉のような温かい光", "キラキラしたキャンドルの光"], index=None)
    
    # 流れ2：冬の情緒（季節の雑談）
    q2 = st.radio("2. 窓の外で雪が降り始めました。それを見て、どう感じられますか？", ["「静まり返る世界に浸りたい」", "「暖かい家が恋しくなる」", "「少し特別な気分でワクワクする」"], index=None)
    q3 = st.radio("3. 冬の香りで、心にふっと残る好きなものはありますか？", ["薪が燃える煙の匂い", "焼きたてのパンの香り", "爽やかなシトラスの香り"], index=None)
    
    # 流れ3：おうちでの過ごし方（プライベートへの入り口）
    q4 = st.radio("4. 冬の夜、お手元に置きたい本はどんなものですか？", ["じっくり読み耽る長編ミステリー", "心が温まる優しいエッセイ", "ページを捲るのが楽しい華やかな画集"], index=None)
    q5 = st.radio("5. もし冬の休日、自分を存分に甘やかすなら何をしましょう？", ["誰にも邪魔されず一人で瞑想", "大切な友人とゆっくりお喋り", "お気に入りの服を着てお出かけ"], index=None)
    q6 = st.radio("6. お部屋のインテリア。どこに一番のこだわりを持っていますか？", ["重厚なアンティークの机", "飽きのこないシンプルなソファ", "お部屋を彩るお花やアート"], index=None)
    q7 = st.radio("7. お部屋でのルームウェア。一番重視するのはどこですか？", ["守られているような安心感", "動きやすさとリラックス感", "鏡を見た時に嬉しくなるデザイン"], index=None)
    
    # 流れ4：あなたの内面（深い性格や習慣）
    q8 = st.radio("8. 普段、周りの方からはどんな性格だと言われることが多いですか？", ["「ミステリアスで芯が強い」", "「穏やかで親しみやすい」", "「明るくて華がある」"], index=None)
    q9 = st.radio("9. 大切な約束がある時。何分くらい前に到着されることが多いでしょう？", ["10分前には落ち着いていたい", "ちょうど良い時間に着きたい", "楽しみにしすぎて早く着きすぎる"], index=None)
    
    # 流れ5：理想の姿（バリスタとしての視点）
    q10 = st.radio("10. もしあなたがバリスタなら、どんなお店を作ってみたいですか？", ["隠れ家のような静かな店", "誰でも気軽に立ち寄れる店", "センスのいいお洒落な店"], index=None)

    submitted = st.form_submit_button("バリスタに結果を伝える")
    
#DEBUG_MODE = True
DEBUG_MODE = False

if submitted:
    if DEBUG_MODE:#markdownでは、半角スペース2つで改行、改行で段落になる
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
        user_input = f"回答結果: {q0}, {q1}, {q2}, {q3}, {q4}, {q5}, {q6}, {q7}, {q8}, {q9}, {q10}"
        
        with st.spinner('そうですねえ...'):
            # 1. 位置調整用のカラム作成 [左余白, 画像本体, 右余白]
            # [1, 2, 1] なら中央、[0.1, 3.8, 0.1] ならほぼ全幅になります
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                # 2. 画像の表示とサイズ調整
                # widthで横幅を指定（ピクセル単位）。お好みの大きさに変えてください
                st.image("おじ１.png", width=100)

            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.7,
                    ),
                    contents=user_input
                )
                st.success("診断完了です…！")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                # もしここでも404が出るなら、APIキー側の設定に問題があります
                st.error(f"エラーが発生しました: {e}")
                st.info("AI Studioで『Create API key in NEW project』を選択して、新しいプロジェクトでキーを作り直してみてください。")


