# 直接HTMLを挿入してアニメーション背景とアプリコンテンツを一緒に表示
WAVE_BACKGROUND_HTML_CSS = """
<!DOCTYPE html>
<html>
<head>
<style>
    
    /* 背景アニメーションのスタイルを設定する場合、これをcssとして設定。背景はbodyに含める。*/
    body::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #4973ff;
        z-index: -1;
    }
    
    .wave-animation {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: #4973ff;
        overflow: hidden;
    }
    
    .wave-animation span {
        position: absolute;
        width: 325vh;
        height: 325vh;
        top: 0;
        left: 50%;
        transform: translate(-50%, -75%);
    }
    
    .wave-animation span:nth-child(1) {
        border-radius: 45%;
        background: rgba(20, 20, 20, 1);
        animation: wave-rotate 20s linear infinite;
    }
    
    .wave-animation span:nth-child(2) {
        border-radius: 40%;
        background: rgba(20, 20, 20, 0.5);
        animation: wave-rotate 40s linear infinite;
    }
    
    .wave-animation span:nth-child(3) {
        border-radius: 42.5%;
        background: rgba(20, 20, 20, 0.5);
        animation: wave-rotate 60s linear infinite;
    }
    
    @keyframes wave-rotate {
        0% {
            transform: translate(-50%, -75%) rotate(0deg);
        }
        100% {
            transform: translate(-50%, -75%) rotate(360deg);
        }
    }
    
</style>
</head>
<body>
    <div class="wave-animation">
        <span></span>
        <span></span>
        <span></span>
    </div>
</body>
</html>
"""

# Streamlitメイン機能の透明か化, 背景を表示できるように調整, チャットUIを半透明の背景で表示
MAIN_APP_CONTENTS_CSS = """
<style>
    /* 上部バーを透明に */
    header {
        background-color: transparent !important;
    }
            
    /* Streamlitコンテンツのスタイル調整 */
    .stApp {
        background: transparent !important;
    }
            
    .stAppViewMain {
        background-color: transparent !important;
    }
    .stMainBlockContainer {
        background-color: transparent !important;
        padding-top: 0rem; /* 上部の余白を削除 */
    }
    .stAppViewBlockContainer {
        background-color: transparent !important;
        padding-top: 0rem; /* 上部の余白を削除 */
    }
    /* ヘッダーを非表示に */
    header {visibility: hidden;}
    
    
    /* フッターを透明に */
    footer {
        background-color: transparent !important;
    }

    /* チャットメッセージ内のすべてのテキスト要素を白色に */
    header,
    .stChatMessage p, 
    .stChatMessage span, 
    .stChatMessage div, 
    .stChatMessage h1, 
    .stChatMessage h2, 
    .stChatMessage h3, 
    .stChatMessage h4, 
    .stChatMessage h5, 
    .stChatMessage h6, 
    .stChatMessage li, 
    .stChatMessage a {
        color: rgba(0,0,0,0.95) !important;
    }
</style>
"""
# color: rgba(255, 255, 255, 0.95) !important;

# チャット機能に関するCSS
CHAT_MESSAGE_CSS = """      
<style>                
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0) !important;
        margin: 10px 20px !important;
        border-radius: 20px !important;
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* ユーザーのアバターを非表示 */
    [data-testid="stChatMessageAvatarUser"] {
        display: none;
    }
    /* User Message */       
    .st-emotion-cache-1c7y2kd {
        animation: messageAppear 1.0s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-left: 20rem !important;
        display: flex;
        background-color: rgba(30,30,30,0.06) !important;
        flex-direction: row-reverse;
        align-items: end;
        text-align: left;
    }
    /* AI Message */
    .st-emotion-cache-4oy321 {
        color: rgba(255, 255, 255, 0.95) !important;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none;
    }
    
    /* 上のanimation属性に対応するメッセージが表示されるアニメーション */
    @keyframes messageAppear {
        0% { opacity: 0; transform: translateY(20px) scale(0.95); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
            
    /* チャットインプットメッセージのボックスを透明に。2つ指定する必要ある。 */
    .st-emotion-cache-qdbtli, .st-emotion-cache-128upt6 {
        background-color: transparent !important;
    }
    
    .stChatInput {
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        background-color: #fff !important;
        color: #333;
        padding: 16px 10px !important;
    }

    .stChatInput *{
        border: none !important;
        background-color: #fff !important;
    }


    /* アイコンボタンっぽいものに適用するなら（例: 検索・音声） */
    .stChatInput button {
        border: none;
        border-radius: 50%;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        transition: background-color 0.2s;
        margin-right: .8em;
    }

    .stChatInput button:hover {
        background-color: #f0f0f0;
    }
    .st-emotion-cache-sey4o0 {
        z-index: 1000;
    }

</style>
"""

# /* サイドバーのスタイリング */
SIDEBAR_CSS = """      
<style>                
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 350px;
        max-width: 350px;
    }
    [data-testid="stSidebar"] {
        background-color: rgb(240,244,250) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
"""

