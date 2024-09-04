import { styles } from "./styles";
import React, { useState, useRef, useEffect} from "react";

// import icon
import { BsFillChatFill } from "react-icons/bs";
import ModalWindow from './ModalWindow'

function ChatWidget() {
  const [hovered, setHovered] = useState(false);
  const [visible, setVisible] = useState(false);

  const widgetRef = useRef(null);

  return (
    <div>
      {/* Chat Button Component */}
      <div     
        style={{
          ...styles.chatWidget,
          ...{ border: hovered ? "1px solid black" : "" },
        }}
        ref={widgetRef}
      >
        <ModalWindow visible={visible}/>

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
            <span style={styles.chatWidgetText}>Chat Now!!</span>            
        </div>
      </div>
    </div>
  );
 }
   
   
export default ChatWidget;