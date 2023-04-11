import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from activities import (
    book_car,
    book_hotel,
    book_flight,
    undo_book_car,
    undo_book_hotel,
    undo_book_flight,
)
from book_workflow import BookWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="saga-task-queue",
        workflows=[BookWorkflow],
        activities=[
            book_car,
            book_hotel,
            book_flight,
            undo_book_car,
            undo_book_hotel,
            undo_book_flight,
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
