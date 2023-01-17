# https://zenn.dev/robes/articles/a3e1a6e80efd99
# https://qiita.com/y_itoh/items/7aa33ba0b1e30b3ea33d
# https://qiita.com/FukuharaYohei/items/767d27d1aae550399be9
# https://boxcode.jp/nlplot%E3%81%8C%E5%87%84%E3%81%84%EF%BC%81%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E3%82%92%E5%8F%AF%E8%A6%96%E5%8C%96%E3%83%BB%E5%88%86%E6%9E%90%E3%81%A7%E3%81%8D%E3%82%8Bpython%E3%83%A9%E3%82%A4
# https://www.dskomei.com/entry/2019/04/07/021028#%E5%BF%85%E8%A6%81%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB%E3%81%AE%E3%82%A4%E3%83%B3%E3%83%9D%E3%83%BC%E3%83%88
# https://minamolab.com/khcoder-python-co-occurrence-network-analysis
# https://dev.classmethod.jp/articles/mrmo-20190930/
# https://note.com/nymnkun/n/n8abaa21d9e88
# https://analysis-navi.com/?p=2577
# https://analysis-navi.com/?p=2293
# https://analysis-navi.com/?p=2258
# https://analysis-navi.com/?p=2577
# https://analysis-navi.com/?p=569
# https://www.eureka-moments-blog.com/entry/2022/10/01/152218
# https://www.eureka-moments-blog.com/entry/2022/10/01/152218#%E5%8D%98%E8%AA%9E%E3%82%84%E5%8F%A5%E8%AA%AD%E7%82%B9%E6%8B%AC%E5%BC%A7%E3%81%AA%E3%81%A9%E3%81%AE%E5%8D%98%E4%BD%8D%E3%81%AB%E6%96%87%E6%9B%B8%E3%82%92%E5%8C%BA%E5%88%87%E3%82%8B
# http://localhost:8888/lab
# http://localhost:8501/
# https://docs.streamlit.io/library/api-reference/media/st.image
# https://docs.streamlit.io/library/api-reference/charts/st.bar_chart
# https://docs.streamlit.io/library/api-reference/widgets/st.time_input
# https://docs.streamlit.io/library/api-reference/widgets/st.selectbox
# https://docs.streamlit.io/library/api-reference/widgets/st.multiselect
# https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart
# https://docs.streamlit.io/library/api-reference/layout/st.sidebar
# https://docs.streamlit.io/library/api-reference/layout/st.tabs
# https://docs.streamlit.io/library/api-reference/layout/st.expander
# https://docs.streamlit.io/library/api-reference/control-flow/st.form
# https://www.google.com/search?q=%E5%85%B1%E8%B5%B7%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF+plotly&ei=6K_GY9v5H-7e2roPrde9mAs&ved=0ahUKEwjbjZfN5878AhVur1YBHa1rD7MQ4dUDCA8&uact=5&oq=%E5%85%B1%E8%B5%B7%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF+plotly&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIJCAAQCBAeEPEEOg0IABAEEIAEELEDEIMBOgYIABAEEAM6CggAEAQQgAQQsQM6FggAEIAEELEDEIMBELEDEIMBEEYQgAI6EQgAEIAEELEDEIMBELEDEIMBOgUIABCABDoICAAQgAQQsQM6CwgAEIAEELEDEIMBOgcIABAEEIAEOgUIABCiBDoJCAAQHhDxBBANSgQIQRgBSgQIRhgAUKILWIs6YNo6aAFwAHgBgAH-AYgBiRySAQYwLjIxLjKYAQCgAQHAAQE&sclient=gws-wiz-serp
# https://irukanobox.blogspot.com/2021/02/python.html
# https://qiita.com/hima2b4/items/944194b206173c5721f7
# https://tech.opst.co.jp/2021/07/02/google-colaboratory%E3%81%A7plotly%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%B0%E3%83%A9%E3%83%95%E3%82%92%E4%BD%9C%E6%88%90/
# https://gist.github.com/kohiro37/d8dd770421e89fbf2c2907d4400931f0


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


#タイトル
st.title("Geminiデータ解析ツール デモver")
st.write("streamlitで実装中...")


import time
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)

# with st.form("my_form"):
#    st.write("Inside the form")
#    slider_val = st.slider("Form slider")
#    checkbox_val = st.checkbox("Form checkbox")

#    # Every form must have a submit button.
#    submitted = st.form_submit_button("Submit")
#    if submitted:
#        st.write("slider", slider_val, "checkbox", checkbox_val)

# st.write("Outside the form")

import streamlit as st

# def get_user_name():
#     return 'John'

# with st.echo():
#     # Everything inside this block will be both printed to the screen
#     # and executed.

#     def get_punctuation():
#         return '!!!'

#     greeting = "Hi there, "
#     value = get_user_name()
#     punctuation = get_punctuation()

#     st.write(greeting, value, punctuation)

# # And now we're back to _not_ printing to the screen
# foo = 'bar'
# st.write('Done!')


# st.balloons()

# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('This is a success message!', icon="✅")


# 記号全消し
# re.sub("[!-/:-@[-`{-~]","",text)
# re.sub("[\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3000-\u303F]","",text)



# 以下をサイドバーに表示
st.sidebar.markdown("### 解析に用いるGeminiデータ(.xlsxファイル)を入力してください.")
# ファイルアップロード
uploaded_files = st.sidebar.file_uploader("Geminiデータをアップロードしてください。", accept_multiple_files=False)

# ファイルがアップロードされたら以下が実行される
if uploaded_files:

    # st.image("wc.png", caption="wordcloud", width=300)

    df = pd.read_excel(uploaded_files)

    n = 20
    df_freq = get_counts(df)
    df_freq = df_freq.sort_values(by=["頻度"],ascending=False).iloc[1:n].reset_index(drop=True)
    # st.dataframe(df_freq)
    # st.bar_chart(df_freq,x="単語",y="頻度")

    import plotly.express as px
    fig = px.bar(df_freq, x='単語', y='頻度')
    ############### title=“Long-Form Input”,text=itemcrosstab_text
    # Plot!
    st.plotly_chart(fig, use_container_width=True)#, theme="streamlit")

    # selectboxで症状コード選んで
    # groupbyで機種とか選べるやつ実装しなければ
    # ------------------------------



    # ワードクラウド
    # wc_img = make_wc(df)
    # st.image(wc_img, caption="wordcloud", width=300)

    # データフレームを表示
    st.markdown("### 入力データ")
    st.dataframe(df)

    # # matplotlibで可視化。X軸,Y軸を選択できる
    # st.markdown("### 可視化 単変量")
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
                  
