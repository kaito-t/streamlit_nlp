import json
import pandas as pd
import requests
import streamlit as st

with open('secret.json') as f:
    secret = json.load(f)

BASE_URL = secret["COTOHA_BASE_URL"]
CLIENT_ID = secret["COTOHA_ID"]
CLIENT_SECRET = secret["COTOHA_SECRET"]

def get_cotoha_acces_token():

    token_url = "https://api.ce-cotoha.com/v1/oauth/accesstokens"

    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    data = {
        "grantType": "client_credentials",
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET
    }

    response = requests.post(token_url,
                        headers=headers,
                        data=json.dumps(data))

    access_token = response.json()["access_token"]

    return access_token


def cotoha_sentiment_analyze(access_token, sentence):
    base_url = BASE_URL
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8",
        "Authorization": "Bearer {}".format(access_token)
    }
    data = {
        "sentence": sentence,
    }
    response = requests.post(base_url + "nlp/v1/sentiment",
                      headers=headers,
                      data=json.dumps(data))
    return response.json()


st.title('テキスト感情分析アプリ')

input_option =st.selectbox(
    '入力データの選択',
    ('直接入力', 'テキストファイル')
)

input_data = None

if input_option == '直接入力':
    input_data = st.text_area('こちらにテキストを入力して下さい。')
else:
    uploaded_file = st.file_uploader('テキストファイルをアップロードして下さい。', ['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data = content.decode()


if input_data is not None:
    st.write('入力データ')
    st.write(input_data)

    if st.button('実行'):
        accses_token = get_cotoha_acces_token()
        response = cotoha_sentiment_analyze(accses_token, input_data)

        sentiment = response["result"]["sentiment"]
        score = response["result"]["score"]
        emotional_phrase = response["result"]["emotional_phrase"]
        df_emotional_phrase = pd.DataFrame(emotional_phrase)
        st.write(f'## 分析結果:{sentiment}')
        st.write(f'### スコア:{score}')
        st.dataframe(df_emotional_phrase)