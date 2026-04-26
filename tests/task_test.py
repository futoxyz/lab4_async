from pytest import raises, mark
from time import sleep
from src.task import Task
from src.exceptions import IntegerError, StringError, StatusError


def test_tasks() -> None:
    '''
    Тесты дескрипторов.
    '''
    normal_task = Task("id_1", "description", "default_type", 1)
    assert normal_task.status == "pending"
    with raises(StatusError):
        normal_task.status = "can't be a status"
    with raises(StatusError):
        normal_task.status = 1010101
    normal_task.status = "in_progress"
    assert normal_task.status == "in_progress"

    with raises(IntegerError):
        normal_task.priority = -1
    with raises(IntegerError):
        normal_task.priority = "string"


@mark.parametrize("bad_id", ["", 0, None, 123, -123])
def test_id(bad_id):
    '''
    Отдельные тесты вводов.
    '''
    with raises(StringError):
        Task(id=bad_id, description="valid", task_type="default_type")


@mark.parametrize("bad_desc", ["", 0, None, 123, -123])
def test_desc(bad_desc):
    with raises(StringError):
        Task(id="valid", description=bad_desc, task_type="default_type")


@mark.parametrize("bad_type", ["", 0, None, 123, -123])
def test_type(bad_type):
    with raises(StringError):
        Task(id="valid", description="valid", task_type=bad_type)


@mark.parametrize("bad_priority", ["", -1, None, "priority_1"])
def test_priority(bad_priority):
    with raises(IntegerError):
        Task(id="valid", description="valid", task_type="default_type", priority=bad_priority)


def test_age_measurement() -> None:
    task = Task("id", "description", "default_type")
    time_exist: float = 0.75
    sleep(time_exist)
    assert abs(task.age_seconds - time_exist) < 0.1 # Погрешность
