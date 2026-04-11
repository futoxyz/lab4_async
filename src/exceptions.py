from typing import Any


class IntegerError(Exception):
    def __init__(self, name: Any, type: int = -1):
        match type:
            case 0:
                super().__init__(f"{name} is not an integer!")
            case 1:
                super().__init__(f"{name} can't be negative!")
            case _:
                super().__init__(f"Undefined type given: {name}")


class StringError(Exception):
    def __init__(self, name: Any, type: int = -1):
        match type:
            case 0:
                super().__init__(f"{name} is not a string!")
            case 1:
                super().__init__(f"{name} can't be an empty line!")
            case _:
                super().__init__(f"Undefined type given: {name}")


class StatusError(Exception):
    def __init__(self, value: Any):
            super().__init__(f"\"{value}\" can't be used as a status!")


class TaskError(Exception):
    def __init__(self, value: Any, type: int = -1):
        match type:
            case 0:
                super().__init__(f"No such task in queue -> {value}")
            case 1:
                super().__init__(f"Task id must be unique: task with similar id already exists -> {value}")
            case _:
                super().__init__(f"Undefined type given: {value}")
