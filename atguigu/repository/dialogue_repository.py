from sqlalchemy.ext.asyncio import AsyncSession
from atguigu.domain.stata import DialogueState
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from atguigu.repository.orm.dialogue_state import DialogueStateRecord


DIALOGUE_STATE_ADAPTER = TypeAdapter(DialogueState)

class DialogueRepository:
    def __init__(self,session: AsyncSession):
        self.session = session
    # 加载对话状态
    async def load_state(
        self,
        sender_id: str,
    ) -> DialogueState:
        statement = select(DialogueStateRecord).where(DialogueStateRecord.sender_id == sender_id)

        result = await self.session.execute(statement)
        record = result.scalar_one_or_none()
        if record is None:
            return DialogueState(sender_id=sender_id)
        return DIALOGUE_STATE_ADAPTER.validate_json(record.state_json)

    # 保存对话状态
    async def save_state(
        self,
        state: DialogueState,
    ) -> None:
        state_json = DIALOGUE_STATE_ADAPTER.dump_json(
            state
        ).decode("utf-8")

        statement = insert(DialogueStateRecord).values(
            sender_id=state.sender_id,
            state_json=state_json,
        )
        statement = statement.on_duplicate_key_update(
            state_json=state_json
        )

        await self.session.execute(statement)
        await self.session.commit()