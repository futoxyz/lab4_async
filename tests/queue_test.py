from pytest import raises, mark
from random import randint, choice, seed
from src.task import Task
from src.queue import TaskQueue
from src.exceptions import TaskError
from src.source import RandomSource


@mark.asyncio
async def test_task_queue():
    seed() # Сид генерации
    amount = randint(10,500)
    source = RandomSource(amount)
    tasks = await source.get_tasks()

    collection = TaskQueue()
    for task in tasks:
        collection.add_task(task)

    i = 0
    for task in collection:
        assert task == tasks[i]
        i += 1
    assert amount == i
    collection.delete(choice(list(collection._tasks.values())))
    assert len(list(collection)) == amount - 1

    non_existing_task = Task("task_-1", "description", 1)
    with raises(TaskError):
        collection.delete(non_existing_task)

    assert collection.find(non_existing_task) is None
    some_task = choice(list(collection._tasks.values()))
    assert collection.find(some_task.id) == some_task
    with raises(TaskError):
        collection.add_task(some_task)
