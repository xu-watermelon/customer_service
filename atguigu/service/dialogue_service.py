from atguigu.domain.message import UserMessage, ProcessResult, BotMessage
from atguigu.domain.state import DialogueState
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.repository.dialogue_repository import DialogueRepository



class DialogueService:
    # 引入DialogueEngine和DialogueRepository
    def __init__(self,dialogue_engine: DialogueEngine,dialogue_repository: DialogueRepository):
            self.dialogue_engine = dialogue_engine
            self.dialogue_repository = dialogue_repository
    async def process_message(self, user_message: UserMessage) -> ProcessResult:
        # 1.从数据库中获取用户的状态
        dialogue_state: DialogueState = await self.dialogue_repository.load_state(user_message.sender_id)
        # 2.调用DialogueEngine处理用户消息
        process_result: list[BotMessage] = await self.dialogue_engine.process_message(dialogue_state,user_message)
        # 3.将处理结果保存到数据库
        await self.dialogue_repository.save_state(dialogue_state)
        # 4.返回处理结果
        return process_result
