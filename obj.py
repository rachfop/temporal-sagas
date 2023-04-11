from dataclasses import dataclass


@dataclass
class BookVacationInput:
    book_car_id: str
    book_hotel_id: str
    book_flight_id: str
