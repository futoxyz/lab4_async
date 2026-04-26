import asyncio
from random import randint
from src.task import Task
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='taskexec.log', level=logging.INFO)

class APIHandler:
    async def handle(self, task: Task):
        logger.info(f"Processing API task {task.id}")
        task.status = "in_progress"
        await asyncio.sleep(randint(1, 3))
        task.status = "completed"


class FileHandler:
    async def handle(self, task: Task):
        logger.info(f"Processing file task {task.id}")
        task.status = "in_progress"
        await asyncio.sleep(randint(1, 3))
        task.status = "completed"


class GeneratorHandler:
    async def handle(self, task: Task):
        logger.info(f"Processing generator task {task.id}")
        task.status = "in_progress"
        await asyncio.sleep(randint(1, 3))
        if task.description == 'must fail':
            task.status = "failed"
        else:
            task.status = "completed"