import asyncio
from dataclasses import dataclass

from temporalio import activity


@dataclass
class BookVacationInput:
    book_user_id: str
    book_car_id: str
    book_hotel_id: str
    book_flight_id: str
    attempts: int


@activity.defn
async def book_car(input: BookVacationInput) -> str:
    await asyncio.sleep(3)
    if activity.info().attempt < input.attempts:
        activity.heartbeat(
            f"Invoking activity, attempt number {activity.info().attempt}"
        )
        await asyncio.sleep(3)
        raise RuntimeError("Car service is down")
    
    if "invalid" in input.book_car_id:
        raise Exception("Invalid car booking, rolling back!")

    print(f"Booking car: {input.book_car_id}")
    return f"Booked car: {input.book_car_id}"


@activity.defn
async def book_hotel(input: BookVacationInput) -> str:
    await asyncio.sleep(3)
    if activity.info().attempt < input.attempts:
        activity.heartbeat(
            f"Invoking activity, attempt number {activity.info().attempt}"
        )
        await asyncio.sleep(3)
        raise RuntimeError("Hotel service is down")
    
    if "invalid" in input.book_hotel_id:
        raise Exception("Invalid hotel booking, rolling back!")

    print(f"Booking hotel: {input.book_hotel_id}")
    return f"Booked hotel: {input.book_hotel_id}"


@activity.defn
async def book_flight(input: BookVacationInput) -> str:
    await asyncio.sleep(3)
    if activity.info().attempt < input.attempts:
        activity.heartbeat(
            f"Invoking activity, attempt number {activity.info().attempt}"
        )
        await asyncio.sleep(3)
        raise RuntimeError("Flight service is down")
    
    if "invalid" in input.book_flight_id:
        raise Exception("Invalid flight booking, rolling back!")

    print(f"Booking flight: {input.book_flight_id}")
    return f"Booking flight: {input.book_flight_id}"


@activity.defn
async def undo_book_car(input: BookVacationInput) -> str:
    print(f"Undoing booking of car: {input.book_car_id}")
    return f"Undoing booking of car: {input.book_car_id}"


@activity.defn
async def undo_book_hotel(input: BookVacationInput) -> str:
    print(f"Undoing booking of hotel: {input.book_hotel_id}")
    return f"Undoing booking of hotel: {input.book_hotel_id}"


@activity.defn
async def undo_book_flight(input: BookVacationInput) -> str:
    print(f"Undoing booking of flight: {input.book_flight_id}")
    return f"Undoing booking of flight: {input.book_flight_id}"
