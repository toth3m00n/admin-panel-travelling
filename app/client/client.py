import re
from datetime import timezone, datetime
import pytz
from flask import Blueprint, render_template, request, redirect
from sqlalchemy import distinct

from app.class_type.models import Class
from app.hotel.models import Hotel
from .models import Client, Booking
from app.database import db

client_bp = Blueprint("client", __name__)


@client_bp.route("/", methods=["GET"])
def clients():
    all_records_client = db.session.query(Client).all()
    return render_template("client/clients.html", clients=all_records_client)


def validate_user(name, surname, job, telephone):
    errors = []
    if not name:
        errors.append("Name can not be empty!")
    if not surname:
        errors.append("Surname can not be empty!")
    if name and surname and (not name.isalpha() or not surname.isalpha()):
        errors.append("Name and surname must contain only latin letter!")
    if job and not job.isalpha():
        errors.append("Job must contain only latin letter!")
    if not re.fullmatch(r"[1-9]-\d{3}-\d{3}-\d{4}", telephone):
        errors.append("Telephone format must be _-___-___-____ !")
    return errors


def validate_date(check_in, check_out):
    if check_in > check_out:
        return "Check in data must be earlier than check out data"
    return None


@client_bp.route("/create", methods=["GET", "POST"])
def create_client():

    timezone = pytz.timezone("Europe/Istanbul")
    class_names = db.session.query(distinct(Class.name)).all()
    hotel_names = db.session.query(Hotel.name).all()

    if request.method == "POST":

        insert_data_client = {
            "name": request.form["name"],
            "surname": request.form["surname"],
            "sex": "male" if request.form["gender"] == "male" else "female",
            "age": request.form["age"],
            "telephone": request.form["telephone"],
            "job": request.form["job"],
        }

        errors = validate_user(
            insert_data_client["name"],
            insert_data_client["surname"],
            insert_data_client["job"],
            insert_data_client["telephone"],
        )

        hotel = request.form["hotel"]
        class_name = request.form["class_name"]
        room = request.form["room"]

        class_id = db.session.query(Class.id).filter(
            (Class.hotel_name == hotel) & (Class.name == class_name)
        ).first()[0]

        checkin_day = request.form["checkin_day"]
        checkin_month = request.form["checkin_month"]
        checkin_year = request.form["checkin_year"]

        check_in = timezone.localize(
            datetime(int(checkin_year), int(checkin_month), int(checkin_day), 14)
        )

        checkout_day = request.form["checkout_day"]
        checkout_month = request.form["checkout_month"]
        checkout_year = request.form["checkout_year"]

        check_out = timezone.localize(
            datetime(int(checkout_year), int(checkout_month), int(checkout_day), 14)
        )

        if validate_date(check_in, check_out):
            errors.append(validate_date(check_in, check_out))

        booking_id = db.session.query(Booking.id).order_by(Booking.id.desc()).first()[0]

        print(class_id, booking_id)

        insert_data_client['booking_id'] = booking_id + 1

        insert_data_booking = {
            "room_number": room,
            "class_id": class_id,
            "check_in": check_in,
            "check_out": check_out,
        }

        try:
            db.session.add(Booking(**insert_data_booking))
            db.session.add(Client(**insert_data_client))
        except Exception as err:
            errors.append(str(err))

        if errors:
            return render_template(
                "client/client_form.html", errors=errors, client=None, classes=class_names,
                hotels=hotel_names
            )
        db.session.commit()

        return redirect("/client")

    return render_template(
        "client/client_form.html", client=None, classes=class_names, hotels=hotel_names
    )
