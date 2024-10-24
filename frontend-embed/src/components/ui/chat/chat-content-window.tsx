"use client";

import React, { useEffect, useRef, useState } from 'react';
import { useConfigUI } from '../../../ChatUIContext';




const ContentWindowComponent: React.FC = () => {
  // const router = useRouter();
  const { documentUrl, windowWidth, windowHeight, showContent, setShowContent } = useConfigUI();

  // console.log("documentUrl", documentUrl)
  const iframeRef = useRef<HTMLIFrameElement | null>(null);

  const openContentWindow = (imageUrl:any) => {
    setShowContent(true);
  };  
  const closeContentWindow = () => {
    setShowContent(false);
  };

  //   background-color: rgba(0, 0, 0, 0.9);
  // display: flex;
  // justify-content: center;
  // align-items: center;
  // z-index: 1000;
  // cursor: pointer;

  return (
    <>
    {showContent && (
      <div style={{zIndex: '1001', 
        position: "absolute",
        bottom: "10px",
        width: '786px', height: '90vh',
        display: 'flex', alignItems: 'center', justifyContent:'center', 
        backgroundColor: 'rgba(0, 0, 0, 0.9)'}}
        className='right-[10px] 2xl:right-[640px] xl:right-[600px] lg:right-[200px] md:right-[50px] '
        >

        <div style={{
          maxWidth: '768px',maxHeight: '90vh', width: '95%', height: '90%', 
          display: 'flex', alignItems: 'center', justifyContent:'center'
        }}>
          {/* iframe */}      
          <iframe
            ref={iframeRef}
            name="gitbook"
            src={documentUrl}
            frameBorder="0"
            style={{ width: '100%', height: '100%' }}
          />                  
        </div>
        <button style={{
            position: "absolute",
            top: "10px",
            right: "10px",
            background: "none",
            border: "none",
            fontSize: "2rem",
            color: "white",
            cursor: "pointer",
            zIndex: "1100",
            transition: "transform 0.2s ease",          
          }} onClick={closeContentWindow}>
              &times;
            </button>     
      </div>
    )}
    </>
  );
};

export default ContentWindowComponent;
