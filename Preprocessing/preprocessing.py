import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer




df_Wordembbading = pd.read_excel("moview_6506000_6506500.xlsx")
wordembadding_df = pd.DataFrame(df_Wordembbading)

# NLTK 자연어 처리 패키지를 사용하여 아래와 같이 전처리를 진행 


# 불필요한 문자, 소문자 변경, 문장 부호 또는 특수 기호를 제거하여 텍스트를 정리
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower() 
    text = text.strip() 
    return text


# 텍스트를 개별 단어로 토큰화
def tokenize_text(text):
    tokens = word_tokenize(text)
    return tokens


# 불용어 제거(의미없는 단어 일반적인 단어 제거)
def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return filtered_tokens



wordembadding_df[4] = wordembadding_df[4].apply(clean_text)
wordembadding_df[4] = wordembadding_df[4].apply(tokenize_text)
wordembadding_df[4] = wordembadding_df[4].apply(remove_stopwords)


#전처리된 DataFrame을 새 파일에 저장
wordembadding_df.to_excel('moview_test.xlsx', index=False)  