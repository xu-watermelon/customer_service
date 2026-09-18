from atguigu.domain.stata import DialogueState
from atguigu.domain.message import UserMessage, BotMessage, ProcessResult

class DialogueEngine:
     async def process_message(
        self,
        state: DialogueState,
        user_message: UserMessage,
    ) -> ProcessResult:
        ...