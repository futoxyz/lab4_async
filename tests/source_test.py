import src.source as src
import src.task as task_ref
from pytest import raises, mark
from random import randint, seed


@mark.asyncio
async def test_generator_api() -> None:
    seed() # Сид генерации
    first = randint(10, 1000)
    second = randint(10, 1000)

    source_gen = src.RandomSource(first)
    tasks_gen = await source_gen.get_tasks()

    source_api = src.APISource(second)
    tasks_api = await source_api.get_tasks()

    assert isinstance(source_gen, src.TaskGiver)
    assert isinstance(source_api, src.TaskGiver)

    for task in tasks_gen:
        assert isinstance(task, task_ref.Task)
        assert task.task_type == 'gen'
    for task in tasks_api:
        assert isinstance(task, task_ref.Task)
        assert task.task_type == 'api'

    assert len(tasks_gen) == first
    assert len(tasks_api) == second


@mark.asyncio
async def test_file() -> None:
    '''
    Файл 'tasks.txt' заведомо имеет верный формат.
    '''
    with raises(ValueError):
        source = src.FileSource("src/main.py")
        await source.get_tasks()

    source = src.FileSource("tests/tasks.txt")

    tasks = await source.get_tasks()
    assert isinstance(source, src.TaskGiver)
    for task in tasks:
        assert isinstance(task, task_ref.Task)
