from fastapi import FastAPI
from atguigu.api.chat_router import chat_router

app = FastAPI()
app.include_router(chat_router)