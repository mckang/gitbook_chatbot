import React, { createContext, useState, ReactNode, FC, Dispatch, SetStateAction, useContext } from 'react';

// starterQuestions의 타입을 명확하게 정의합니다.
type StarterQuestions = string[]; // string 배열로 가정

// Context에서 사용할 값의 타입을 정의합니다.
interface ConfigChatUIType {
  starterQuestions: StarterQuestions;
  setStarterQuestions: Dispatch<SetStateAction<StarterQuestions>>;
  title: string;
  setTitle: Dispatch<SetStateAction<string>>;  
  imageUrl: string;
  setImageUrl: Dispatch<SetStateAction<string>>;  
  windowWidth: string;
  setWindowWidth: Dispatch<SetStateAction<string>>;   
  windowHeight: string;
  setWindowHeight: Dispatch<SetStateAction<string>>;     
}

// Context 생성 (기본값으로 undefined 설정)
const ConfigChatUIContext = createContext<ConfigChatUIType | undefined>(undefined);

interface ConfitChatUIProviderProps {
  starterQuestions: StarterQuestions;
  title: string;
  imageUrl: string;
  windowWidth: string;
  windowHeight: string;
  children: ReactNode;
}


// Provider 컴포넌트 구현
const ConfigChatUIProvider: FC<ConfitChatUIProviderProps> = ({ starterQuestions: initialQuestions, title: initialTitle, imageUrl: initialImageUrl, windowWidth: initialWidth, windowHeight: initialHeight, children }) => {
  const [starterQuestions, setStarterQuestions] = useState<StarterQuestions>(initialQuestions);
  const [title, setTitle] = useState<string>(initialTitle);
  const [imageUrl, setImageUrl] = useState<string>(initialImageUrl);
  const [windowWidth, setWindowWidth] = useState<string>(initialWidth);
  const [windowHeight, setWindowHeight] = useState<string>(initialHeight);
  
  return (
    <ConfigChatUIContext.Provider value={{starterQuestions, setStarterQuestions, title, setTitle, imageUrl, setImageUrl, windowWidth, setWindowWidth, windowHeight, setWindowHeight}}>
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
