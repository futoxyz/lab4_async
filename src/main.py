from src.source import RandomSource
from src.constants import COMMANDS, STATUS_LIST
from src.queue import TaskQueue
from src.executor import TaskExecutor
from src.handlers import GeneratorHandler
from src.exceptions import StatusError, TaskError, IntegerError
import asyncio
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


def task_table(tasks, title):
    table = Table(title=title, show_header=True, header_style="bold")
    table.add_column("ID", justify="center")
    table.add_column("Description", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Priority", justify="center")

    for t in tasks:
        match t.status:
            case "pending":
                status_color = "yellow"
            case "completed":
                status_color = "green"
            case "failed":
                status_color = "red"
            case "in_progress":
                status_color = "cyan"

        table.add_row(
            t.id,
            t.description,
            f"[{status_color}]{t.status}[/{status_color}]",
            str(t.priority)
        )
    return table

async def main():
    task_queue = TaskQueue()
    executor = TaskExecutor(task_queue, max_workers=3)
    executor.register_handler("default", GeneratorHandler())

    console.print(Panel.fit(
        f"Available commands: [bold]{', '.join(COMMANDS)}[/bold]",
        title="Task manager"
    ))

    while True:
        inp = await asyncio.to_thread(input, "> ")
        if not inp:
            continue
        if inp == "exit":
            if executor._running:
                await executor.stop()
            break

        match inp:
            case "add-task":
                source = RandomSource(amount=1)
                new_task = await source.get_tasks()
                new_task = new_task[0]
                new_task.task_type = "gen"
                await task_queue.add(new_task)
                console.print(f"[green]✔[/green] Task {new_task.id} added to queue.")

            case "add-many-tasks":
                source = RandomSource(amount=25)
                new_task = await source.get_tasks()
                for t in new_task:
                    t.task_type = "gen"
                    await task_queue.add(t)
                    console.print(f"[green]✔[/green] Task {t.id} added to queue.")

            case "executor":
                if not executor._running:
                    await executor.start()
                    console.print("[bold green]Executor started[/bold green]")
                else:
                    console.print("[bold yellow]Executor is already running[/bold yellow]")

            case "show-tasks":
                console.print(task_table(list(task_queue), "Task queue"))
                console.print(task_table(executor.history, "Finished tasks"))

            case "change-task-status":
                tid = await asyncio.to_thread(input, "Task ID: ")
                task = next((t for t in task_queue if t.id == tid), None)
                if not task:
                    raise TaskError(tid, 0)
                new_status = await asyncio.to_thread(input, f"New Status ({', '.join(STATUS_LIST)}): ")
                task.status = new_status
                console.print(f"[green]✔[/green] Status updated to {new_status}")

            case "available-statuses":
                console.print(f"Available: [bold]{', '.join(STATUS_LIST)}[/bold]")

            case "find-task":
                tid = await asyncio.to_thread(input, "Enter ID: ")
                task = next((t for t in list(task_queue) + executor.history if t.id == tid), None)
                if task:
                    console.print(Panel(f"ID: {task.id}\nDesc: {task.description}\nStatus: {task.status}\nPriority: {task.priority}", title=task.id))
                else:
                    console.print("[red]✘[/red] Task was not found.")

            case "filter-by-priority":
                p = await asyncio.to_thread(input, "Enter priority: ")
                if not p.isdigit():
                    raise IntegerError(p, 0)
                results = list(task_queue.filter_by_priority(int(p)))
                for t in executor.history:
                    if t.priority == p:
                        results.append(t)
                console.print(task_table(results, f"Priority: {p}"))

            case "filter-by-status":
                s = await asyncio.to_thread(input, "Enter status: ")
                if s not in STATUS_LIST:
                    raise StatusError(s)
                results = list((task_queue).filter_by_status(s))
                for t in executor.history:
                    if t.status == s:
                        results.append(t)
                console.print(task_table(results, f"Status: {s}"))


if __name__ == "__main__":
    console = Console()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
