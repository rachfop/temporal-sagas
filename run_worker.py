import asyncio
from typing import Optional
import os

from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker

from activities import (
    book_car,
    book_flight,
    book_hotel,
    undo_book_car,
    undo_book_flight,
    undo_book_hotel,
)
from book_workflow import BookWorkflow


async def main():

    if os.getenv('TEMPORAL_MTLS_TLS_CERT') and os.getenv('TEMPORAL_MTLS_TLS_KEY') is not None:
        server_root_ca_cert: Optional[bytes] = None
        f = open(os.getenv('TEMPORAL_MTLS_TLS_CERT'), "rb")
        client_cert = f.read()

        f = open(os.getenv('TEMPORAL_MTLS_TLS_KEY'), "rb")
        client_key = f.read()

        # Start client
        client = await Client.connect(
            os.getenv('TEMPORAL_HOST_URL'),
            namespace=os.getenv('TEMPORAL_NAMESPACE'),
            tls=TLSConfig(
                server_root_ca_cert=server_root_ca_cert,
                client_cert=client_cert,
                client_private_key=client_key,
            ),
        )
    else:
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
