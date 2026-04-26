from src.handlers import TaskHandler
from src.queue import TaskQueue
import asyncio
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='taskexec.log', level=logging.INFO)


class TaskExecutor:
    def __init__(self, queue: TaskQueue, max_workers: int = 5):
        self.queue = queue
        self.max_workers = max_workers
        self.handlers: dict[str, TaskHandler] = {}
        self._running = False
        self._workers = []
        self.history = []
    
    def register_handler(self, task_type: str, handler: TaskHandler):
        if not isinstance(handler, TaskHandler):
            raise TypeError(f"{task_type} handler does not implement protocol")
        self.handlers[task_type] = handler

    async def _worker(self, worker_id: int):
        logger.info(f"Worker {worker_id} started")
        while self._running:
            try:
                task = await self.queue.get()
                task_type = getattr(task, 'task_type', 'default') 
                handler = self.handlers.get(task_type)

                if handler:
                    await handler.handle(task)
                    self.history.append(task) 
                    logger.info(f"Worker {worker_id} finished task {task.id}")
                else:
                    logger.warning(f"No handler for type: {task_type}")
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}", exc_info=True)
    
    async def start(self):
        self._running = True
        self._workers = [
            asyncio.create_task(self._worker(i)) 
            for i in range(self.max_workers)
        ]

    async def stop(self):
        self._running = False
        for w in self._workers:
            w.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)
        logger.info("All workers stopped")

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
