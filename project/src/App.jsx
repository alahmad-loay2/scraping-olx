import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import Header from "./components/Header";
import AddProduct from "./components/AddProduct";
import ProductList from "./components/ProductList";
import ProductDetails from "./components/ProductDetails";
import "./index.css";

function App() {
  const [products, setProducts] = useState([]);
  const [productInput, setProductInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [filterTracked, setFilterTracked] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/get-products");
      const result = await response.json();
      setProducts(result.products);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const handleAddProduct = async (e) => {
    e.preventDefault();
    const trimmedInput = productInput.trim();
    if (!trimmedInput) return;

    setLoading(true);
    try {
      await fetch("http://127.0.0.1:5000/run-script", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product: trimmedInput }),
      });
      setProductInput("");
      fetchProducts();
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTrackToggle = async (productName) => {
    try {
      await fetch("http://127.0.0.1:5000/toggle-daily", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product: productName }),
      });
      fetchProducts();
    } catch (error) {
      console.error("Error toggling daily tracking:", error);
    }
  };

  const handleDeleteProduct = async (productName) => {
    try {
      await fetch("http://127.0.0.1:5000/delete-product", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product: productName }),
      });
      fetchProducts();
    } catch (error) {
      console.error("Error deleting product:", error);
    }
  };

  return (
    <Router>
      <div className="container-fluid p-0">
        <Header />
        <Routes>
          <Route
            path="/"
            element={
              <>
                <AddProduct
                  productInput={productInput}
                  setProductInput={setProductInput}
                  handleAddProduct={handleAddProduct}
                />
                <ProductList
                  products={products}
                  filterTracked={filterTracked}
                  setFilterTracked={setFilterTracked}
                  handleTrackToggle={handleTrackToggle}
                  handleDeleteProduct={handleDeleteProduct}
                />
              </>
            }
          />
          <Route path="/product/:productName" element={<ProductDetails />} />
        </Routes>

        {loading && (
          <div className="spinner-container">
            <div className="spinner"></div>
          </div>
        )}
      </div>
    </Router>
  );
}

export default App;
