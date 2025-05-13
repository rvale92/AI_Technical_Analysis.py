import streamlit as st
from typing import List, Dict, Optional, Callable
from datetime import datetime
from enum import Enum, auto
from dataclasses import dataclass
from uuid import uuid4

class TaskStatus(Enum):
    """Enum for task status"""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

@dataclass
class Task:
    """Represents an analysis task"""
    id: str
    name: str
    description: str
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    result: Optional[Dict] = None
    dependencies: List[str] = None

class TaskManager:
    """Manages analysis tasks"""
    
    TASKS_KEY = "analysis_tasks"
    
    @classmethod
    def init_tasks(cls) -> None:
        """Initialize tasks in session state"""
        if cls.TASKS_KEY not in st.session_state:
            st.session_state[cls.TASKS_KEY] = {}
    
    @classmethod
    def create_task(cls, name: str, description: str, dependencies: List[str] = None) -> str:
        """Create a new task"""
        cls.init_tasks()
        task_id = str(uuid4())
        task = Task(
            id=task_id,
            name=name,
            description=description,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            dependencies=dependencies or []
        )
        st.session_state[cls.TASKS_KEY][task_id] = task
        return task_id
    
    @classmethod
    def start_task(cls, task_id: str) -> None:
        """Start a task"""
        cls.init_tasks()
        if task_id in st.session_state[cls.TASKS_KEY]:
            task = st.session_state[cls.TASKS_KEY][task_id]
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
    
    @classmethod
    def complete_task(cls, task_id: str, result: Dict = None) -> None:
        """Mark a task as completed"""
        cls.init_tasks()
        if task_id in st.session_state[cls.TASKS_KEY]:
            task = st.session_state[cls.TASKS_KEY][task_id]
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
    
    @classmethod
    def fail_task(cls, task_id: str, error: str) -> None:
        """Mark a task as failed"""
        cls.init_tasks()
        if task_id in st.session_state[cls.TASKS_KEY]:
            task = st.session_state[cls.TASKS_KEY][task_id]
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            task.error = error
    
    @classmethod
    def cancel_task(cls, task_id: str) -> None:
        """Cancel a task"""
        cls.init_tasks()
        if task_id in st.session_state[cls.TASKS_KEY]:
            task = st.session_state[cls.TASKS_KEY][task_id]
            task.status = TaskStatus.CANCELLED
            task.completed_at = datetime.now()
    
    @classmethod
    def get_task(cls, task_id: str) -> Optional[Task]:
        """Get a specific task"""
        cls.init_tasks()
        return st.session_state[cls.TASKS_KEY].get(task_id)
    
    @classmethod
    def get_all_tasks(cls) -> Dict[str, Task]:
        """Get all tasks"""
        cls.init_tasks()
        return st.session_state[cls.TASKS_KEY]
    
    @classmethod
    def get_pending_tasks(cls) -> List[Task]:
        """Get all pending tasks"""
        return [
            task for task in cls.get_all_tasks().values()
            if task.status == TaskStatus.PENDING
        ]
    
    @classmethod
    def get_running_tasks(cls) -> List[Task]:
        """Get all running tasks"""
        return [
            task for task in cls.get_all_tasks().values()
            if task.status == TaskStatus.RUNNING
        ]
    
    @classmethod
    def clear_completed_tasks(cls) -> None:
        """Clear all completed tasks"""
        cls.init_tasks()
        st.session_state[cls.TASKS_KEY] = {
            task_id: task
            for task_id, task in st.session_state[cls.TASKS_KEY].items()
            if task.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]
        } 