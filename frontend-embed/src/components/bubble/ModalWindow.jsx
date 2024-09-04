// importing external style
import { styles } from "./styles";
import React, { useState, useRef, useEffect} from "react";

import ChatSection from "../ChatSection";
import { useConfigUI } from "../../ChatUIContext";
function ModalWindow(props) {
    const { windowWidth, windowHeight } = useConfigUI();

    const [size, setSize] = useState({ width: windowWidth, height: windowHeight });
    const [isResizing, setIsResizing] = useState(false);

    const handleMouseDown = (e) => {
        setIsResizing(true);
      };
    
    const handleMouseMove = (e) => {
        if (!isResizing) return;
        // 마우스의 현재 위치로 width와 height 업데이트
        setSize({
          width: e.clientX - e.target.offsetLeft,
          height: e.clientY - e.target.offsetTop,
        });
    };

    const handleMouseUp = () => {
        setIsResizing(false);
    };    

    
    return (
        // <div className="tailwind-container">
            <main className="h-screen w-screen flex justify-center items-center background-gradient"
                style={{
                    ...styles.modalWindow,
                    ...{ opacity: props.visible ? "1" : "0" },
                    width: size.width, height: size.height,
                    minWidth: size.width, minHeight: size.height,
                    zIndex:1000,
                }}  
                // onMouseMove={handleMouseMove}
                // onMouseUp={handleMouseUp}
                // onMouseLeave={handleMouseUp}                      
                >
                <ChatSection />
                {/* <div
                    className="resize-handle"
                    onMouseDown={handleMouseDown}
                    style={{
                    width: "10px",
                    height: "10px",
                    background: "gray",
                    position: "absolute",
                    left: 0,
                    top: 0,
                    cursor: "nwse-resize",
                    }}
                />                 */}
            </main>
        // </div>
    )
}
export default ModalWindow;