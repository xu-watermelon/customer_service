from dataclasses import dataclass, field
import uuid
from typing import Any
from atguigu.domain.message import UserMessage, BotMessage

@dataclass
class FocusedObject:
    type: str
    id: str
    title: str | None = None
    attributes: field(
        default_factory=dict
    )
@dataclass
class Turn:
    turn_id: str
    user_message: UserMessage
    bot_messages: list[BotMessage] = field(default_factory=list)


@dataclass
class Session:
    session_id: str
    started_at: float
    last_activity_at: float
    closed_at: float | None = None
    turns: list[Turn] = field(default_factory=list)

@dataclass
class TaskInstance:
    flow_id: str
    step_id: str | None = None
    slots: dict[str, Any] = field(default_factory=dict)
    task_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

@dataclass
class TaskState:
    active: TaskInstance | None = None
    paused: list[TaskInstance] = field(
        default_factory=list
    )

@dataclass
class SharedState:
    focused_object: FocusedObject | None = None
    sessions: list[Session] = field(
        default_factory=list
    )

@dataclass
class DialogueState:
    sender_id: str
    shared: SharedState = field(
        default_factory=lambda: SharedState()
    )
    tasks: TaskState = field(
        default_factory=lambda: TaskState()
    )