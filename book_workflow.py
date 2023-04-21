from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import BookVacationInput, book_car, book_flight, book_hotel

ATTEMPTS_FLIGHT = 5


@workflow.defn
class BookWorkflow:
    @workflow.run
    async def run(self, input: BookVacationInput):
        compensations = []

        try:
            compensations.append("undo_book_car")
            output = await workflow.execute_activity(
                book_car,
                input,
                start_to_close_timeout=timedelta(seconds=10),
                task_queue="saga-task-queue",
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(seconds=1),
                    maximum_attempts=3,
                    non_retryable_error_types=["Exception"],
                ),
            )
            compensations.append("undo_book_hotel")
            output += " " + await workflow.execute_activity(
                book_hotel,
                input,
                start_to_close_timeout=timedelta(seconds=10),
                task_queue="saga-task-queue",
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(seconds=1),
                    maximum_attempts=3,
                    non_retryable_error_types=["Exception"],
                ),
            )

            compensations.append("undo_book_flight")
            output += " " + await workflow.execute_activity(
                book_flight,
                input,
                start_to_close_timeout=timedelta(seconds=10),
                task_queue="saga-task-queue",
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(seconds=1),
                    maximum_attempts=ATTEMPTS_FLIGHT,
                    non_retryable_error_types=["Exception"],
                ),
            )
            return output
        except Exception:
            for compensation in reversed(compensations):
                await workflow.execute_activity(
                    compensation,
                    input,
                    task_queue="saga-task-queue",
                    start_to_close_timeout=timedelta(seconds=10),
                )

            return "Voyage cancelled"
