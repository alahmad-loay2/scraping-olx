from flask import Flask, request, jsonify
import pandas as pd
import os
from scrape import scrape, cleaning, toggle_daily, delete
from flask_cors import CORS 
import plotly.express as px

app = Flask(__name__)
CORS(app)
CSV_FILE = "cleaned_user_data.csv"

@app.route("/run-script", methods=["POST"])
def run_scraping():
    data = request.get_json()
    product_name = data.get("product", "").strip()
    
    if not product_name:
        return jsonify({"error": "Invalid product name"}), 400
    
    print(f"Scraping product: {product_name}")
    scrape(product_name)
    
    print("Cleaning data...")
    cleaning()
    
    return jsonify({"message": "Scraping and cleaning completed"}), 200

@app.route("/get-products", methods=["GET"])
def get_products():
    if not os.path.exists(CSV_FILE):
        return jsonify({"products": []})

    df = pd.read_csv(CSV_FILE)
    products = df[["user_search", "daily"]].drop_duplicates().to_dict(orient="records")
    return jsonify({"products": products})

@app.route("/toggle-daily", methods=["POST"])
def toggle_daily_tracking():
    data = request.get_json()
    product_name = data.get("product", "").strip()
    
    if not product_name:
        return jsonify({"error": "Invalid product name"}), 400
    
    toggle_daily(product_name)
    
    return jsonify({"message": f"Toggled daily tracking for {product_name}."}), 200


@app.route("/delete-product", methods=["POST"])
def delete_product():
    data = request.get_json()
    product_name = data.get("product", "").strip()
    
    if not product_name:
        return jsonify({"error": "Invalid product name"}), 400
    
    delete(product_name)  

    return jsonify({"message": f"Deleted {product_name}."}), 200


@app.route("/get-histogram", methods=["GET"])
def get_histogram():
    product_name = request.args.get("product", "").strip()
    min_price = request.args.get("min_price", type=float, default=None)
    max_price = request.args.get("max_price", type=float, default=None)
    df = pd.read_csv(CSV_FILE)
    df_filtered = df[df["user_search"] == product_name]
    
    if df_filtered.empty:
        return jsonify({"error": "No data for this product"}), 404
    if min_price is not None:
        df_filtered = df_filtered[df_filtered["Price"] >= min_price]
    if max_price is not None:
        df_filtered = df_filtered[df_filtered["Price"] <= max_price]

    fig = px.histogram(df_filtered, x="Price", nbins=20, title=f"Price Distribution for {product_name}",
                       labels={"Price": "Price (USD)", "count": "Frequency"}, opacity=0.7)
    
    return jsonify(fig.to_json())


@app.route("/get-daily-trends", methods=["GET"])
def get_daily_trends():
    product_name = request.args.get("product", "").strip()
    df = pd.read_csv(CSV_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df_filtered = df[df["user_search"] == product_name]
    
    if df_filtered.empty:
        return jsonify({"error": "No data for this product"}), 404

    df_filtered = df_filtered.sort_values(by="timestamp")
    df_filtered["day"] = df_filtered["timestamp"].dt.date  

    daily = df_filtered.groupby("day").size().reset_index(name="count")

    fig = px.line(daily, x="day", y="count", markers=True, 
                  title=f"Listings Per Day for {product_name}",
                  labels={"day": "Date", "count": "Total Listings"})

    return jsonify(fig.to_json())





if __name__ == "__main__":
    app.run(debug=True)
