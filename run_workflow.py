import asyncio
from temporalio.client import Client

# Import the workflow from the previous code
from book_workflow import BookWorkflow
from obj import BookVacationInput


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233")

    input = BookVacationInput(
        book_car_id="Toyota Camry",
        book_hotel_id="Hilton",
        book_flight_id="Alaska Airlines",
    )
    result = await client.execute_workflow(
        BookWorkflow.run,
        input,
        id="saga",
        task_queue="saga-task-queue",
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
