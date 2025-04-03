import React from 'react';
import { FaRegEye, FaTimes } from 'react-icons/fa';
import { Link } from 'react-router-dom';

function ProductList({ products, filterTracked, setFilterTracked, handleTrackToggle, handleDeleteProduct }) {
  const trackedProductsCount = products.filter(p => p.daily).length;
  const filteredProducts = filterTracked ? products.filter(p => p.daily === true) : products;

  return (
    <div className="products-container">
      <div className="products-header">
        <div className="products-title-section">
          <h2 className="products-title">Your Product Tracker</h2>
          <span className="products-count">
            Tracking {trackedProductsCount} products
          </span>
        </div>
        <div className={`filter-buttons ${filterTracked ? 'daily-active' : ''}`}>
          <button 
            className={`btn filter-button ${!filterTracked ? 'active' : ''}`}
            onClick={() => setFilterTracked(false)}
          >
            All
          </button>
          <button 
            className={`btn filter-button ${filterTracked ? 'active' : ''}`}
            onClick={() => setFilterTracked(true)}
            disabled={trackedProductsCount === 0}
          >
            Daily Tracking
          </button>
        </div>
      </div>
      <div className="row">
        {filteredProducts.map((product, index) => (
          <div key={index} className=" col-md-6">
            <div className={`product-card ${product.daily ? 'tracking' : ''}`}>
              <div className="product-card-header">
                <h3 className="product-card-title">{product.user_search}</h3>
                <button 
                  className="btn delete-button"
                  onClick={() => handleDeleteProduct(product.user_search)}
                >
                  <FaTimes />
                </button>
              </div>
              <div className="product-card-actions">
                <div className="switch-container">
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={product.daily}
                      onChange={() => handleTrackToggle(product.user_search)}
                    />
                    <span className="slider"></span>
                  </label>
                  <span className="switch-label">Daily Track</span>
                </div>
                <Link to={`/product/${encodeURIComponent(product.user_search)}`} className="btn details-button">
                  <FaRegEye />
                  View
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProductList;