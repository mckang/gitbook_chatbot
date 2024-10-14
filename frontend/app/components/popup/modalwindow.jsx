// importing external style
import { styles } from "./styles";
import Header from "@/app/components/header";
import ChatSection from "@/app/components/chat-section";
import { Resizable } from 're-resizable';
function ModalWindow(props) {
    // returning display
    return (
         
        <main className="h-screen w-screen flex justify-center items-center background-gradient"
            style={{
                ...styles.modalWindow,
                ...{ opacity: props.visible ? "1" : "0" },
            }}        
            >         
            <Resizable
                defaultSize={{
                    width: "600px",
                    height: "70vh",           
                }} 
                minWidth="600px" 
                minHeight="50vh"
                maxWidth="1024px" 
                maxHeight="90vh"
            >                
                <div className="w-full h-full">
                    {/* <Header /> */}
                    <div className="h-full flex">
                    <ChatSection />
                    </div>
                </div>
            </Resizable>                     
        </main>
         
    );
}
export default ModalWindow;



