import React from 'react';
import { FaSearch } from 'react-icons/fa';

function AddProduct({ productInput, setProductInput, handleAddProduct }) {
  return (
    <div className="search-section">
      <h2>Add Products to Track</h2>
      <p>Enter the name of any product you want to monitor</p>
      <form onSubmit={handleAddProduct}>
        <div className="input-container">
          <FaSearch className="search-icon" />
          <input
            type="text"
            className="form-control search-input"
            placeholder="add product to scrape..."
            value={productInput}
            onChange={(e) => {
              if (e.target.value.length <= 50) {
                setProductInput(e.target.value);
              }
            }}
            maxLength={50}
          />
          <button 
            className={`btn add-button ${!productInput.trim() ? 'disabled' : ''}`}
            type="submit"
            disabled={!productInput.trim()}
          >
            Add Product
          </button>
        </div>
      </form>
    </div>
  );
}

export default AddProduct