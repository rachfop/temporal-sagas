# Sagas

Sagas are a protocol for implementing long-running processes. The Saga protocol ensures that a process is atomic, that is, a process executes observably equivalent to completely or not at all.

## Overview

The booking saga workflow is responsible for coordinating the booking of a vacation package, consisting of a car, hotel, and flight reservation. In the event of a failure at any point during the booking process, the workflow will trigger compensating actions to undo any previous bookings.

![](static/booking-saga.png)

## Running

Prerequisites:

- Python >= 3.7
- [Poetry](https://python-poetry.org)
- [Local Temporal server running](https://docs.temporal.io/application-development/foundations#run-a-development-cluster)

With this repository cloned, run the following at the root of the directory:

```bash
poetry install
```
That loads all required dependencies. 

Then run the worker and workflow.

```bash
poetry run python run_worker.py
poetry run python run_workflow.py
```

![](static/webui_success.png)
![](static/success.gif)

![](stat/../static/webui_failure.png)
![](static/failure.gif)

## Design

The booking saga is implemented using the Temporal Workflow framework, which provides a robust and fault-tolerant platform for coordinating distributed transactions.

The saga workflow consists of three activities: `book_car()`, `book_hotel)()`, and `book_flight)()`, each of which is responsible for making a reservation with the corresponding service provider. If any of these activities fail, the workflow will trigger the corresponding compensating action (`undo_book_car()`, `undo_book_hotel()`, or `undo_book_flight()`) to undo any previous bookings.

The `non_retryable_error_types` parameter is used to specify a list of error types that should not be retried when a Workflow or Activity fails.