# /* 洗練されたヘッダー効果 */
# [data-testid="stHeader"] {
#     background-color: rgba(0, 0, 0, 0.3) !important;
#     backdrop-filter: blur(10px) !important;
#     border-bottom: 1px solid rgba(255, 255, 255, 0.05);
#     box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
# }

# <div class="st-emotion-cache-128upt6 ea3mdgi6"><div data-testid="stBottomBlockContainer" class="st-emotion-cache-qdbtli ea3mdgi2"><div data-testid="stVerticalBlockBorderWrapper" data-test-scroll-behavior="normal" class="st-emotion-cache-0 e1f1d6gn0"><div class="st-emotion-cache-1wmy9hl e1f1d6gn1"><div width="474" data-testid="stVerticalBlock" class="st-emotion-cache-jqs80i e1f1d6gn2"><div data-stale="false" width="474" class="element-container st-emotion-cache-18i1yyl e1f1d6gn4" data-testid="element-container"><div class="stChatInput st-emotion-cache-10ceb0g e1d2x3se4" data-testid="stChatInput" width="474"><div class="st-emotion-cache-s1k4sy e1d2x3se3"><div data-baseweb="textarea" class="st-ae st-af st-ag st-ah st-ai st-aj st-ak st-al st-am st-an st-ao st-ap st-aq st-ar st-as st-at st-au st-av st-aw st-ax st-ay st-az st-b0 st-b1 st-b2 st-b3 st-b4 st-b5"><div data-baseweb="base-input" class="st-af st-b6 st-b7 st-ar st-as st-b8 st-b9 st-ba st-bb st-bc st-bd st-be st-b1"><textarea aria-label="メッセージを入力してください..." aria-invalid="false" aria-required="false" autocomplete="on" inputmode="text" name="" placeholder="メッセージを入力してください..." type="textarea" rows="1" data-testid="stChatInputTextArea" class="st-ae st-b1 st-bf st-bg st-bh st-bi st-bj st-bk st-bl st-bm st-b5 st-b6 st-bn st-bo st-bp st-bq st-br st-bs st-bt st-bu st-b8 st-b9 st-ba st-bv st-bc st-bd st-be st-bw st-bx st-by st-bz st-c5" style=""></textarea></div></div><div class="st-emotion-cache-1lm6gnd e1d2x3se0"><div data-testid="InputInstructions" class="st-emotion-cache-1li7dat e1y5xkzn1"></div></div><div class="st-emotion-cache-f4ro0r e1d2x3se1"><button data-testid="stChatInputSubmitButton" class="st-emotion-cache-1up18o9 e1d2x3se2" disabled=""><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp53 st-emotion-cache-1f3w014 ex0cdmw0"><rect width="24" height="24" fill="none"></rect><path d="M3 5.51v3.71c0 .46.31.86.76.97L11 12l-7.24 1.81c-.45.11-.76.51-.76.97v3.71c0 .72.73 1.2 1.39.92l15.42-6.49c.82-.34.82-1.5 0-1.84L4.39 4.58C3.73 4.31 3 4.79 3 5.51z"></path></svg></button></div></div></div></div></div></div></div></div></div>

