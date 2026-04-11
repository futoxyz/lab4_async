import src.source as src
import src.task as task_ref
from pytest import raises
from random import randint, seed


def test_generator_api() -> None:
    seed() # Сид генерации
    first = randint(10, 1000)
    second = randint(10, 1000)

    source_gen = src.RandomSource(first)
    tasks_gen = source_gen.get_tasks()

    source_api = src.APISource(second)
    tasks_api = source_api.get_tasks()

    assert isinstance(source_gen, src.TaskGiver)
    assert isinstance(source_api, src.TaskGiver)

    for task in tasks_gen:
        assert isinstance(task, task_ref.Task)
    for task in tasks_api:
        assert isinstance(task, task_ref.Task)

    assert len(tasks_gen) == first
    assert len(tasks_api) == second


def test_file() -> None:
    '''
    Файл 'tasks.txt' заведомо имеет верный формат.
    '''
    with raises(ValueError):
        source = src.FileSource("src/main.py")
        source.get_tasks()

    source = src.FileSource("tests/tasks.txt")

    tasks = source.get_tasks()
    assert isinstance(source, src.TaskGiver)
    for task in tasks:
        assert isinstance(task, task_ref.Task)
