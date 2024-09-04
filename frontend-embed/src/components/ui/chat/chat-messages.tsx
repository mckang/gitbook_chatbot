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

export default function ChatMessages(
  props: Pick<
    ChatHandler,
    "messages" | "isLoading" | "reload" | "stop" | "append"
  >,
) {
  const { backend } = useClientConfig();
  const { starterQuestions: customQuestions, title, imageUrl } = useConfigUI();
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
    console.log("title",title)
    console.log("title",imageUrl)

    // console.log("customQuestions",customQuestions)
    
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

  return (
    <div
      className="flex-1 w-full rounded-xl bg-white p-4 shadow-xl relative overflow-y-auto"
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
            <Loader2 className="h-4 w-4 animate-spin" />
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
          />
        </div>
      )}
      {!messageLength && starterQuestions?.length && props.append && (
        <div className="flex flex-col h-full justify-center items-center">
          <div className="bg-purple-600 text-white p-4 rounded-t-lg w-full text-center">
            <h1 className="text-lg font-semibold">{title}</h1>
          </div>          
          <div className="flex-1 py-4 justify-center items-center">
            <div className="flex h-full text-center  justify-center  items-center">
              <img style={{width: "100%", height: "auto"}} src={imageUrl}/>
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
