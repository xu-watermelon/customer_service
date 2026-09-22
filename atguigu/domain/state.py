from dataclasses import dataclass, field
import uuid
from typing import Any

from jinja2.runtime import F
from atguigu.domain.message import UserMessage, BotMessage
from atguigu.task.lifecycle.models import TaskRef, TaskEvent, TaskSwitched, TaskStarted, TaskCanceled, TaskResumed
import time
@dataclass
class FocusedObject:
    type: str
    id: str
    title: str | None = None
    attributes: dict = field(default_factory=dict)
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
    @classmethod
    def create(cls) -> "Session":
       now = time.time()
       return cls(
           session_id=str(uuid.uuid4()),
           started_at=now,
           last_activity_at=now,
       )

    def close(self) -> None:
        self.closed_at = time.time()

@dataclass
class TaskInstance:
    flow_id: str
    step_id: str | None = None
    slots: dict[str, Any] = field(default_factory=dict)
    task_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )
    def to_ref(self) -> TaskRef:
        return TaskRef(
            task_id=self.task_id,
            flow_id=self.flow_id,
        )
    

@dataclass
class TaskState:
    active: TaskInstance | None = None
    paused: list[TaskInstance] = field(
        default_factory=list
    )
    # 开始任务
    def start(self, task: TaskInstance) -> TaskEvent:
        # 如果有活跃的任务，将其暂停并添加到暂停列表中
        if self.active:
            previous = self.active.to_ref()
            self.paused.append(self.active)
            self.active = task
            current = self.active.to_ref()
            return TaskSwitched(
                previous=previous,
                current=current,
            )
        # 如果没有活跃的任务
        self.active = task
        return TaskStarted(
            task=task.to_ref()
        )
    # 设置任务槽位
    def set_slots(self, slots: dict[str, Any]) -> None:
        self.active.slots.update(slots)
    # 取消任务
    def cancel(self, task_id: str) -> TaskCanceled:
        if self.active is not None and self.active.task_id == task_id:
            canceled = self.active
            self.active = None
            return TaskCanceled(task=canceled.to_ref())

        canceled = next(
            task
            for task in self.paused
            if task.task_id == task_id
        )
        self.paused.remove(canceled)
        return TaskCanceled(task=canceled.to_ref())
    # 恢复任务
    def resume(self, task_id: str) -> TaskEvent:
        target = next(
            task
            for task in self.paused
            if task.task_id == task_id
        )
        self.paused.remove(target)

        if self.active is None:
            self.active = target
            return TaskResumed(task=target.to_ref())

        previous = self.active
        self.paused.append(previous)
        self.active = target
        return TaskSwitched(
            previous=previous.to_ref(),
            current=target.to_ref(),
        )
        # 重置任务状态
    def reset(self) -> None:
        self.active = None
        self.paused.clear()
@dataclass
class SharedState:
    focused_object: FocusedObject | None = None
    sessions: list[Session] = field(
        default_factory=list
    )
    @property
    # 获取当前会话
    def current_session(self) -> Session | None:
        if not self.sessions:
            return None
        return self.sessions[-1]
    # 开始会话
    def start_session(self) -> Session:
        session = Session.create()
        self.sessions.append(session)
        return session
    # 关闭当前会话
    def close_current_session(self) -> None:
        session = self.current_session
        if session is not None:
            session.close()
    # 清除当前会话的焦点对象
    def clear_focus(self) -> None:
        self.focused_object = None

@dataclass
class DialogueState:
    sender_id: str
    shared: SharedState = field(
        default_factory=lambda: SharedState()
    )
    tasks: TaskState = field(
        default_factory=lambda: TaskState()
    )
    def reset_runtime_state_for_new_session(self) -> None:
        self.tasks.reset()
        self.shared.clear_focus()