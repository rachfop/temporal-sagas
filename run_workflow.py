from temporalio.client import Client

# Import the workflow from the previous code
from book_workflow import BookWorkflow
from activities import BookVacationInput
from flask import Flask, request, render_template
import uuid

app = Flask(__name__)


@app.route("/")
async def display_form():
    return render_template("book_vacation.html")


@app.route("/book", methods=["POST"])
async def book_vacation():
    user_id = f'{request.form.get("name")}-{str(uuid.uuid4( ))}'
    car = request.form.get("car")
    hotel = request.form.get("hotel")
    flight = request.form.get("flight")

    input = BookVacationInput(
        book_user_id=user_id,
        book_car_id=car,
        book_hotel_id=hotel,
        book_flight_id=flight,
    )

    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        BookWorkflow.run,
        input,
        id=user_id,
        task_queue="saga-task-queue",
    )
    if result == "Voyage cancelled":
        return render_template("book_vacation.html", cancelled=True)

    else:
        print(result)
        result_list = result.split("Booked ")
        car = result_list[1].split(" Booking ")[0].title()
        hotel = result_list[2].split(" Booking ")[0].title()
        flight = result_list[2].split(" Booking ")[1].title()
        print(user_id)
        return render_template(
            "book_vacation.html",
            result=result,
            cancelled=False,
            car=car,
            hotel=hotel,
            flight=flight,
            user_id=user_id,
        )


if __name__ == "__main__":
    app.run(debug=True)
