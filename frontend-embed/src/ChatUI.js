import React, { useState, useRef } from 'react';
import ChatWidget from './components/bubble/chatwidget';
import styles from './ChatUI.module.css'; 
import root from 'react-shadow';
import tailwind from '../public/tailwind.generated.css?inline'
import { ConfigChatUIProvider } from './ChatUIContext'


const ChatUI = ({starterQuestions=[], title="", imageUrl="", windowWidth="600px", windowHeight="80vh"}) => {
  // console.log("tailwind", tailwind)
  // console.log("styles", styles)
  return (
    <root.div className="quote">
        <style>{tailwind}</style>
        <ConfigChatUIProvider starterQuestions={starterQuestions} title={title} imageUrl={imageUrl} windowWidth={windowWidth} windowHeight={windowHeight}>
          <ChatWidget />
        </ConfigChatUIProvider>
    </root.div>
  );
};

export default ChatUI;