# <div data-testid="stBottomBlockContainer" class="st-emotion-cache-qdbtli ea3mdgi2"><div data-testid="stVerticalBlockBorderWrapper" data-test-scroll-behavior="normal" class="st-emotion-cache-0 e1f1d6gn0"><div class="st-emotion-cache-1wmy9hl e1f1d6gn1"><div width="474" data-testid="stVerticalBlock" class="st-emotion-cache-jqs80i e1f1d6gn2"><div data-stale="false" width="474" class="element-container st-emotion-cache-18i1yyl e1f1d6gn4" data-testid="element-container"><div class="stChatInput st-emotion-cache-10ceb0g e1d2x3se4" data-testid="stChatInput" width="474"><div class="st-emotion-cache-s1k4sy e1d2x3se3"><div data-baseweb="textarea" class="st-ae st-af st-ag st-ah st-ai st-aj st-ak st-al st-am st-an st-ao st-ap st-aq st-ar st-as st-at st-au st-av st-aw st-ax st-ay st-az st-b0 st-b1 st-b2 st-b3 st-b4 st-b5"><div data-baseweb="base-input" class="st-af st-b6 st-b7 st-ar st-as st-b8 st-b9 st-ba st-bb st-bc st-bd st-be st-b1"><textarea aria-label="メッセージを入力してください..." aria-invalid="false" aria-required="false" autocomplete="on" inputmode="text" name="" placeholder="メッセージを入力してください..." type="textarea" rows="1" data-testid="stChatInputTextArea" class="st-ae st-b1 st-bf st-bg st-bh st-bi st-bj st-bk st-bl st-bm st-b5 st-b6 st-bn st-bo st-bp st-bq st-br st-bs st-bt st-bu st-b8 st-b9 st-ba st-bv st-bc st-bd st-be st-bw st-bx st-by st-bz st-c5" style=""></textarea></div></div><div class="st-emotion-cache-1lm6gnd e1d2x3se0"><div data-testid="InputInstructions" class="st-emotion-cache-1li7dat e1y5xkzn1"></div></div><div class="st-emotion-cache-f4ro0r e1d2x3se1"><button data-testid="stChatInputSubmitButton" class="st-emotion-cache-1up18o9 e1d2x3se2" disabled=""><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp53 st-emotion-cache-1f3w014 ex0cdmw0"><rect width="24" height="24" fill="none"></rect><path d="M3 5.51v3.71c0 .46.31.86.76.97L11 12l-7.24 1.81c-.45.11-.76.51-.76.97v3.71c0 .72.73 1.2 1.39.92l15.42-6.49c.82-.34.82-1.5 0-1.84L4.39 4.58C3.73 4.31 3 4.79 3 5.51z"></path></svg></button></div></div></div></div></div></div></div></div>
# st-emotion-cache-qdbtli ea3mdgi2"><div data-testid="stVerticalBlockBorderWrapper" data-test-scroll-behavior="normal" class="st-emotion-cache-0 e1f1d6gn0"><div class="st-emotion-cache-1wmy9hl e1f1d6gn1"><div width="474" data-testid="stVerticalBlock" class="st-emotion-cache-jqs80i e1f1d6gn2"><div data-stale="false" width="474" class="element-container st-emotion-cache-18i1yyl e1f1d6gn4" data-testid="element-container"><div class="stChatInput st-emotion-cache-10ceb0g e1d2x3se4" data-testid="stChatInput" width="474"><div class="st-emotion-cache-s1k4sy e1d2x3se3"><div data-baseweb="textarea" class="st-ae st-af st-ag st-ah st-ai st-aj st-ak st-al st-am st-an st-ao st-ap st-aq st-ar st-as st-at st-au st-av st-aw st-ax st-ay st-az st-b0 st-b1 st-b2 st-b3 st-b4 st-b5"><div data-baseweb="base-input" class="st-af st-b6 st-b7 st-ar st-as st-b8 st-b9 st-ba st-bb st-bc st-bd st-be st-b1"><textarea aria-label="メッセージを入力してください..." aria-invalid="false" aria-required="false" autocomplete="on" inputmode="text" name="" placeholder="メッセージを入力してください..." type="textarea" rows="1" data-testid="stChatInputTextArea" class="st-ae st-b1 st-bf st-bg st-bh st-bi st-bj st-bk st-bl st-bm st-b5 st-b6 st-bn st-bo st-bp st-bq st-br st-bs st-bt st-bu st-b8 st-b9 st-ba st-bv st-bc st-bd st-be st-bw st-bx st-by st-bz st-c1"></textarea></div></div><div class="st-emotion-cache-1lm6gnd e1d2x3se0"><div data-testid="InputInstructions" class="st-emotion-cache-1li7dat e1y5xkzn1"></div></div><div class="st-emotion-cache-f4ro0r e1d2x3se1"><button disabled="" data-testid="stChatInputSubmitButton" class="st-emotion-cache-1up18o9 e1d2x3se2"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" class="eyeqlp53 st-emotion-cache-1f3w014 ex0cdmw0"><rect width="24" height="24" fill="none"></rect><path d="M3 5.51v3.71c0 .46.31.86.76.97L11 12l-7.24 1.81c-.45.11-.76.51-.76.97v3.71c0 .72.73 1.2 1.39.92l15.42-6.49c.82-.34.82-1.5 0-1.84L4.39 4.58C3.73 4.31 3 4.79 3 5.51z"></path></svg></button></div></div></div></div></div></div></div></div>

# [data-testid="stBottom"] {
#     /*background-color: transparent !important;*/
#     background-color: #fff;
# }


# [data-testid="stBottomBlockContainer"] {
#     /*background-color: transparent !important;*/
#     background-color: #fff;
# }

# .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) {
    # display: flex;
    # flex-direction: row-reverse;
    # align-itmes: end;
# }

# /* 洗練されたヘッダー効果 */
# [data-testid="stHeader"] {
#     background-color: rgba(0, 0, 0, 0.3) !important;
#     backdrop-filter: blur(10px) !important;
#     border-bottom: 1px solid rgba(255, 255, 255, 0.05);
#     box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
# }

# /* サイドバーのスタイリング */
# [data-testid="stSidebar"] {
#     background-color: rgba(0, 0, 0, 0.3) !important;
#     backdrop-filter: blur(10px) !important;
#     border-right: 1px solid rgba(255, 255, 255, 0.05);
# }

# .stChatMessage:hover {
#     transform: translateY(-3px) !important;
#     box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25) !important;
#     border: 1px solid rgba(255, 255, 255, 0.15) !important;
#     background: linear-gradient(135deg, rgba(20, 20, 35, 0.8), rgba(40, 40, 70, 0.8)) !important;
# }
# .stChatInputContainer {
#         background-color: rgba(255, 255, 255, 0.8) !important;
#         margin: 10px 20px !important;
#         border-radius: 10px !important;
#         padding: 10px !important;
#     }
