import React, { useState } from 'react';
import axios from 'axios';
import img_1 from '../images/Environment-bro.svg'

const Input = ({ setResult, onURLSubmit }) => {
  const [url, setUrl] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/calculatecarbon', { url });
      setResult(response.data);
      setSubmitted(true);
      onURLSubmit(); // Notify parent component that URL has been submitted
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="flex flex-col md:flex-row items-center justify-center h-screen p-10 ">
      {/* Search bar */}
      <div className="flex-1 p-4 flex flex-col gap-10">
        <h1 className='text-2xl md:text-4xl text-center'>Enter your website's URL</h1>
        <input
          type="text"
          placeholder=""
          className="w-full p-2 md:p-4 rounded-full bg-[#202020] text-white focus:outline-none"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <p className='text-md md:text-lg text-center'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Id explicabo repudiandae ex perspicatis, dolores sint sapiente! Eum consectetur cumque dolorem ullam. Necessitatibus nulla nam et obcaecati minus omnis, ex cumque.</p>
        <button onClick={handleSubmit}>Calculate Carbon</button>
      </div>

      {/* Illustration */}
      <div className="flex-1">
        <img src={img_1} alt="Illustration" className="w-full h-auto" />
      </div>
    </div>
  );
}

export default Input;
