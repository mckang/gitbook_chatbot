import streamlit as st
from streamlit_pills import pills
from app.utils import build_chat_engine
import json


st.set_page_config(
    page_title="SocialBiz 가이드 봇",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("SocialBiz 가이드 봇 💬")
st.info(
    "인스타그램 DM 마케팅 자동화 솔루션 SocialBiz 상담 봇입니다."
    ,
    icon="ℹ️",
)

st.info(f"자세한 내용은 사이트( https://socialbiz.gitbook.io/ )에서 확인해 주세요", icon="ℹ️")

    
if "messages" not in st.session_state.keys():  
    st.session_state.messages = [
        {"role": "assistant", "content": "소셜비즈에 대해서 물어보세요."}
    ]


if "promptstring" not in st.session_state.keys():  
    st.session_state.promptstring = ""  


def add_to_message_history(role: str, content: str, links = [], imgs = [], nexts = []) -> None:
    message = {"role": role, "content": str(content), "links":links, "imgs":imgs, "nexts":nexts}
    st.session_state.messages.append(message)  # Add response to message history

def doAsk(user_message):
    add_to_message_history("user", user_message)
    with st.chat_message("user"):
        st.write(user_message)

    dummy = None
    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_stream = st.session_state.chat_engine.stream_chat(user_message)
                st.write_stream(response_stream.response_gen)
                # response_stream =  st.session_state.chat_engine.chat(prompt)
                # st.write(response_stream.response)
            
                links = [ nodeWithScore.node.metadata.get('links',[]) for nodeWithScore in response_stream.source_nodes if nodeWithScore.score >= 9.0]
                nexts = [ nodeWithScore.node.metadata.get('nexts',[]) for nodeWithScore in response_stream.source_nodes if nodeWithScore.score >= 9.0]
                links = [ json.loads(link) for link in links]
                nexts = [ json.loads(next) for next in nexts]
                links = [item for sublist in links for item in sublist]
                nexts = [item for sublist in nexts for item in sublist]
                imgs = list(filter(lambda link: link.get('type','') == "img", links))
                imgs = list(filter(lambda img: not img.get("desc","").startswith("이미지"), imgs))

                links = list(filter(lambda link: link.get('type','') == "link", links))
                if links:
                    st.write("[[참고 링크]]")
                    
                    for link in links:
                        link_url = link.get("link") if link.get("link").startswith(("http","https")) else "https://socialbiz.gitbook.io" + link.get("link")
                        st.write("[" +link.get("desc") + "](%s)" % link_url)
                if imgs:
                    st.write("[[참고 이미지]]")
                    imgs=imgs[:2]
                    for img in imgs:                            
                        st.image(img.get("link"), caption=img.get("desc"))    

                if nexts:
                    st.write("[[더 알아보기]]")
                    for next in nexts:                             
                        st.write(" - "+next)   

                               
                add_to_message_history("assistant", str(response_stream.response), links, imgs, nexts)
  

for message in st.session_state.messages:  # Display the prior chat messages

    with st.chat_message(message["role"]):
        st.write(message["content"])
        links = message.get("links")
        imgs = message.get("imgs")
        nexts = message.get("nexts")

        if links:
            st.write("[[참고 링크]]")
            
            for link in links:
                link_url = link.get("link") if link.get("link").startswith(("http","https")) else "https://socialbiz.gitbook.io" + link.get("link")
                st.write("[" +link.get("desc") + "](%s)" % link_url)
        if imgs:
            st.write("[[참고 이미지]]")
            for img in imgs:
                st.image(img.get("link"), caption=img.get("desc"))   
        if nexts:
            st.write("[[더 알아보기]]")
            for next in nexts:                             
                st.write(" - "+next)                   
                                   

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = build_chat_engine()

      

if prompt := st.chat_input(
    st.session_state.promptstring,
):  # Prompt for user input and save to chat history
    doAsk(prompt)
