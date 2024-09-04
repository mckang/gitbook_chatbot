import React from 'react';
// import ReactDOM from 'react-dom';
import { createRoot } from 'react-dom/client';

import ChatUI from './ChatUI';
import './index.css'; 


class SocialbizChat {
  _root; // Root 타입은 실제로 사용하는 라이브러리에 맞춰 설정
  _backendUrl;
  _starterQuestions;
  _title;
  _imageUrl;
  _windowHeight;
  _windowWidth;

  constructor(backendUrl, starterQuestions, title, imageUrl, windowWidth, windowHeight) {
    this._backendUrl = backendUrl;
    this._starterQuestions = starterQuestions;
    this._title = title;
    this._imageUrl= imageUrl
    this._windowWidth = windowWidth
    this._windowHeight = windowHeight
    this.init();
  }

  // 초기화 메서드
  init() {
    const element = document.createElement('socialbiz-chatbot');
    document.body.appendChild(element);
    this._root = createRoot(element);
    return this;
  }

  // render 메서드
  render() {
    this._root.render(
      <div className="chatbot">
        <ChatUI starterQuestions={this._starterQuestions} 
                title={this._title} 
                imageUrl={this._imageUrl} 
                windowWidth={this._windowWidth} 
                windowHeight={this._windowHeight}/>
      </div>
    );
  }

  // backendUrl 반환 메서드
  getBackendUrl() {
    return this._backendUrl;
  }
}

window.SocialbizChat = (function() {
  return function({ title="CHATBOT", backendUrl, imageUrl, starterQuestions=[], windowWidth="600px", windowHeight="80vh" }) {
    // console.log("=======")
    if (!window.socialbizChat) {
      window.socialbizChat = new SocialbizChat(backendUrl, starterQuestions, title, imageUrl, windowWidth, windowHeight); // 처음 호출 시 인스턴스를 생성
    }
    return window.socialbizChat; // 동일한 인스턴스를 반환
  };
})();



if (process.env.NODE_ENV === 'development') {
    const devRoot = document.querySelector('#_socialbiz_chat');
  
    if (devRoot) {
        window.SocialbizChat({
          title: "🤓 소셜비즈에 대해서 물어보세요~ 🤓",
          // imageUrl: "https://static.wixstatic.com/media/dfd6da_03bb3d558caf4192b5a17864d5441c33~mv2.png/v1/fill/w_970,h_658,al_c,q_90,usm_0.66_1.00_0.01,enc_auto/Group%204612.png",
          imageUrl: "https://socialbiz.gitbook.io/~gitbook/image?url=https%3A%2F%2F1292615749-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FkLJJW5RDkaBvxZmPKudR%252Fuploads%252FoQib1yROMUuazPf2pBXq%252Fwelcome.png%3Falt%3Dmedia%26token%3D1a8c3d6d-4542-4ded-bd8d-5d966e2b6368&width=768&dpr=4&quality=100&sign=6fa2a5c2&sv=1",
          backendUrl: "https://socialbiz-chat.nhndata-bigbrother.link:8989",
          starterQuestions: [
            // "소셜비즈가 뭔가ㅇ요1?",
            // "소셜비즈가 뭔가ㅇ요2 한글 동해물과백두산이 마르고 닳도록?",
            // "소셜비즈가 뭔가ㅇ요3?",
            // "소셜비즈가 뭔가ㅇ요4?",
            "소셜비즈가 뭔가ㅇ요5?",
            "소셜비즈가 뭔가ㅇ요6?",
            "소셜비즈가 뭔가ㅇ요7 한글 동해물과백두산이 마르고 닳도록??",
            "소셜비즈가 뭔가ㅇ요8?",
            "소셜비즈가 뭔가ㅇ요9?",
            "소셜비즈가 뭔가ㅇ요10?",
            "소셜비즈가 뭔가ㅇ요3?",
            "소셜비즈가 뭔가ㅇ요4?",
            "소셜비즈가 뭔가ㅇ요5?",
            "소셜비즈가 뭔가ㅇ요6?",
            "소셜비즈가 뭔가ㅇ요7?",
            "소셜비즈가 뭔가ㅇ요8?",
            "소셜비즈가 뭔가ㅇ요9?",
            // "소셜비즈가 뭔가ㅇ요10?",        
          ]
        }).render() 
        // const root = createRoot(devRoot); // React 18 이상에서는 createRoot 사용
        // root.render(<div className='chatbot'><ChatUI /></div>); // Shadow DOM 안에 ChatContent 컴포넌트 렌더링

    }
}