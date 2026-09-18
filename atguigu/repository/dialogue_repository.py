from sqlalchemy.ext.asyncio import AsyncSession
from atguigu.domain.stata import DialogueState

class DialogueRepository:
    def __init__(self,session: AsyncSession):
        self.session = session

    async def load_state(
        self,
        sender_id: str,
    ) -> DialogueState:
        ...

    async def save_state(
        self,
        state: DialogueState,
    ) -> None:
        ...