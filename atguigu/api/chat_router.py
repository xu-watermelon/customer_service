from dataclasses import asdict

from fastapi import APIRouter, Depends
from atguigu.api.schemas import ChatRequest, ChatResponse, ChatMessage
from atguigu.domain.message import UserMessage, MessageType, ProcessResult, MessageObject
import uuid
from atguigu.api.depends import get_dialogue_service


from atguigu.service.dialogue_service import DialogueService

chat_router = APIRouter()





@chat_router.post("/api/chat")
async def chat(chat_request: ChatRequest,dialogue_service: DialogueService=Depends(get_dialogue_service))  -> ChatResponse:
    # 1.接收前端传来的数据封装为ChatRequest模型
    # 2.将ChatRequest模型转换为UserMessage模型
    user_message = _build_user_message(chat_request)
    # 3.调用service层的方法处理数据,返回ProcessResult模型
    process_result: ProcessResult = await dialogue_service.process_message(user_message)
    # 4.将ProcessResult模型转换为ChatResponse模型
    chat_response = _build_chat_response(process_result)
    # 5.返回ChatResponse模型
    return chat_response

def _build_user_message(chat_request: ChatRequest) -> UserMessage:
    return UserMessage(
        sender_id=chat_request.sender_id,
        message_id=chat_request.message_id
            if chat_request.message_id else str(uuid.uuid4()),
        type=MessageType.TEXT if chat_request.text else MessageType.OBJECT,
        text=chat_request.text,
        object=MessageObject(
            type=chat_request.object.type,
            id=str(uuid.uuid4()),
            title=chat_request.object.title,
            attributes=chat_request.object.attributes
        ) if chat_request.object else None
    )

def _build_chat_response(process_result: ProcessResult) -> ChatResponse:
    return ChatResponse(
        sender_id=process_result.sender_id,
        message_id=process_result.message_id,
        messages=[
            ChatMessage(text=message.text, object=ChatObject(**asdict(message.object))if message.object else None)
            for message in process_result.messages
        ]
    )