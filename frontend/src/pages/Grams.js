import React,{useEffect, useRef} from 'react';
import '../index.css';

const Grams = ({ result }) => {
  // Check if result exists and has Carbon_footprint property
  const carbonFootprint = result && result.Carbon_footprint;
  const greenHosting = result && result.Green_hosting;

  // Format carbon footprint to display up to 3 decimal places
  const formattedCarbonFootprint = carbonFootprint ? carbonFootprint.toFixed(3) : null;

  const gramsRef = useRef(null);

  useEffect(() => {
    if (result) {
      gramsRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [result]);

  // Render the component only when result is available
  if (!result) {
    return null;
  }

  return (
    <div className='flex flex-col bg-[#202020] text-white p-10 gap-10' ref={gramsRef}>
      <div className='flex flex-row items-center justify-between gap-20'>
        <div className='flex flex-col gap-20'>
          <p className='text-xl md:text-3xl'>RESULTS FOR<br/> whatthefuckamidoing.com</p>
          {carbonFootprint && ( // Check if carbonFootprint exists
            <p className='text-3xl md:text-5xl'>EACH VISIT TO THIS WEBSITE PRODUCES <span className="text-[#1ecb7b]">{formattedCarbonFootprint}g</span> OF CO2</p>
          )}
        </div>
        <div className='flex items-center'>
          <span className='text-[10rem] lg:text-[18rem] font-outline hidden md:block'>{formattedCarbonFootprint}g</span>
        </div>
      </div>
      <span className=' hidden md:block'>
        {greenHosting ? 'Green' : 'Not Green'}
      </span>
      <div className='text-2xl md:text-4xl pb-20'>This web page emits the amount of carbon that 2 trees absorb in a year.</div>
    </div>
  );
}

export default Grams;
