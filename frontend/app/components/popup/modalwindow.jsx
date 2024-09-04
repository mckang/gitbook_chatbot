// importing external style
import { styles } from "./styles";
import Header from "@/app/components/header";
import ChatSection from "@/app/components/chat-section";
function ModalWindow(props) {
    // returning display
    return (
        <main className="h-screen w-screen flex justify-center items-center background-gradient"
            style={{
                ...styles.modalWindow,
                ...{ opacity: props.visible ? "1" : "0" },
             
            }}        
            >
            <div className="w-full h-full">
                {/* <Header /> */}
                <div className="h-full flex">
                <ChatSection />
                </div>
            </div>
        </main>
    );
}
export default ModalWindow;