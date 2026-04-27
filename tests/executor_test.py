import asyncio
from pytest import mark, raises
from src.task import Task
from src.queue import TaskQueue
from src.executor import TaskExecutor
from src.handlers import APIHandler, FileHandler, GeneratorHandler

@mark.asyncio
async def test_handler_registration():
    queue = TaskQueue()
    executor = TaskExecutor(queue)
    executor.register_handler("api", APIHandler())
    assert "api" in executor.handlers
    with raises(TypeError):
        executor.register_handler("bad", "not_handler")

@mark.asyncio
async def test_executor():
    queue = TaskQueue()
    executor = TaskExecutor(queue, max_workers=2)
    executor.register_handler("gen", GeneratorHandler())
    normal_task = Task(id="task_1", description="test", task_type="gen")
    for_fail = Task(id="task_2", description="must fail", task_type="gen")
    await queue.add(normal_task)
    await queue.add(for_fail)

    async with executor:
        await asyncio.sleep(3.1)

    assert normal_task.status == "completed"
    assert for_fail.status == "failed"

@mark.asyncio
async def test_multiple_handlers():
    queue = TaskQueue()
    executor = TaskExecutor(queue, max_workers=3)
    executor.register_handler("api", APIHandler())
    executor.register_handler("file", FileHandler())
    t1 = Task("t1", "desc", task_type="api")
    t2 = Task("t2", "desc", task_type="file")

    await queue.add(t1)
    await queue.add(t2)

    async with executor:
        await asyncio.sleep(3.1)

    assert t1.status == "completed"
    assert t2.status == "completed"

@mark.asyncio
async def test_bad_task_type():
    queue = TaskQueue()
    executor = TaskExecutor(queue, max_workers=1)
    task = Task("t_unknown", "desc", task_type="wrong")
    await queue.add(task)

    async with executor:
        await asyncio.sleep(3.1)

    assert task.status == "pending"
