"use client";


import ChatWidget from './components/popup/chatwidget'
import IframeComponent from './components/idocument';
import { usePathname } from 'next/navigation';
import { ConfigChatUIProvider } from './hooks/ChatContext';

import { useCallback } from 'react';


export default function Home() {


  const pathname = usePathname();  
  const initUrl=process.env.NEXT_PUBLIC_GITBOOK_URL + pathname
  

  return (
    <div>
      <ConfigChatUIProvider documentUrl={initUrl} >
        <IframeComponent/>    
        <ChatWidget />
      </ConfigChatUIProvider>
    </div>    
  );
}
