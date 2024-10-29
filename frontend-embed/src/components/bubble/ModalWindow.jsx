// importing external style
import React, { useState, useRef, useEffect} from "react";

import ChatSection from "../ChatSection";
import { useConfigUI } from "../../ChatUIContext";
import { Resizable } from 're-resizable';

function ModalWindow(props) {
    const { windowWidth, windowHeight } = useConfigUI();
    
    return (
            <main className="flex justify-center items-center background-gradient"
                style={{
                    ...{ opacity: props.visible ? "1" : "0" },
                    zIndex:1000,
                    backgroundColor: "white",
                    // Border
                    borderRadius: "12px",
                    border: `2px solid #cb71e3`,
                    overflow: "hidden",
                    // Shadow
                    boxShadow: "0px 0px 16px 6px rgba(0, 0, 0, 0.33)",                    
                }}>  
                <Resizable
                    defaultSize={{
                        width: windowWidth,
                        height: windowHeight,           
                    }} 
                    minWidth="400px" 
                    minHeight="600px"
                    maxWidth="1024px" 
                    maxHeight="90vh"
                    
                >                                     
                    <ChatSection />
                </Resizable>     
            </main>
        // </div>
    )
}
export default ModalWindow;