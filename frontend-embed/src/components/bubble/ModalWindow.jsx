// importing external style
import { styles } from "./styles";
import React, { useState, useRef, useEffect} from "react";

import ChatSection from "../ChatSection";
import { useConfigUI } from "../../ChatUIContext";
import { Resizable } from 're-resizable';

function ModalWindow(props) {
    const { windowWidth, windowHeight } = useConfigUI();
    
    return (
            <main className="flex justify-center items-center background-gradient"
                style={{
                    ...styles.modalWindow,
                    ...{ opacity: props.visible ? "1" : "0" },
                    zIndex:1000,
                }}>    
                <Resizable
                    defaultSize={{
                        width: windowWidth,
                        height: windowHeight,           
                    }} 
                    minWidth="600px" 
                    minHeight="700px"
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