from pytest import mark
from random import randint, seed
from src.queue import TaskQueue
from src.source import RandomSource

@mark.asyncio
async def test_task_queue():
    seed() # Сид генерации
    amount = randint(10, 100)
    source = RandomSource(amount)
    tasks = await source.get_tasks()

    collection = TaskQueue()
    for task in tasks:
        task.task_type = "default"
        await collection.add(task)
    i = 0
    for task in collection:
        assert task == tasks[i]
        i += 1
    assert amount == i
    if tasks:
        target_prio = tasks[0].priority
        filtered = list(collection.filter_by_priority(target_prio))
        assert len(filtered) > 0
        assert all(t.priority == target_prio for t in filtered)
    first_task = await collection.get()
    assert first_task == tasks[0]
    assert len(list(collection)) == amount - 1
