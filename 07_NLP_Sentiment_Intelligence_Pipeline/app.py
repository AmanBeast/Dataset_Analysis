import streamlit as st
import pandas as pd

import re
import joblib

from nltk.corpus import stopwords

from nltk.stem import PorterStemmer

#load model and TF-IDF
model = joblib.load('modal.joblib')

tfidf = joblib.load('tfidf.joblib')

ps = PorterStemmer()

stop_words = set(stopwords.words('english'))

#text clearning
def  clean_text(text):
    text= text.lower()
    text = re.sub('[^a-z]',' ' ,text)
    words = text.split()
    words = [ps.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

#Prediction
def predict_sentiment(text):
    cleaned = clean_text(text)
    vector = tfidf.transform([cleaned])
    prediction = model.predict(vector)[0]

    #label mapping
    return "Positive" if prediction == 1 else "Negative"

# user interface
st.title("Movie Sentiment Analyzer🍿🎥")
st.markdown("## *Interactive ML Dashboard with IMDB Dataset*")


user_input = st.text_input("Enter your review:🥸")

if st.button("Predict🔮"):
    if user_input.strip() != "":
        result = predict_sentiment(user_input)
        st.success(f"Prediction: {result}")

    else:
        st.warning("Please enter some text")

#reset button
if st.button("Reset❌"):
 st.session_state.clear()

 st.rerun()

 st.divider()


