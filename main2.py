import os
import streamlit as st
import pandas as pd
import numpy as np

import MeCab
from wordcloud import WordCloud


def get_input_for_wordcloud(text):
    # こっちの方がいい
    # https://boxcode.jp/nlplot%E3%81%8C%E5%87%84%E3%81%84%EF%BC%81%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E3%82%92%E5%8F%AF%E8%A6%96%E5%8C%96%E3%83%BB%E5%88%86%E6%9E%90%E3%81%A7%E3%81%8D%E3%82%8Bpython%E3%83%A9%E3%82%A4

    #単語の分割
    m = MeCab.Tagger()#('-Ochasen')

    word=""
    nodes = m.parseToNode(text)
    s = []
    while nodes:
        if nodes.feature[:2] in ["名詞"]:
            s.append(nodes.surface)
        nodes = nodes.next
    
    return s

def make_wc(df):
    text = "。".join(df["連絡事項_修正"].values)
    words = get_input_for_wordcloud(text)
    word = " ".join(words)
     
    fpath = "./ヒラギノ角ゴシック W0.ttc"
    wordcloud = WordCloud(background_color="white",font_path=fpath,width=1200,height=800,min_font_size=15)
    wordcloud.generate(word)
    wordcloud.to_file("./wordcloud.png")
    
    return np.array(wordcloud)

import collections
def get_counts(df):

    #単語の数カウント
    text = "。".join(df["連絡事項_修正"].values)
    words = get_input_for_wordcloud(text)

    c = collections.Counter(words)

    df_freq = pd.DataFrame({"頻度":c}).reset_index()
    df_freq.columns = ["単語","頻度"]

    return df_freq

import time
import plotly.express as px
import streamlit as st

# webページの設定
# https://data-analytics.fun/2022/07/10/streamlit-theme-page-settings/
# image = Image.open('スライム.jpg')
st.set_page_config(
    page_title="Geminiデータ解析ツール Hitachi GLS", 
    # page_icon=image, 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items={
        #  'Get Help': 'https://www.google.com',
        #  'Report a bug': "https://www.google.com",
         'About': """
         # 画像生成風アプリ
         このアプリは画像生成風アプリで、実際にはキングスライムしか表示しません。
         """
     })

#タイトル
st.title("Geminiデータ解析ツール デモver")
st.write("streamlitで実装中...")
st.write("pageが使えるなら...連絡事項分析(wordcloud,共起ネットワーク), チャート分析 に分ける")

# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)

# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('This is a success message!', icon="✅")

def remove_col_from_list(col,cols):
    return [c for c in cols if c != col]

FILE_DIR_PATH = "docs"
os.makedirs(FILE_DIR_PATH, exist_ok=True)
COMMENT_FILE_PATH = f"./{FILE_DIR_PATH}/comment.txt"


# import pandas as pd

# url = [
#   # Adelie penguin data
#   'https://portal.edirepository.org/nis/dataviewer?packageid=knb-lter-pal.219.3&entityid=002f3893385f710df69eeebe893144ff',
#   # Gentoo penguin data
#   'https://portal.edirepository.org/nis/dataviewer?packageid=knb-lter-pal.220.3&entityid=e03b43c924f226486f2f0ab6709d2381',
#   # Chinstrap penguin data
#   'https://portal.edirepository.org/nis/dataviewer?packageid=knb-lter-pal.221.2&entityid=fe853aa8f7a59aa84cdd3197619ef462',
# ]

# df = pd.concat([
#   pd.read_csv(url[0]),
#   pd.read_csv(url[1]),
#   pd.read_csv(url[2])
# ])


# 以下をサイドバーに表示
st.sidebar.markdown("### 解析に用いるGeminiデータ(.xlsxファイル)を入力してください.")
# ファイルアップロード
uploaded_files = st.sidebar.file_uploader("Geminiデータをアップロードしてください。", accept_multiple_files=False)

