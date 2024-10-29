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
  _gitbookUrl;
  _contextPath;
  _windowHeight;
  _windowWidth;
  _embedDocSite;

  constructor(backendUrl, starterQuestions, title, imageUrl, gitbookUrl, contextPath=null, windowWidth, windowHeight,embedDocSite) {
    this._backendUrl = backendUrl;
    this._starterQuestions = starterQuestions;
    this._title = title;
    this._imageUrl= imageUrl;
    this._gitbookUrl = gitbookUrl;
    this._contextPath = contextPath
    this._windowWidth = windowWidth;
    this._windowHeight = windowHeight;
    this._embedDocSite = embedDocSite;
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
                gitbookUrl={this._gitbookUrl}
                contextPath={this._contextPath}
                windowWidth={this._windowWidth} 
                windowHeight={this._windowHeight}
                embedDocSite={this._embedDocSite}/>
      </div>
    );
  }

  // backendUrl 반환 메서드
  getBackendUrl() {
    return this._backendUrl;
  }
}

window.SocialbizChat = (function() {
  return function({ title="CHATBOT", backendUrl, imageUrl, gitbookUrl, contextPath, 
                    starterQuestions=[], windowWidth=600, windowHeight=600, embedDocSite=true }) {
    if (!window.socialbizChat) {
      window.socialbizChat = new SocialbizChat(backendUrl, starterQuestions, title, imageUrl, gitbookUrl, contextPath,
                                                windowWidth, windowHeight, embedDocSite); // 처음 호출 시 인스턴스를 생성
    }
    return window.socialbizChat; // 동일한 인스턴스를 반환
  };
})();



if (process.env.NODE_ENV === 'development') {
    const devRoot = document.querySelector('#_socialbiz_chat');
  
    if (devRoot) {
        window.SocialbizChat({
          title: "🤓 소셜비즈에 대해서 물어보세요~ 🤓",
          imageUrl: "https://static.wixstatic.com/media/dfd6da_03bb3d558caf4192b5a17864d5441c33~mv2.png/v1/fill/w_970,h_658,al_c,q_90,usm_0.66_1.00_0.01,enc_auto/Group%204612.png",
          gitbookUrl: "https://socialbiz.gitbook.io",
          backendUrl: "https://socialbiz-chat.nhndata-bigbrother.link:8989",
          // contextPath: "/docs",
          windowWidth: 400,
          windowHeight: 600,          
          starterQuestions: [
            "Socialbiz가 뭔가요?",
            "Socialbiz를 통해 자동화할 수 있는 메시지 유형은 뭔가요?",
            "Socialbiz 활용 시나리오를 알려주세요",
            "Socialbiz 이용 요금은 어떻게 되나요?",
            "Socialbiz 사용자 인터뷰",
            "인스타그램 전환 분석도 가능한가요?",            
          ],
          embedDocSite: false
        }).render() 
    }
}