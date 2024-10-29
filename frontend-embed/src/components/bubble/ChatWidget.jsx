import React, { useState, useRef, useEffect} from "react";

// import icon
import { BsFillChatFill } from "react-icons/bs";
import ModalWindow from './ModalWindow'
import ContentWindowComponent from "../ui/chat/chat-content-window";
import { useLocalStorage } from "../ui/chat/hooks/use-storage";
import { Message } from 'ai/react'

function ChatWidget() {
  const [hovered, setHovered] = useState(false);
  const [visible, setVisible] = useState(false);
  const [localMessages,_] = useLocalStorage('messages', []);
  const widgetRef = useRef(null);

  useEffect(()=>{
    console.log(localMessages)
    if(localMessages.length > 0){
      setVisible(true)
    }
  },[])
  console.log(localMessages)
  console.log(visible)
  return (
    <div>
      {/* Chat Button Component */}
      <div     
        style={{
          ...{ border: hovered ? "1px solid black" : "" },     
          // Position
          position: "fixed",
          bottom: "20px",
          right: "20px",
          backgroundColor: "#cb71e3",
          // Padding
          paddingLeft: "18px",
          paddingRight: "18px",
          paddingTop: "7px",
          paddingBottom: "7px",
          // Border
          borderRadius: "10px",
          //  cursor: "pointer",
          zIndex: 9999                  
        }}
        ref={widgetRef}
      >
        <div className="flex flex-row gap-4" 
            style={{position: 'fixed', bottom: '70px', right: '20px'}}
        >
          <ContentWindowComponent/>   
          <ModalWindow visible={visible}/>
        </div>
        {/* Inner Container */}
        <div         
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
            onClick={() => setVisible(!visible)}
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}              
          >
            {/* Button Icon */}
            <BsFillChatFill size={20} color="white" />
            {/* Button Text */}
            <span style={{    
              color: "white",
              fontSize: "15px",
              marginLeft: "5px",}}>
                Chat Now!!
            </span>            
        </div>
      </div>
    </div>
  );
 }
   
   
export default ChatWidget;