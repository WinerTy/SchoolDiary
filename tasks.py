from celery import shared_task


@shared_task()
def debug_task():
    print("asdasdsad")
    return "1234"
