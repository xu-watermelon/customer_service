from dataclasses import dataclass, field


@dataclass
class SharedState:
    """对话级共享状态（占位，课程后续补充字段）"""
    pass


@dataclass
class TaskState:
    """任务状态（占位，课程后续补充字段）"""
    current_task: str | None = None
