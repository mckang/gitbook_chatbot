"use client";

import React, { useEffect, useRef, useState } from 'react';
import { useConfigUI } from '../ChatUIContext';



const IframeComponent: React.FC<{initUrl:string}> = ({initUrl}) => {
  // const router = useRouter();
  const { documentUrl:_documentUrl, contextPath } = useConfigUI();

  const documentUrl = _documentUrl? _documentUrl : initUrl

  // console.log("documentUrl", documentUrl)
  const iframeRef = useRef<HTMLIFrameElement | null>(null);

  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (documentUrl) {
      try {
        const url = new URL(documentUrl);
        const pathname = url.pathname;
        if (contextPath){
          window.history.pushState(null, '', contextPath+pathname);
        } else {
          window.history.pushState(null, '', pathname);
        }

      } catch (error) {
        console.error('Invalid URL:', documentUrl);
        // 에러 처리 코드
      }
    }
    setLoading(true);
    // 타임아웃 설정 (예: 10초 후 로딩 상태 해제)
    const timeoutId = setTimeout(() => {
      setLoading(false);
    }, 5000);   
    
    return () => {
      clearTimeout(timeoutId);
    };    
  }, [ documentUrl, contextPath]);

  const handleLoad = () => {
    // console.log("End Loading")
    setLoading(false);
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)', // 반투명 배경
      zIndex: 8888, // 다른 요소 위로 덮음
    }}>
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
    </div>
  );
};

export default IframeComponent;
