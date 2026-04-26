from src.source import RandomSource, TaskGiver
from src.constants import COMMANDS, STATUS_LIST
from src.queue import TaskQueue
from src.exceptions import StatusError


async def main() -> None:
    print(f"Available commands:\n- {"\n- ".join(COMMANDS)}")
    task_queue = TaskQueue()
    while inp := input():
        if inp not in COMMANDS:
            continue
        match inp:
            case "add-task":
                task_rnd = RandomSource(1)
                if isinstance(task_rnd, TaskGiver):
                    new_task = await task_rnd.get_tasks() 
                    task_queue.add_task(new_task)
                    print("Initiated task with generator")

            case "show-tasks":
                if not task_queue:
                    print("No active tasks")
                else:
                    for task in task_queue:
                        print(f"{task.id}: {task.description}. Priority: {task.priority}, Status: {task.status}")

            case "change-task-status":
                id = str(input("Enter the task id: "))
                task = task_queue.find(id)
                if task:
                    task.status = str(input("Enter new status: "))
                    print("Status updated")
                else:
                    raise ValueError("No such task")

            case "available-statuses":
                print(", ".join(STATUS_LIST))

            case "find-task":
                id = str(input("Enter the id: "))
                task = task_queue.find(id)
                if task:
                    print(f"{task.id}: {task.description}. Priority: {task.priority}, Status: {task.status}")
                else:
                    print("Task was not found")

            case "filter-by-priority":
                prio_filter = input("Enter the priority: ")
                try:
                    prio_filter = int(prio_filter)
                except ValueError:
                    raise ValueError(f"Priority must be integer: \"{prio_filter}\"")
                for task in task_queue.filter_by_priority(prio_filter):
                    print(f"{task.id}: {task.description}. Priority: {task.priority}, Status: {task.status}")

            case "filter-by-status":
                filter_status = str(input("Enter the status: "))
                if filter_status not in STATUS_LIST:
                    raise StatusError(filter_status)
                for task in task_queue.filter_by_status(filter_status):
                    print(f"{task.id}: {task.description}. Priority: {task.priority}, Status: {task.status}")

            case "exit":
                return


if __name__ == "__main__":
    await main()
