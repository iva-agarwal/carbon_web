import React from 'react';

const Results = ({ result }) => {
  // Destructure values from the result object
  if (!result) {
    return null;
  }

  const {
    css_data_gb,
    font_data_gb,
    js_data_gb,
    media_data_gb,
    html_data_gb,
    total_data_gb,
    Carbon_footprint,
    Green_hosting
  } = result;

  // Define an array of headings
  const headings = ["CSS", "Font", "JavaScript", "Media", "HTML"];

  // Define an array of corresponding data_gb values
  const data_gb = [css_data_gb, font_data_gb, js_data_gb, media_data_gb, html_data_gb];

  return (
    <div className='grid grid-cols-1 lg:grid-cols-2 p-10 gap-x-28'>
      {headings.map((heading, index) => (
        <div key={index} className='flex flex-row items-center gap-4'>
          <div className='text-[180px] lg:text-[250px] font-outline'>{index + 1}</div>
          <div className='flex flex-col'>
            <h1 className='text-5xl md:text-9xl font-rough'>{heading}</h1>
            <p className='text-lg md:text-xl'>
              {data_gb[index]} {/* Access the corresponding data_gb value */}
            </p>
          </div>
        </div>
      ))}
      <div className='flex flex-row items-center gap-4'>
        <div className='text-[180px] lg:text-[250px] font-outline'>{headings.length + 1}</div>
        <div className='flex flex-col'>
          <h1 className='text-5xl md:text-9xl font-rough'>Total</h1>
          <p className='text-lg md:text-xl'>{total_data_gb}</p>
        </div>
      </div>
    </div>
  );
};

export default Results;
