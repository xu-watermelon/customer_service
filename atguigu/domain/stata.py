from dataclasses import dataclass, field
from typing import Any

from atguigu.domain.message import BotMessage, UserMessage
from atguigu.domain.task import TaskState, SharedState

@dataclass
class DialogueState:
    sender_id: str
    shared: SharedState = field(
        default_factory=lambda: SharedState()
    )
    tasks: TaskState = field(
        default_factory=lambda: TaskState()
    )