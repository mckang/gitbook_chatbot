import React, { createContext, useState, ReactNode, FC, Dispatch, SetStateAction, useContext } from 'react';


// Context에서 사용할 값의 타입을 정의합니다.
interface ConfigChatUIType {
  documentUrl: string;
  setDocumentUrl: Dispatch<SetStateAction<string>>;  
  handleDocumentUrlChange: (
    event: React.MouseEvent<HTMLAnchorElement, MouseEvent>,
    url: string
  ) => void;
}

// Context 생성 (기본값으로 undefined 설정)
const ConfigChatUIContext = createContext<ConfigChatUIType | undefined>(undefined);

interface ConfitChatUIProviderProps {
    documentUrl: string; 
    children: ReactNode;    
}

// Provider 컴포넌트 구현
const ConfigChatUIProvider: FC<ConfitChatUIProviderProps> = ({ documentUrl: initialUrl, children}) => {
    
    const [documentUrl, setDocumentUrl] = useState<string>(initialUrl);
    
    const handleDocumentUrlChange = (event: React.MouseEvent<HTMLAnchorElement>, url: string) => {
      event.preventDefault(); // 기본 동작 방지
      setDocumentUrl(url);    // 부모 컴포넌트에 URL 전달
    };

    return (
      <ConfigChatUIContext.Provider value={{documentUrl, setDocumentUrl, handleDocumentUrlChange}}>
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