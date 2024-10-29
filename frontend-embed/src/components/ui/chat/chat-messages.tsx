import { Loader2 } from "lucide-react";
import { useEffect, useRef, useState, useContext } from "react";

import { Button } from "../button";
import ChatActions from "./chat-actions";
import ChatMessage from "./chat-message";
import { ChatHandler } from "./chat.interface";
import { useClientConfig } from "./hooks/use-config";
// import { Tooltip } from 'react-tooltip';
import Tooltip from '../Tooltip'

import React from "react";
import { useConfigUI } from "../../../ChatUIContext";
// import ContentWindowComponent from "./chat-content-window";
import { useLocalStorage } from "./hooks/use-storage";
import { Message } from "ai";

export default function ChatMessages(
  props: Pick<
    ChatHandler,
    "messages" | "isLoading" | "reload" | "stop" | "append"
  >,
) {
  const { backend } = useClientConfig();
  const { starterQuestions: customQuestions, title, imageUrl } = useConfigUI();
  const [_, saveMessages] = useLocalStorage<Message[]>('messages', []);
  const [starterQuestions, setStarterQuestions] = useState<string[]>();



  const scrollableChatContainerRef = useRef<HTMLDivElement>(null);
  const messageLength = props.messages.length;
  const lastMessage = props.messages[messageLength - 1];

  const scrollToBottom = () => {
    if (scrollableChatContainerRef.current) {
      scrollableChatContainerRef.current.scrollTop =
        scrollableChatContainerRef.current.scrollHeight;
    }
  };

  const isLastMessageFromAssistant =
    messageLength > 0 && lastMessage?.role !== "user";
  const showReload =
    props.reload && !props.isLoading && isLastMessageFromAssistant;
  const showStop = props.stop && props.isLoading;

  // `isPending` indicate
  // that stream response is not yet received from the server,
  // so we show a loading indicator to give a better UX.
  const isPending = props.isLoading && !isLastMessageFromAssistant;

  useEffect(() => {
    scrollToBottom();
  }, [messageLength, lastMessage]);

  useEffect(() => {
    
    if(customQuestions.length > 0){
      setStarterQuestions(customQuestions.length > 10 ? customQuestions.slice(0, 10) : customQuestions)
    } else {
      if (!starterQuestions) {
        fetch(`${backend}/api/chat/config`)
          .then((response) => response.json())
          .then((data) => {
            if (data?.starterQuestions) {
              setStarterQuestions(data.starterQuestions);
            }
          })
          .catch((error) => console.error("Error fetching config", error));
      }
    }
  }, []);

  useEffect(() => {

    if (showReload) {
      // console.log(props.messages)
      saveMessages(props.messages.slice(-10))
    }    
  }, [showReload]);

  const divStyle = {
    width: "90%",
    height: "400px",
    backgroundImage: `url(${imageUrl})`, // 여기에 이미지 경로를 지정
    // backgroundSize: "cover", // 이미지가 div의 크기에 맞춰지도록 함
    // backgroundPosition: "center", // 이미지의 중심을 div의 중앙에 위치
    backgroundSize: "contain", // 이미지가 div의 크기에 맞춰지도록 함
    backgroundPosition: "center", // 이미지의 중심을 div의 중앙에 위치
    backgroundRepeat: "no-repeat", // 이미지를 반복하지 않도록 설정    
  };  

  return (
    <div
      className="flex-1 w-full rounded-xl bg-white p-2 shadow-xl relative overflow-y-auto"
      ref={scrollableChatContainerRef}
    >
      <div className="flex flex-col gap-5 divide-y">
        {props.messages.map((m, i) => {
          const isLoadingMessage = i === messageLength - 1 && props.isLoading;
          // console.log(m)
          return (
            <ChatMessage
              key={m.id}
              chatMessage={m}
              isLoading={isLoadingMessage}
              append={props.append!}
            />
          );
        })}
        {isPending && (
          <div className="flex justify-center items-center pt-10">
            <Loader2 className="h-4 w-4 animate-spin" /> <strong style={{fontSize: '14px'}}>  자료 검색 중 ...</strong> 
          </div>
        )}
      </div>
      {(showReload || showStop) && (
        <div className="flex justify-end py-4">
          <ChatActions
            reload={props.reload}
            stop={props.stop}
            showReload={showReload}
            showStop={showStop}
            messages={props.messages}
          />
        </div>
      )}
      {!messageLength && starterQuestions?.length && props.append && (
        <div className="flex flex-col h-full justify-center items-center">
          <div className="bg-purple-600 text-white p-4 rounded-t-lg w-full text-center">
            <h1 className="text-lg font-semibold">{title}</h1>
          </div>          
          <div style={divStyle} className="flex-1 py-4 justify-center items-center">
            <div className="flex h-full text-center  justify-center  items-center">
              {/* <img style={{width: 400, height: "auto"}} src={imageUrl}/> */}
            </div>
          </div>        
          <div className="flex-none bottom-6 left-0 w-full">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {starterQuestions.map((question, i) => (                
                <Button
                  variant="outline"
                  key={i}
                  onClick={() =>
                    props.append!({ role: "user", content: question })
                  }
                >
                  <Tooltip key={"tooltip-"+i} text={question}>
                    <div className="overflow-hidden truncate w-30">
                      {question}
                    </div>
                  </Tooltip>
                </Button>
              ))}
            </div>
          </div>
        </div>
      )}     
    </div>
  );
}
