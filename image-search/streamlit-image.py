import streamlit as st
import os
import random
import time
from PIL import Image

css = """
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    
    /* 必要に応じて以下も追加できます */
    # MainMenu {visibility: hidden;}
    # header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""

# カスタムCSSを適用
st.markdown(css, unsafe_allow_html=True)

# 検索対象の画像ファイルが格納されたフォルダパス
IMAGE_DIR = "images"

# 検索対象の画像ファイルリストを生成
def get_image_files():
    image_files = []
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_files.append(os.path.join(IMAGE_DIR, filename))
    return image_files

# 類似画像を擬似的に検索する関数（5秒の処理をシミュレート）
def search_similar_images(uploaded_image, image_files, num_results=5):
    
    import time
    with st.spinner("Wait for it..."):
        time.sleep(2)    
    random.shuffle(image_files)
    return image_files[:num_results]

# 擬似的なJSON情報を生成する関数
def generate_fake_json(image_path):
    return {
        "filename": os.path.basename(image_path),
        "size": os.path.getsize(image_path),
        "timestamp": time.time(),
        "random_value": random.randint(1, 100)
    }

def main():
    st.title("画像検索アプリ")

    # サイドバーの横幅を狭く設定
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            width: 200px !important; # 幅を200pxに設定（調整可能）
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # サイドバーに画像アップロード機能を追加
    uploaded_file = st.sidebar.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # st.write(uploaded_file)
        # アップロードされた画像を表示
        image = Image.open(uploaded_file)
        
        st.subheader("アップロードした画像")
        col1, col2 = st.columns([1, 2])  # 列の幅を調整
        with col1:
            st.image(image, caption="アップロードされた画像", use_column_width=True)
        with col2:
            fake_json = generate_fake_json("/Users/ryoyakatafuchi/Desktop/streamlit-claude/images/1_page_0008_idx_0037.png")
            st.json(fake_json)

        # 検索対象の画像ファイルリストを取得
        image_files = get_image_files()

        # 類似画像を検索（擬似的な処理と進捗表示）
        subtitle = st.empty()
        subtitle.subheader("検索中...")
        similar_images = search_similar_images(uploaded_file, image_files)

        # 検索結果を表示
        subtitle.subheader("検索結果")
        for img_path in similar_images:
            col1, col2 = st.columns([1, 2])  # 列の幅を調整
            with col1:
                img = Image.open(img_path)
                st.image(img, caption=os.path.basename(img_path), use_column_width=True)
            with col2:
                fake_json = generate_fake_json(img_path)
                st.json(fake_json)
            st.divider()

if __name__ == "__main__":
    main()
