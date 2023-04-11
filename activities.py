from temporalio import activity
from obj import BookVacationInput

import random


@activity.defn
async def book_car(input: BookVacationInput) -> str:
    print(f"Booking car: {input.book_car_id}")
    return f"Booked car: {input.book_car_id}"


@activity.defn
async def book_hotel(input: BookVacationInput) -> str:
    print(f"Booking hotel: {input.book_hotel_id}")
    return f"Booked hotel: {input.book_hotel_id}"


@activity.defn
async def book_flight(input: BookVacationInput) -> str:
    seats_available = random.randint(0, 10)
    try:
        if seats_available < 1:
            raise Exception("No seats remaining")
        else:
            print(f"Booking flight: {input.book_flight_id}")
    except Exception:
        raise Exception("No seats remaining")


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
