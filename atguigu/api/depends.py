from atguigu.repository.dialogue_repository import DialogueRepository
from atguigu.service.dialogue_service import DialogueService
from fastapi import Depends
from atguigu.engine.dialogue_engine import DialogueEngine
from atguigu.utils import database
from atguigu.utils.database import AsyncSession

async def get_db_session() -> AsyncSession:
    # 每次调用时实时读取 database.session_factory，拿到 init 之后的最新值
    async with database.session_factory() as session:
        yield session

async def get_dialogue_engine() -> DialogueEngine:
    return DialogueEngine(
    )


async def get_dialogue_repository(session: AsyncSession=Depends(get_db_session)) -> DialogueRepository:
    return DialogueRepository(session)


async def get_dialogue_service(dialogue_engine:DialogueEngine = Depends(get_dialogue_engine),dialogue_repository:DialogueRepository = Depends(get_dialogue_repository)) -> DialogueService:
    return DialogueService(
       dialogue_engine=dialogue_engine,
       dialogue_repository=dialogue_repository,
    )
