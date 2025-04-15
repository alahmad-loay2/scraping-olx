import pandas as pd
import joblib
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from scipy.sparse import hstack

model = joblib.load("resale_model.pkl")
tfidf = joblib.load("vectorizer.pkl")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text):
    text = re.sub(r"[^\w\s]", "", str(text).lower())
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]
    lemmatized = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(lemmatized)

def predict_resale_score(search_query, original_price):
    df = pd.read_csv("cleaned_user_data.csv")
    df = df[df["user_search"].str.lower() == search_query.lower()]

    if df.empty:
        print(f"No entries found for '{search_query}'")
        return

    df["text"] = df["user_search"] + " " + df["Name"]
    text_cleaned = df["text"].apply(preprocess)
    X_text = tfidf.transform(text_cleaned)

    df["original_price"] = original_price


    X_numeric = df[["Price", "days_ago", "original_price"]].values
    X_combined = hstack([X_text, X_numeric])

    df["resale_score"] = model.predict_proba(X_combined)[:, 1]

    top_5 = df.sort_values("resale_score", ascending=False).head(5)

    return top_5[["user_search", "Name", "Price", "resale_score", "link"]]


# search_query = "asus rog strix"
# original_price = 1000

# result = predict_resale_score(search_query, original_price)
# print(result)

