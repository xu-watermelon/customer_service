from atguigu.domain.state import DialogueState, Turn
from atguigu.domain.message import UserMessage, BotMessage, ProcessResult
from atguigu.plan.turn_planner import TurnPlanner
from atguigu.plan.validator import TurnPlanValidator
from atguigu.task.handler import TaskHandler
from atguigu.domain.message import MessageType
import uuid
import time

class DialogueEngine:
    def __init__(self, turn_planner: TurnPlanner,
                 turn_plan_validator: TurnPlanValidator,
                 task_handler: TaskHandler,
    ):
        self.turn_planner = turn_planner
        self.turn_plan_validator = turn_plan_validator
        self.task_handler = task_handler



    async def process_message(
        self,
        state: DialogueState,
        user_message: UserMessage,
    ) -> ProcessResult:
        # 1.准备当前session
        self._prepare_session(state)
        # 2.准备当前turn
        # state.shared.sessions[-1].turns
        turn = Turn(turn_id=uuid.uuid4(),user_message=user_message)
        # 3.判断当前传入类型
        #    1.文本消息
        if user_message.type == MessageType.TEXT:
            messages: list[BotMessage] = self._execute_text_message(state, turn)
        #    2.对象消息
        elif user_message.type == MessageType.OBJECT:
            messages: list[BotMessage] = self._execute_object_message(state, turn)

        # 4.更新当前turn
        turn.bot_messages.extend(messages)
        # 5.更新当前session
        state.shared.sessions[-1].turns.append(turn)

        return ProcessResult(
            sender_id=user_message.sender_id,
            messages=messages,
            message_id=user_message.message_id
        )
        

    # 准备当前session
    def _prepare_session(
        self,
        state: DialogueState,
    ) -> None:
        session = state.shared.current_session

        if session is None:
            state.shared.start_session()
        elif time.time() - session.last_activity_at > 60 * 60:
            state.shared.close_current_session()
            state.reset_runtime_state_for_new_session()
            state.shared.start_session()

    def _execute_text_message(self, state: DialogueState, turn: Turn) -> list[BotMessage]:
        ...
    def _execute_object_message(self, state: DialogueState, turn: Turn) -> list[BotMessage]:
        ...