from celery.result import AsyncResult

from celery_app import ParseLinksTask


def check_tasks_set(tasks: list) -> bool:
    return all(AsyncResult(task).ready() for task in tasks)


def print_ready_tasks_set(tasks: list) -> None:
    for task in tasks:
        print(AsyncResult(task).result)


def main():
    tasks_to_run = [ParseLinksTask().delay(i) for i in range(1, 3)]
    while tasks_to_run:
        ready_tasks = [task for task in tasks_to_run if task.ready()]
        for task in ready_tasks:
            if check_tasks_set(task.result):
                print_ready_tasks_set(task.result)
                tasks_to_run.remove(task)


if __name__ == '__main__':
    main()
