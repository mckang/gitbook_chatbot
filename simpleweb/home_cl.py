import chainlit as cl
from app.utils import build_chat_engine
import json

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="소셜비즈란?",
            message="소셜비즈가 뭔가요?",
            icon="/public/learn.svg",
            ),

        cl.Starter(
            label="소셜비즈를 통해 자동화할 수 있는 메시지 유형?",
            message="Socialbiz를 통해 자동화할 수 있는 메시지 유형은 뭔가요?",
            icon="/public/learn.svg",
            ),
        cl.Starter(
            label="활용 시나리오는?",
            message="소셜비즈로 활용 가능한 시나리오를 알려주세요",
            icon="/public/learn.svg",
            ),
        cl.Starter(
            label="이용 요금은?",
            message="소셜비즈의 이용 요금은 어떻게 되나요?",
            icon="/public/learn.svg",
            )
        ]

@cl.on_chat_start
async def start():
    cl.user_session.set("chat_engine", build_chat_engine())
    
    # await cl.Message(
    #     author="Assistant", content="인스타그램 DM 마케팅 자동화 솔루션 SocialBiz 상담 봇입니다."
    # ).send()

@cl.action_callback("do_more")
async def on_action(action: cl.Action):
    await doMessaging(action.value)
    return 


@cl.on_message
async def main(message: cl.Message):
    await doMessaging(message.content)

async def doMessaging(content: str):
    chat_engine = cl.user_session.get("chat_engine")
    msg = cl.Message(content="")
    await msg.send()

    # response_stream = chat_engine.stream_chat(message.content)

    response_stream = await cl.make_async(chat_engine.stream_chat)(content)

    # async for part in response_stream.response_gen:
    for part in response_stream.response_gen:        
        await msg.stream_token(part)   
    await msg.update()

    links = [ nodeWithScore.node.metadata.get('links',[]) for nodeWithScore in response_stream.source_nodes if nodeWithScore.score == 10.0]
    nexts = [ nodeWithScore.node.metadata.get('nexts',[]) for nodeWithScore in response_stream.source_nodes if nodeWithScore.score >= 9.0]
    links = [ json.loads(link) for link in links]
    nexts = [ json.loads(next) for next in nexts]
    links = [item for sublist in links for item in sublist]
    nexts = [item for sublist in nexts for item in sublist]
    imgs = list(filter(lambda link: link.get('type','') == "img", links))
    imgs = list(filter(lambda img: not img.get("desc","").startswith("이미지"), imgs))
    links = list(filter(lambda link: link.get('type','') == "link", links))

    if links:
        await msg.stream_token("\n\n")
        await msg.stream_token("[[참고 링크]]")
        await msg.stream_token("\n")
        for link in links:
            link_url = link.get("link") if link.get("link").startswith(("http","https")) else "https://socialbiz.gitbook.io" + link.get("link")
            await msg.stream_token("- [" +link.get("desc") + "](%s)" % link_url)
            await msg.stream_token("\n")
    if imgs:
        await msg.stream_token("\n\n")
        await msg.stream_token("[[참고 이미지]]")
        await msg.stream_token("\n")
        imgs=imgs[:2]
        for img in imgs:         
            # await msg.stream_token(f'<img src="{img.get("link")}" alt="{img.get("desc")}" width="300px">')       
            await msg.stream_token(img.get("desc")+"\n")            
            await msg.stream_token("![" +img.get("desc") + "](%s)" % img.get("link"))
            # await msg.stream_token("![" +img.get("desc") + "](%s){width=300}" % img.get("link"))
            await msg.stream_token("\n")            
    await msg.update()

    if nexts:
        # await msg.stream_token("\n\n")        
        # await msg.stream_token("[[더 알아보기]]")
        # await msg.stream_token("\n")
        # for next in nexts:                             
        #     await msg.stream_token("- "+next)   
        #     await msg.stream_token("\n")
        actions = []
        for next in nexts:
            if next == content:
                continue
            actions.append(cl.Action(name="do_more", value=next, description=next,label=next ))
        if actions:
            await cl.Message(content="연관 주제 알아보기", actions=actions).send()            