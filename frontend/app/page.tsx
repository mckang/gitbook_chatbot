"use client";


import ChatWidget from './components/popup/chatwidget'
import IframeComponent from './components/idocument';
import { usePathname } from 'next/navigation';
import { ConfigChatUIProvider } from './hooks/ChatContext';
import { useEffect, useState } from 'react';

export default function Home() {

  const pathname = usePathname();  
  const [initUrl, setInitUrl] = useState('');

  useEffect(() => {
    const url = `${process.env.NEXT_PUBLIC_GITBOOK_URL}${pathname}`;
    setInitUrl(url);
  }, [pathname]);
  
  return (
    <div>
      <ConfigChatUIProvider documentUrl={initUrl} >
        <IframeComponent initUrl={initUrl}/>    
        <ChatWidget />
      </ConfigChatUIProvider>
    </div>    
  );
}
