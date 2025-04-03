import React from 'react';

function Header() {
  return (
    <header className="header">
      <h1>Track Products</h1>
      <p>Monitor changes automatically</p>
      <div className="loading-bar">
        <div className="loading-progress" style={{ width: '40%', left: '0', animation: 'none' }}></div>
      </div>
    </header>
  );
}

export default Header;