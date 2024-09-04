import { Loader2 } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { Button } from "../button";
import ChatActions from "./chat-actions";
import ChatMessage from "./chat-message";
import { ChatHandler } from "./chat.interface";
import { useClientConfig } from "./hooks/use-config";
import { Tooltip } from 'react-tooltip';

import React from "react";

export default function ChatMessages(
  props: Pick<
    ChatHandler,
    "messages" | "isLoading" | "reload" | "stop" | "append"
  >,
) {
  const { backend } = useClientConfig();
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
  }, [starterQuestions, backend]);

  return (
    <div
      className="flex-1 w-full rounded-xl bg-white p-4 shadow-xl relative overflow-y-auto h-full"
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
            <h1 className="text-lg font-semibold">소셜비즈에 대해서 물어보세요!</h1>
          </div>          
          <div className="flex-1 p-4 justify-center items-center">
            <div className="flex h-full text-center  justify-center  items-center">
              <img style={{width: "100%", height: "auto"}} src="https://static.wixstatic.com/media/dfd6da_03bb3d558caf4192b5a17864d5441c33~mv2.png/v1/fill/w_970,h_658,al_c,q_90,usm_0.66_1.00_0.01,enc_auto/Group%204612.png"/>
            </div>
          </div>        
          <div className="flex-none absolute bottom-6 left-0 w-full">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mx-5">
              {starterQuestions.map((question, i) => (
                <Button
                  variant="outline"
                  key={i}
                  onClick={() =>
                    props.append!({ role: "user", content: question })
                  }
                >
                  <div className="overflow-hidden truncate w-30" data-tooltip-id={"tooltip-"+i} data-tooltip-content={question}>
                    {question}
                  </div>
                  <Tooltip place="top" id={"tooltip-"+i} />
                </Button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
