import pandas as pd
import re
import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from scipy.sparse import hstack
import joblib
from sklearn.metrics import classification_report

# nltk.download("punkt")
# nltk.download("stopwords")
# nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = re.sub(r"[^\w\s]", "", str(text).lower())
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]
    lemmatized = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(lemmatized)

def predict_resalability():
    df = pd.read_csv("cleaned_user_data.csv")

    df = df[df["original_price"].notna()]

    # df = df[df["user_search"].str.lower() == user_search_query.lower()]

    df["text"] = df["user_search"] + " " + df["Name"]
    text_cleaned = df["text"].apply(preprocess)

    tfidf = TfidfVectorizer()
    X_text = tfidf.fit_transform(text_cleaned)

    df["label"] = df.apply(
        lambda row: 1 if row["Price"] <= 0.7 * row["original_price"]
        and row["Price"] >= 0.4 * row["original_price"]
        and row["days_ago"] <= 5 else 0,
        axis=1
    )

    X_numeric = df[["Price", "days_ago"]].values
    X_combined = hstack([X_text, X_numeric])


    y = df["label"]
    # if len(set(y)) < 2:
    #     print(f"Not enough variation in labels to train model")
    #     return

    X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.3, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Save model and vectorizer
    joblib.dump(model, "resale_model.pkl")
    joblib.dump(tfidf, "vectorizer.pkl")

    # y_pred = model.predict(X_test)
    # print(classification_report(y_test, y_pred, zero_division=1))

    #df["resale_score"] = model.predict_proba(X_combined)[:, 1]


    # from sklearn.metrics import classification_report
    # y_pred = model.predict(X_test)
    # print(classification_report(y_test, y_pred, zero_division=1))

    # top_3 = df.sort_values("resale_score", ascending=False).head(3)
    # print(top_3[["user_search", "Name", "Price", "days_ago", "resale_score"]].to_string(index=False))


# predict_resalability("ps5", 700)
# predict_resalability("iphone x", 500)
# predict_resalability("iphone 15 pro", 800)
# predict_resalability("airpods pro 2", 250)

if __name__ == "__main__":
    predict_resalability()