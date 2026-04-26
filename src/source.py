from src.task import Task
from src.constants import DESCRIPTIONS
from typing import runtime_checkable, Protocol
from os import path
import logging
import random
from asyncio import to_thread
logger = logging.getLogger(__name__)
logging.basicConfig(filename='srcs.log', level=logging.INFO)


@runtime_checkable
class TaskGiver(Protocol):
    async def get_tasks(self) -> list[Task] | Task:
        ...


class APISource:
    def __init__(self, amount: int = 5):
        self.amount = amount

    async def get_tasks(self) -> list[Task] | Task:
        tasks = []
        ids = random.sample(range(1000), self.amount+1)
        for i in range(1, self.amount + 1):
            current_task = Task(
                id=f"task_{ids[i]}",
                description=random.choice(DESCRIPTIONS),
                priority=random.randint(0, 10)
            )
            tasks.append(current_task)
            logger.info(f"Initiated {current_task.id} with API, description \"{current_task.description}\' and priority {current_task.priority}")
        if self.amount == 1:
            return tasks[0]
        return tasks


class FileSource:
    def __init__(self, file_dir: str):
        if not path.isfile(file_dir):
            logger.info(f"Failed to open {file_dir}")
            raise ValueError("File was not found")
        self.file = path.abspath(file_dir)

    async def get_tasks(self) -> list[Task]:
        return await to_thread(self.read_file) 

    def read_file(self) -> list[Task]:
        '''
        Пример приема данных: Каждая строка - отдельная задача, первое слово - айди, далее описание.
        '''
        tasks = []
        try:
            with open(self.file, encoding="utf-8") as f:
                i=0
                for line in f:
                    id, description = line.split(maxsplit=1)
                    current_task = Task(
                        id=id,
                        description=description,
                        priority=i
                    )
                    tasks.append(current_task)
                    logger.info(f"Initiated {current_task.id} from file located in \"{self.file}\"")
                    i += 1

        except PermissionError as e:
            logger.info(f"Failed to read {self.file}: {e}")
            raise ValueError("Failed to read file due to permission")

        except UnicodeDecodeError:
            logger.info(f"Failed to read {self.file}: {line}")
            raise ValueError("Failed to decode file")

        except ValueError as e:
            logger.info(f"File does not contain correct info: {line}")
            raise ValueError(f"Bad line: {e}")
        return tasks


class RandomSource:
    def __init__(self, amount: int = 5):
        self.amount = amount

    async def get_tasks(self) -> list[Task] | Task:
        tasks = []
        ids = random.sample(range(1000), self.amount+1)
        for i in range(1, self.amount + 1):
            current_task = Task(
                id=f"task_{ids[i]}",
                description=random.choice(DESCRIPTIONS),
                priority=random.randint(0, 10)
            )
            tasks.append(current_task)
            logger.info(f"Initiated {current_task.id} with generator, description \"{current_task.description}\' and priority {current_task.priority}")
        if self.amount == 1:
            return tasks[0]
        return tasks