# ファイルがアップロードされたら以下が実行される
if uploaded_files:

    # st.image("wc.png", caption="wordcloud", width=300)

    # df = pd.read_excel(uploaded_files)
    df = pd.read_csv("penguin.csv",index_col=0)

    # データフレームを表示
    st.markdown("### 入力データ")
    st.dataframe(df)

    group_cols = ["studyName","Species","Island","Clutch Completion","Sex"]
    # 処理内容が一般化できるなら、forで作っても良さそう
    # tab1, tab2, tab3, tab4, tab5 = st.tabs(group_cols)
    tabs = st.tabs(group_cols)

    for i in range(len(tabs)):
        with tabs[i]:
            col = group_cols[i]
            st.subheader(col)

            df_ret = df.groupby(col).size().sort_values(ascending=False).to_frame(name="出現数").reset_index()
            fig = px.bar(df_ret,x=col,y="出現数",title=f"{col}別データ数")
            st.plotly_chart(fig,use_container_width=True)#, theme="streamlit")

            # データフレームのカラムを選択肢にする。複数選択
            # colで横に置いても良さそう
            df_columns = remove_col_from_list(col,group_cols)
            col_layouts = st.columns(len(df_columns))
            for j in range(len(col_layouts)):
                sub_col = df_columns[j]
                with col_layouts[j]:
                    st.markdown(f"#### {sub_col}")
                    item = st.multiselect("",df[sub_col].unique(),key=f"{col}_{sub_col}")

                    # 辞書に入れて下で取り出すか〜
                    st.write(item)

    # with tab1:
    #     col = group_cols[0]
    #     st.header(col)

    #     df_ret = df.groupby(col).size().sort_values(ascending=False).to_frame(name="出現数").reset_index()
    #     fig = px.bar(df_ret,x=col,y="出現数",title=f"{col}別データ数")
    #     st.plotly_chart(fig,use_container_width=True)#, theme="streamlit")

    # with tab2:
    #     st.header(group_cols[1])
        
    # with tab3:
    #     st.header(group_cols[2])
    
    # with tab4:
    #     st.header(group_cols[3])

    # with tab5:
    #     st.header(group_cols[4])
        
        #st.write("・各機種ごとの症状コード")
        #st.write("・各症例ごとの機種番号")

    # 余白
    st.markdown("#  ") 

    ####################
    # コメントフォーム
    ####################
    with st.form("freeform", clear_on_submit=False):
        st.markdown("### コメントフォーム")
        
        txt_comment = st.text_area("不便な点や欲しい機能等、ご意見・ご要望がございましたら何でもお送りください👍", "",)
        submitted = st.form_submit_button("送信")
        
        # 提出ボタンが押されたとき
        if submitted:
            if len(txt_comment.replace(" ",""))>0:
                st.success('メッセージが送信されました!', icon="✅")

                # コメントをファイルに出力
                with open(COMMENT_FILE_PATH, mode='a') as f:
                    # 日付入れたい。
                    # f.write(f"\n\n({}){txt_comment}")
                    f.write(f'\n\n{txt_comment}')
            else:
                st.write(f"空のコメントは送信できません。")


    # n = 20
    # df_freq = get_counts(df)
    # df_freq = df_freq.sort_values(by=["頻度"],ascending=False).iloc[1:n].reset_index(drop=True)
    # st.dataframe(df_freq)
    # st.bar_chart(df_freq,x="単語",y="頻度")

    
    # fig = px.bar(df_freq, x='単語', y='頻度')
    ############### title=“Long-Form Input”,text=itemcrosstab_text
    # Plot!
    # st.plotly_chart(fig, use_container_width=True)#, theme="streamlit")

    # selectboxで症状コード選んで
    # groupbyで機種とか選べるやつ実装しなければ
    # ------------------------------



    # ワードクラウド
    # wc_img = make_wc(df)
    # st.image(wc_img, caption="wordcloud", width=300)

    
        

    # st.markdown("### ")
    # #データフレームのカラムを選択オプションに設定する
    # x = st.selectbox("X軸", df_columns)
    # y = st.selectbox("Y軸", df_columns)
    # #選択した変数を用いてmtplotlibで可視化
    # fig = plt.figure(figsize= (12,8))
    # plt.scatter(df[x],df[y])
    # plt.xlabel(x,fontsize=18)
    # plt.ylabel(y,fontsize=18)
    # st.pyplot(fig)

    # #seabornのペアプロットで可視化。複数の変数を選択できる。
    # st.markdown("### 可視化 ペアプロット")
    # #データフレームのカラムを選択肢にする。複数選択
    # item = st.multiselect("可視化するカラム", df_columns)
    # #散布図の色分け基準を１つ選択する。カテゴリ変数を想定
    # hue = st.selectbox("色の基準", df_columns)
    
    # #実行ボタン（なくてもよいが、その場合、処理を進めるまでエラー画面が表示されてしまう）
    # execute_pairplot = st.button("ペアプロット描画")
    # #実行ボタンを押したら下記を表示
    # if execute_pairplot:
    #         df_sns = df[item]
    #         df_sns["hue"] = df[hue]
            
    #         #streamlit上でseabornのペアプロットを表示させる
    #         fig = sns.pairplot(df_sns, hue="hue")
    #         st.pyplot(fig)


    # st.markdown("### モデリング")
    # #説明変数は複数選択式
    # ex = st.multiselect("説明変数を選択してください（複数選択可）", df_columns)

    # #目的変数は一つ
    # ob = st.selectbox("目的変数を選択してください", df_columns)

    # #機械学習のタイプを選択する。
    # ml_menu = st.selectbox("実施する機械学習のタイプを選択してください", ["重回帰分析","ロジスティック回帰分析"])
    
    # #機械学習のタイプにより以下の処理が分岐
    # if ml_menu == "重回帰分析":
    #         st.markdown("#### 機械学習を実行します")
    #         execute = st.button("実行")
            
    #         lr = linear_model.LinearRegression()
    #         #実行ボタンを押したら下記が進む
    #         if execute:
    #               df_ex = df[ex]
    #               df_ob = df[ob]
    #               X_train, X_test, y_train, y_test = train_test_split(df_ex.values, df_ob.values, test_size = 0.3)
    #               lr.fit(X_train, y_train)
    #               #プログレスバー（ここでは、やってる感だけ）
    #               my_bar = st.progress(0)
                  
    #               for percent_complete in range(100):
    #                     time.sleep(0.02)
    #                     my_bar.progress(percent_complete + 1)
                  
    #               #metricsで指標を強調表示させる
    #               col1, col2 = st.columns(2)
    #               col1.metric(label="トレーニングスコア", value=lr.score(X_train, y_train))
    #               col2.metric(label="テストスコア", value=lr.score(X_test, y_test))
                  
    # #ロジスティック回帰分析を選択した場合
    # elif ml_menu == "ロジスティック回帰分析":
    #         st.markdown("#### 機械学習を実行します")
    #         execute = st.button("実行")
            
    #         lr = LogisticRegression()

    #         #実行ボタンを押したら下記が進む
    #         if execute:
    #               df_ex = df[ex]
    #               df_ob = df[ob]
    #               X_train, X_test, y_train, y_test = train_test_split(df_ex.values, df_ob.values, test_size = 0.3)
    #               lr.fit(X_train, y_train)
    #               #プログレスバー（ここでは、やってる感だけ）
    #               my_bar = st.progress(0)
    #               for percent_complete in range(100):
    #                     time.sleep(0.02)
    #                     my_bar.progress(percent_complete + 1)

    #               col1, col2 = st.columns(2)
    #               col1.metric(label="トレーニングスコア", value=lr.score(X_train, y_train))
    #               col2.metric(label="テストスコア", value=lr.score(X_test, y_test))
                  
