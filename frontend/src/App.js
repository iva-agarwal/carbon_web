import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Input from './pages/Input';
import Grams from './pages/Grams';
import Results from './pages/Results';
import Profile from './pages/Profile';
import Footer from './components/Footer';

function App() {
  const [result, setResult] = useState(null);
  const [isURLSubmitted, setIsURLSubmitted] = useState(false);

  const handleURLSubmit = () => {
    setIsURLSubmitted(true);
  };

  const resetURLSubmitted = () => {
    setIsURLSubmitted(false);
  };

  return (
    <div>
      <Navbar />
      <Home />
       <Input setResult={setResult} onURLSubmit={handleURLSubmit} />
       <Grams result={result} />
       <Results result={result} />
      <Profile />
      <Footer />
    </div>
  );
}

export default App;
