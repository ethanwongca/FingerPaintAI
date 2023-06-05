import { useState, useEffect } from 'react';
import logo from './fingerprint.png'; // Update the path to the correct location of your image
import './app.css';


function App() {
  const [showPopup, setShowPopup] = useState(true);

  const handleClosePopup = () => {
    setShowPopup(false);
  };
  const [imageData, setImageData] = useState(null);

  useEffect(() => {
    fetch('/api/draw')  // Use the actual API endpoint of your Flask backend
      .then((response) => response.json())
      .then((data) => {
        setImageData(data.image);
      })
      .catch((error) => {
        console.log('Error fetching image data from backend:', error);
      });
  }, []);

  return (
    <div className="container">
      {showPopup && (
        <div className="popup">
          <div className="popup-content">
            <h2>Welcome to FingerPaintAI!</h2>
            <p>To draw point up your finger, to select hold up two fingers and touch the color!</p>
            <button onClick={handleClosePopup}>Close</button>
          </div>
        </div>
      )}
    <div className = "header">
      <img src={logo} alt="Logo" className="logo" />
      <h1 className="title">Fingerpaint AI</h1>
    </div>

    {imageData && (
        <img src={`data:image/jpeg;base64,${imageData}`} alt="Drawing" />
      )}
    </div>
  );
}

export default App;

