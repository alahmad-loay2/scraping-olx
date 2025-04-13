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
  const [topResale, setTopResale] = useState(null);
  const [predicting, setPredicting] = useState(false);

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

  const handlePredict = async (e) => {
    e.preventDefault();

    setPredicting(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/get-top-resale', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          product: productName,
        })
      });

      const data = await response.json();
      if (response.ok) {
        setTopResale(data.top_3);
      } else {
        console.error('Prediction failed:', data.error);
      }
    } catch (error) {
      console.error('Prediction error:', error);
    } finally {
      setPredicting(false);
    }
  };

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
          <h5>Distribution Price Filtering</h5>
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
          {histogram && <Plot data={histogram.data} layout={histogram.layout}  style={{ width: "100%", height: "100%" }} useResizeHandler={true}/>}
          {trend && <Plot data={trend.data} layout={trend.layout}  style={{ width: "100%", height: "100%" }} useResizeHandler={true}/>}
        </div>

        <div className="resale-prediction">
          <h3>Resale Value Prediction</h3>
          <form onSubmit={handlePredict} className="prediction-form">
            <button
              type="submit"
              disabled={predicting}
              className="predict-button"
            >
              {predicting ? 'Predicting...' : 'Predict Best Resale'}
            </button>
          </form>

          {topResale && (
            <div className="resale-table-container">
              <table className="resale-table">
                <thead>
                  <tr>
                    <th>Title</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Score/1</th>
                    <th>Link</th>
                  </tr>
                </thead>
                <tbody>
                  {topResale.map((item, index) => {
                    const baseUrl = item.link.split("q-")[0] + "q-";
                    const querySlug = item.Name.toLowerCase().split(" ").join("-");
                    const customLink = `${baseUrl}${querySlug}/`;

                    return (
                      <tr key={index}>
                        <td>
                          <a href={item.link} target="_blank" rel="noopener noreferrer">
                            {item.user_search}
                          </a>
                        </td>
                        <td>{item.Name}</td>
                        <td>${item.Price}</td>
                        <td>{item.resale_score.toFixed(3)}</td>
                        <td>
                          <a href={customLink} target="_blank" rel="noopener noreferrer">
                            {customLink}
                          </a>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      <Link className="back-btn btn details-button" to="/">Back</Link>
    </div>
  );
}

export default ProductDetails;