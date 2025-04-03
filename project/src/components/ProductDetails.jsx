import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import Plot from "react-plotly.js";

function ProductDetails() {
  const { productName } = useParams();
  const [histogram, setHistogram] = useState(null);
  const [trend, setTrend] = useState(null);
  const [loading, setLoading] = useState(true);
  const [minPrice, setMinPrice] = useState(""); 
  const [maxPrice, setMaxPrice] = useState("");

  useEffect(() => {
    setLoading(true);

    const url = `http://127.0.0.1:5000/get-histogram?product=${encodeURIComponent(productName)}&min_price=${minPrice}&max_price=${maxPrice}`;
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setHistogram(JSON.parse(data));
        setLoading(false);
      })
      .catch((err) => {
        console.error("Histogram fetch error:", err);
        setLoading(false);
      });

    fetch(`http://127.0.0.1:5000/get-daily-trends?product=${encodeURIComponent(productName)}`)
      .then((res) => res.json())
      .then((data) => {
        setTrend(JSON.parse(data));
        setLoading(false);
      })
      .catch((err) => {
        console.error("Trend fetch error:", err);
        setLoading(false);
      });
  }, [minPrice, maxPrice]); 
  return (
    <div className="analysis-container">
      <h2>{productName} - Analysis</h2>

      {loading && (
        <div className="spinner-container">
          <div className="spinner"></div>
        </div>
      )}

      <div>
        <div className="filtering">
            <h5>distribution price filterting</h5>
        <div>
          <label>Min Price:</label>
          <input
            type="number"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
            placeholder="Min Price"
          />
        </div>
        <div>
          <label>Max Price:</label>
          <input
            type="number"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            placeholder="Max Price"
          />
        </div>
        </div>
        <div className="graphs">
        {histogram && <Plot data={histogram.data} layout={histogram.layout} />}
        {trend && <Plot data={trend.data} layout={trend.layout} />}
        </div>
      </div>

      <Link className="back-btn btn details-button" to="/">Back</Link>
    </div>
  );
}

export default ProductDetails;
