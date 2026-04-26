from src.task import Task
from datetime import datetime
import asyncio
from collections import deque
from typing import Deque


class TaskQueue:
    def __init__(self):
        self._queue: Deque[dict] = deque()
        self._condition = asyncio.Condition()
    
    def __iter__(self):
        return iter(list(self._queue))

    async def add(self, task: Task):
        async with self._condition:
            self._queue.append(task)
            self._condition.notify()
    
    async def get(self) -> Task:
        async with self._condition:
            while not self._queue:
                await self._condition.wait()
            return self._queue.popleft()    

    def filter_by_priority(self, priority: int):
        for task in self._queue:
            if task.priority == priority:
                yield task
    
    def filter_by_date(self, min_date: datetime):
        for task in self._queue:
            if task.created_at >= min_date:
                yield task
    
    def filter_by_days(self, days: int):
        for task in self:
            if (datetime.now() - task.created_at).days <= days:
                yield task

    def filter_by_status(self, status: str):
        for task in self._queue:
            if task.status == status:
                yield task
