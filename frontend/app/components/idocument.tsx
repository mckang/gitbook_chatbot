"use client";

import React, { useEffect, useRef, useState } from 'react';
import { useConfigUI } from '../hooks/ChatContext';
import { useRouter } from 'next/navigation';



const IframeComponent: React.FC = () => {
  const router = useRouter();
  const { documentUrl } = useConfigUI();

  const iframeRef = useRef<HTMLIFrameElement | null>(null);

  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const url = new URL(documentUrl);
    const pathname = url.pathname;
    router.push(
      pathname
    )
    setLoading(true);
    // 타임아웃 설정 (예: 10초 후 로딩 상태 해제)
    const timeoutId = setTimeout(() => {
      setLoading(false);
    }, 5000);   
    
    return () => {
      clearTimeout(timeoutId);
    };    
  }, [router,documentUrl ]);

  const handleLoad = () => {
    // console.log("End Loading")
    setLoading(false);
  };

  return (
    <div>
      {/* 로딩 바 */}
      {loading && (
        <div className="loading-bar">
          
        </div>
      )}
      {/* iframe */}      
      <iframe
        ref={iframeRef}
        name="gitbook"
        src={documentUrl}
        onLoad={handleLoad}
        onError={handleLoad}
        frameBorder="0"
        style={{ width: '100vw', height: '100vh' }}
      />
      {/* 로딩 바 스타일 */}
      <style jsx>{`
        .loading-bar {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 4px;
          background-color: #3498db;
          animation: loading 2s infinite;
        }

        @keyframes loading {
          0% {
            transform: translateX(-100%);
          }
          50% {
            transform: translateX(0%);
          }
          100% {
            transform: translateX(100%);
          }
        }
      `}</style>      
    </div>
  );
};

export default IframeComponent;
