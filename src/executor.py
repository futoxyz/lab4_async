from typing import Protocol, runtime_checkable
from src.task import Task
from src.queue import TaskQueue
from random import randint
import asyncio

@runtime_checkable
class TaskHandler(Protocol):
    async def handle(self, task: Task): ...


class APIHandler:
    async def handle(self, task: Task):
        print(f"{task.id} is started")
        task.status = "in_progress"
        await asyncio.sleep(randint(3,5))
        task.status = "completed"


class TaskExecutor:
    def __init__(self, queue: TaskQueue, max_workers: int = 5):
        self.queue = queue
        self.max_workers = max_workers
        self.handlers: dict[str, TaskHandler] = {}
        self._running = False
        self._workers = []
    
    def register_handler(self, task_type: str, handler: TaskHandler):
        if not isinstance(handler, TaskHandler):
            raise
        self._handlers[task_type] = handler
    
    def _worker(self, worker_id: int):
        while self._running:
            try:
                task = await self.queue.get()
                task_type = task.get('type', 'default')
                handler = self.handlers.get(task_type)
                if not handler:
                    continue
                await hander.handle(task)
            except Exception:
                raise