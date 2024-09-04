import React, { useState } from 'react';

const Tooltip = ({ text, children }) => {
  const [visible, setVisible] = useState(false);

  const showTooltip = () => setVisible(true);
  const hideTooltip = () => setVisible(false);

  return (
    <div 
      style={{ position: 'relative', display: 'inline-block' }}
      className='w-full'
      onMouseEnter={showTooltip} 
      onMouseLeave={hideTooltip}
    >
      {children}
      {visible && (
        <div 
          style={{
            position: 'absolute',
            bottom: '100%',
            left: '50%',
            width: '20em',
            transform: 'translateX(-50%)',
            backgroundColor: 'black',
            color: 'white',
            padding: '5px',
            borderRadius: '3px',
            whiteSpace: 'nowrap',
            wordWrap: 'break-word',
            wordBreak: 'break-all',
            whiteSpace: 'normal'
          }}
        >
          {text}
        </div>
      )}
    </div>
  );
};

export default Tooltip;
