import { RefreshCw, ThumbsDown, ThumbsUp } from "lucide-react";
import { Button } from "../button";
import React, { useState } from 'react';
import { ChatHandler } from "./chat.interface";
import { Message } from "ai";
 
export function UserFeedbackComponent(props: Pick<ChatHandler, "reload"> & { question:Message, answer:Message }) {
  const [feedback, setFeedback] = useState<string | null>(null); // null, 'good', 'bad'

 
  const handleUserFeedback = async (value: string) => {
      setFeedback(value);
      await sendFeedback(value, props.question, props.answer);
  }


  const sendFeedback = async (score: string, question: Message, answer: Message): Promise<void> => {
    try {
      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ score: score, question: question, answer: answer }),
      });
      if (!response.ok) {
        throw new Error('Failed to send feedback');
      }
    } catch (error) {
      console.error(error);
    }
  };    
 
  return (
    <div className="flex flex-col items-center">
      <div className="flex justify-between w-full max-w-md">
        <div className="flex gap-2  ml-auto">     
          {feedback === null || feedback === 'good' ? (
            <Button
              onClick={() => handleUserFeedback("good")}
              size="sm"
              disabled={feedback !== null}
              className={`transition-transform bg-transparent p-2 rounded-full hover:bg-green-100 ${feedback === 'good' ? 'scale-125' : ''} ${feedback !== null ? 'cursor-not-allowed' : 'cursor-pointer'}`}          
              aria-label="Thumbs Up"
            >
              <ThumbsUp color={feedback === 'good' ? 'green' : 'black'} />
            </Button>
          ) : null}
          {feedback === null || feedback === 'bad' ? (        
            <Button
              onClick={() => handleUserFeedback("bad")}
              size="sm"
              disabled={feedback !== null}
              className={`transition-transform bg-transparent p-2 rounded-full hover:bg-red-100 ${feedback === 'bad' ? 'scale-125' : ''} ${feedback !== null ? 'cursor-not-allowed' : 'cursor-pointer'}`}          
              aria-label="Thumbs Down"
            >
              <ThumbsDown color={feedback === 'bad' ? 'red' : 'black'}  />
            </Button>    
          ) : null}
          <Button size="sm" onClick={props.reload} className="bg-transparent  hover:bg-gray-100 cursor-pointer">
            <RefreshCw color='black'/>
          </Button>          
        </div>
      </div>
    </div>
  );
}