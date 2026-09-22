from atguigu.domain.message import UserMessage, BotMessage
from atguigu.domain.state import DialogueState
from atguigu.task.command.models import Command
from atguigu.task.command.processor import CommandProcessor
from atguigu.task.flow.executor import FlowExecutor
from atguigu.task.flow.models import FlowCatalog
from atguigu.task.lifecycle.models import TaskEvent
from atguigu.task.lifecycle.responder import TaskLifecycleResponder


class TaskHandler:

    def __init__(self,
                 command_processor: CommandProcessor,
                 task_lifecycle_responder: TaskLifecycleResponder,
                 flow_executor: FlowExecutor,
                 flow_catalog: FlowCatalog):
        self.command_processor = command_processor
        self.task_lifecycle_responder = task_lifecycle_responder
        self.flow_executor = flow_executor
        self.flow_catalog = flow_catalog

    async def handle(self, commands: list[Command], state: DialogueState, user_message: UserMessage) -> list[
        BotMessage]:
        # 1. 执行LLM产出的Command，改动DialogueState，产出状态变化事件
        task_events: list[TaskEvent] = await self.command_processor.process(commands, state, self.flow_catalog)
        # 2. 人性化回复,根据任务事件生成回复消息,放入bot_messages中
        messages: list[BotMessage] = await self.task_lifecycle_responder.respond(task_events)
        # 3. 执行active中的flow,生成回复消息,放入bot_messages中
        messages.extend(await self.flow_executor.run_task(state, self.flow_catalog, user_message))
        return messages
