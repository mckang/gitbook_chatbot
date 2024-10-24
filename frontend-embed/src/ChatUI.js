import React, { useState, useEffect } from 'react';
import ChatWidget from './components/bubble/chatwidget';
import styles from './ChatUI.module.css'; 
import root from 'react-shadow';
import tailwind from '../public/tailwind.generated.css?inline'
import { ConfigChatUIProvider } from './ChatUIContext'
import IframeComponent from './components/iDocument'


function removeFirstDocs(docsPattern, url) {
  if (!docsPattern) {
    return url
  }

  const docsIndex = url.indexOf(docsPattern);

  // 만약 /docs가 URL에 존재하면
  if (docsIndex !== -1) {
    // /docs 이후의 문자열을 추출하여 리턴
    return url.substring(0, docsIndex) + url.substring(docsIndex + docsPattern.length);
  }

  // /docs가 없을 경우 원본 URL을 리턴
  return url;
}

const ChatUI = ({starterQuestions=[], title="", imageUrl="", gitbookUrl="", contextPath=null, windowWidth="600px", windowHeight="80vh", embedDocSite=true}) => {
  const pathname =window.location.pathname;  

  const [initUrl, setInitUrl] = useState('');

  useEffect(() => {
    const url = removeFirstDocs(contextPath, `${gitbookUrl}${pathname}`);
    setInitUrl(url);
  }, [pathname]);
  
  return (
    <root.div className="quote">
        <style>{tailwind}</style>
        <ConfigChatUIProvider 
                starterQuestions={starterQuestions} 
                title={title} 
                imageUrl={imageUrl} 
                gitbookUrl={gitbookUrl} 
                windowWidth={windowWidth} 
                windowHeight={windowHeight} 
                documentUrl={initUrl}
                contextPath={contextPath}
                embedDocSite={embedDocSite}>
          {embedDocSite ? <IframeComponent initUrl={initUrl}/>  : <></> }
          <ChatWidget />
        </ConfigChatUIProvider>
    </root.div>
  );
};

export default ChatUI;