import json
import random

from aiostream import stream
from fastapi import Request
from fastapi.responses import StreamingResponse
from llama_index.core.chat_engine.types import StreamingAgentChatResponse

from app.api.routers.events import EventCallbackHandler
from app.api.routers.models import ChatData, Message, SourceNodes
from app.api.services.suggestion import NextQuestionSuggestion


class VercelStreamResponse(StreamingResponse):
    """
    Class to convert the response from the chat engine to the streaming format expected by Vercel
    """

    TEXT_PREFIX = "0:"
    DATA_PREFIX = "8:"

    @classmethod
    def convert_text(cls, token: str):
        # Escape newlines and double quotes to avoid breaking the stream
        token = json.dumps(token)
        return f"{cls.TEXT_PREFIX}{token}\n"

    @classmethod
    def convert_data(cls, data: dict):
        data_str = json.dumps(data)
        return f"{cls.DATA_PREFIX}[{data_str}]\n"

    def __init__(
        self,
        request: Request,
        event_handler: EventCallbackHandler,
        response: StreamingAgentChatResponse,
        chat_data: ChatData,
    ):
        content = VercelStreamResponse.content_generator(
            request, event_handler, response, chat_data
        )
        super().__init__(content=content)

    @staticmethod
    def remove_duplicates(dict_list):
        seen = set()
        unique_list = []
        for d in dict_list:
            # 문자열로 변환
            tuple_representation = d.get("link", "")
            if tuple_representation not in seen:
                seen.add(tuple_representation)
                unique_list.append(d)
        return unique_list

    @classmethod
    async def content_generator(
        cls,
        request: Request,
        event_handler: EventCallbackHandler,
        response: StreamingAgentChatResponse,
        chat_data: ChatData,
    ):
        # Yield the text response
        async def _chat_response_generator():
            final_response = ""
            async for token in response.async_response_gen():
                final_response += token
                yield VercelStreamResponse.convert_text(token)

            # links = [ nodeWithScore.node.metadata.get('links',[]) for nodeWithScore in response.source_nodes if nodeWithScore.score >= 10.0]
            links = [ nodeWithScore.node.metadata.get('links',[]) for nodeWithScore in response.source_nodes if "(%s)"%nodeWithScore.node.metadata.get('source','') in final_response]
            nexts = [ nodeWithScore.node.metadata.get('nexts',[]) for nodeWithScore in response.source_nodes if "(%s)"%nodeWithScore.node.metadata.get('source','') in final_response]

            # nexts = [ nodeWithScore.node.metadata.get('nexts',[]) for nodeWithScore in response.source_nodes if nodeWithScore.score >= 9.0]
            links = [ json.loads(link) for link in links]
            nexts = [ json.loads(next) for next in nexts]
            links = [item for sublist in links for item in sublist]
            nexts = [item for sublist in nexts for item in sublist]

            # for nodeWithScore in response.source_nodes:
            #     print("(%s)"%nodeWithScore.node.metadata.get('source','')  , nodeWithScore.score)
            #     print(nodeWithScore.node.metadata.get('links',[]))

            imgs = list(filter(lambda link: link.get('type','') == "img", links))
            imgs = list(filter(lambda img: not img.get("desc","").startswith("이미지"), imgs))
            links = list(filter(lambda link: link.get('type','') == "link", links))



            imgs = VercelStreamResponse.remove_duplicates(imgs)
            links = VercelStreamResponse.remove_duplicates(links)

            if imgs:        
                random.shuffle(imgs) 
                imgs=imgs[:2]
                _imgs = []
                for img in imgs:          
                    _imgs.append({
                         "url": img.get("link"),            
                         "desc": img.get("desc")          
                    })

                yield VercelStreamResponse.convert_data(
                    {
                        "type": "images",
                        "data": _imgs
                    }
                ) 


            if links:
                _links = []
                for link in links:
                    link_url = link.get("link") if link.get("link").startswith(("http","https")) else "https://socialbiz.gitbook.io" + link.get("link")   
                    _links.append({
                         "url": link_url,            
                         "desc": link.get("desc")         
                    })                                                      

                yield VercelStreamResponse.convert_data(
                    {
                        "type": "links",
                        "data": _links
                    }
                ) 

            if nexts:
                conversation = chat_data.messages + [
                    Message(role="assistant", content=final_response)
                ]
                questions = await NextQuestionSuggestion.suggest_next_questions(
                    conversation, nexts
                )
                if len(questions) > 0:
                    yield VercelStreamResponse.convert_data(
                        {
                            "type": "suggested_questions",
                            "data": questions,
                        }
                    )                

            # the text_generator is the leading stream, once it's finished, also finish the event stream
            event_handler.is_done = True

            # Yield the source nodes
            # yield cls.convert_data(
            #     {
            #         "type": "sources",
            #         "data": {
            #             "nodes": [
            #                 SourceNodes.from_source_node(node).model_dump()
            #                 for node in response.source_nodes
            #             ]
            #         },
            #     }
            # )

        # Yield the events from the event handler
        async def _event_generator():
            async for event in event_handler.async_event_gen():
                event_response = event.to_response()
                if event_response is not None:
                    yield VercelStreamResponse.convert_data(event_response)

        combine = stream.merge(_chat_response_generator(), _event_generator())
        is_stream_started = False
        async with combine.stream() as streamer:
            async for output in streamer:
                if not is_stream_started:
                    is_stream_started = True
                    # Stream a blank message to start the stream
                    yield VercelStreamResponse.convert_text("")

                yield output
                # print(output)
                if await request.is_disconnected():
                    break
