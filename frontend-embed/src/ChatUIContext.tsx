import React, { createContext, useState, ReactNode, FC, Dispatch, SetStateAction, useContext, useRef } from 'react';

// starterQuestions의 타입을 명확하게 정의합니다.
type StarterQuestions = string[]; // string 배열로 가정

// Context에서 사용할 값의 타입을 정의합니다.
interface ConfigChatUIType {
  starterQuestions: StarterQuestions;
  title: string;
  imageUrl: string;
  windowWidth: Number;
  windowHeight: Number;
  gitbookUrl: string,
  contextPath: string,
  documentUrl: string;
  embedDocSite: boolean;
  showContent: boolean;
  chatboxWidth: Number;
  chatboxHeight: Number;  
  setShowContent: Dispatch<SetStateAction<boolean>>;   
  setDocumentUrl: Dispatch<SetStateAction<string>>;   
  setChatboxWidth: Dispatch<SetStateAction<Number>>;   
  setChatboxHeight: Dispatch<SetStateAction<Number>>;     
  handleDocumentUrlChange: (
    event: React.MouseEvent<HTMLAnchorElement, MouseEvent>,
    url: string
  ) => void;      
}

// Context 생성 (기본값으로 undefined 설정)
const ConfigChatUIContext = createContext<ConfigChatUIType | undefined>(undefined);

interface ConfitChatUIProviderProps {
  starterQuestions: StarterQuestions;
  title: string;
  imageUrl: string;
  windowWidth: Number;
  windowHeight: Number;
  documentUrl: string; 
  gitbookUrl: string;
  contextPath: string;
  embedDocSite: boolean;
  children: ReactNode;  
}


// Provider 컴포넌트 구현
const ConfigChatUIProvider: FC<ConfitChatUIProviderProps> = ({ 
                  starterQuestions, 
                  title, 
                  imageUrl, 
                  windowWidth, 
                  windowHeight, 
                  gitbookUrl, 
                  contextPath,
                  documentUrl:initialDocumentUrl, 
                  embedDocSite,
                  children }) => {

  const popupRef = useRef<Window | null>(null);
  const [documentUrl, setDocumentUrl] = useState<string>(initialDocumentUrl);
  const [showContent, setShowContent] = useState(false);
  const [chatboxWidth, setChatboxWidth] = useState<Number>(windowWidth);
  const [chatboxHeight, setChatboxHeight] = useState<Number>(windowHeight);

    
  const handleDocumentUrlChange = (event: React.MouseEvent<HTMLAnchorElement>, url: string) => {
    event.preventDefault(); // 기본 동작 방지
    setDocumentUrl(url);    // 부모 컴포넌트에 URL 전달
    if (!embedDocSite){
      const popupWidth = 600;
      const popupHeight = 800;
  
      // 현재 윈도우의 크기를 기준으로 중앙에 위치 계산
      const left = window.innerWidth / 2 - popupWidth / 2;
      const top = window.innerHeight / 2 - popupHeight / 2;      
      const popupFeatures = `width=${popupWidth},height=${popupHeight},left=${left},top=${top},resizable=yes,scrollbars=yes`;
      // 팝업 창이 열려 있는지 확인
      if (popupRef.current && !popupRef.current?.closed) {
        // 팝업 창이 열려 있고 닫혀 있지 않다면 주소만 변경
        popupRef.current.location.href = url;
        popupRef.current.focus(); // 팝업 창을 앞으로 가져옴
      } else {
        // 팝업 창이 없거나 닫혀 있으면 새로 열기
        popupRef.current = window.open(url, '_blank', popupFeatures);
      }

    }
  };

  return (
    <ConfigChatUIContext.Provider 
      value={{
        starterQuestions, 
        title, 
        imageUrl, 
        windowWidth, 
        windowHeight, 
        gitbookUrl,
        contextPath,
        embedDocSite,
        chatboxWidth,
        chatboxHeight,
        setChatboxHeight,
        setChatboxWidth,
        showContent, setShowContent,
        documentUrl, setDocumentUrl, handleDocumentUrlChange}}>
      {children}
    </ConfigChatUIContext.Provider>
  );
};

// Custom hook을 통해 context 사용을 쉽게 만듭니다.
const useConfigUI = () => {
  const context = useContext(ConfigChatUIContext);
  if (!context) {
    throw new Error('useConfigUI must be used within a ConfigChatUIProvider');
  }
  return context;
}

export { ConfigChatUIProvider, useConfigUI };
