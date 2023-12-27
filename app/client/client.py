import re
from datetime import timezone, datetime
from typing import Optional

import pytz
from flask import Blueprint, render_template, request, redirect
from sqlalchemy import distinct

from app.class_type.models import Class
from app.hotel.models import Hotel
from .models import Client, Booking
from app.database import db

TIMEZONE = pytz.timezone("Europe/Istanbul")

client_bp = Blueprint("client", __name__)


@client_bp.route("/", methods=["GET"])
def clients():
    all_records_client = db.session.query(Client).order_by(Client.id).all()
    return render_template("client/clients.html", clients=all_records_client)


def validate_user(name: str, surname: str, job: str, telephone: str) -> list:
    """ validation of user data: name, surname, job and telephone """

    errors = []
    if not name:
        errors.append("Name can not be empty!")
    if not surname:
        errors.append("Surname can not be empty!")
    if name and surname and (name.isdigit() or surname.isdigit()):
        errors.append("Name and surname must contain only latin letter!")
    if job and job.isdigit():
        errors.append("Job must contain only latin letter!")
    if not re.fullmatch(r"[1-9]-\d{3}-\d{3}-\d{4}", telephone):
        errors.append("Telephone format must be _-___-___-____ !")
    return errors


def validate_date(check_in: datetime, check_out: datetime) -> Optional[str]:
    """ validate date: check in must be earlier than check out"""

    if check_in > check_out:
        return "Check in data must be earlier than check out data"
    return None


@client_bp.route("/create", methods=["GET", "POST"])
def create_client():
    """ creation new client with booking"""
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

        class_id = (
            db.session.query(Class.id)
            .filter((Class.hotel_name == hotel) & (Class.name == class_name))
            .first()[0]
        )

        checkin_day = request.form["checkin_day"]
        checkin_month = request.form["checkin_month"]
        checkin_year = request.form["checkin_year"]

        check_in = TIMEZONE.localize(
            datetime(int(checkin_year), int(checkin_month), int(checkin_day), 14)
        )

        checkout_day = request.form["checkout_day"]
        checkout_month = request.form["checkout_month"]
        checkout_year = request.form["checkout_year"]

        check_out = TIMEZONE.localize(
            datetime(int(checkout_year), int(checkout_month), int(checkout_day), 14)
        )

        if validate_date(check_in, check_out):
            errors.append(validate_date(check_in, check_out))

        booking_id = db.session.query(Booking.id).order_by(Booking.id.desc()).first()[0]

        insert_data_client["booking_id"] = booking_id + 1

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
                "client/client_form.html",
                errors=errors,
                client=Client(**insert_data_client),
                classes=class_names,
                hotels=hotel_names,
                booking=Booking(**insert_data_booking),
                update_client=None,
                update_booking=None,
                class_type=None
            )
        db.session.commit()

        return redirect("/client")

    return render_template(
        "client/client_form.html",
        client=None,
        booking=None,
        classes=class_names,
        hotels=hotel_names,
        update_client=None,
        update_booking=None,
        class_type=None
    )


@client_bp.route("/<int:client_id>", methods=["GET", "POST", "DELETE"])
def get_client(client_id: int):
    """ get certain client info and update it or redirect to delete"""

    uniq_client = db.session.query(Client).filter(Client.id == client_id).first()

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

        try:
            db.session.query(Client).filter_by(id=client_id).update(values=insert_data_client)
        except Exception as err:
            errors.append(str(err))
            db.session.rollback()

        if errors:
            return render_template("client/client_form.html", client=uniq_client, update_client=True, errors=errors)

        db.session.commit()

        return redirect("/client")

    return render_template("client/client_form.html", client=uniq_client, update_client=True)


@client_bp.route("<int:client_id>/delete", methods=["POST"])
def delete_client(client_id: int):
    """ delete client and booking """

    errors = []
    try:
        db.session.query(Client).filter_by(id=client_id).delete()
    except Exception as err:
        uniq_client = db.session.query(Client).filter(Client.id == client_id).first()
        errors.append(str(err))
        return render_template("client/client_form.html", client=uniq_client, errors=errors, update_client=True)
    db.session.commit()
    return redirect("/client")


@client_bp.route("/booking/<int:booking_id>", methods=["GET", "POST", "DELETE"])
def get_booking(booking_id: int):
    """ get certain booking info and update it"""
    class_names = db.session.query(distinct(Class.name)).all()
    hotel_names = db.session.query(Hotel.name).all()
    uniq_booking = db.session.query(Booking).filter(Booking.id == booking_id).first()

    class_type = db.session.query(Class).filter(Class.id == uniq_booking.class_id).first()

    if request.method == "POST":

        errors = []
        checkin_day = request.form["checkin_day"]
        checkin_month = request.form["checkin_month"]
        checkin_year = request.form["checkin_year"]

        check_in = TIMEZONE.localize(
            datetime(int(checkin_year), int(checkin_month), int(checkin_day), 14)
        )

        checkout_day = request.form["checkout_day"]
        checkout_month = request.form["checkout_month"]
        checkout_year = request.form["checkout_year"]

        check_out = TIMEZONE.localize(
            datetime(int(checkout_year), int(checkout_month), int(checkout_day), 14)
        )

        errors.append(validate_date(check_in, check_out))

        hotel = request.form["hotel"]
        class_name = request.form["class_name"]
        room = request.form["room"]

        class_id = (
            db.session.query(Class.id)
            .filter((Class.hotel_name == hotel) & (Class.name == class_name))
            .first()[0]
        )

        update_data_booking = {
            "room_number": room,
            "class_id": class_id,
            "check_in": check_in,
            "check_out": check_out,
        }

        try:
            db.session.query(Booking).filter_by(id=booking_id).update(values=update_data_booking)
        except Exception as err:
            errors.append(str(err))
            return render_template(client=None, update_booking=True, classes=class_names, hotels=hotel_names, errors=errors)
        db.session.commit()

        return redirect("/client")

    return render_template(
        "client/client_form.html",
        client=None,
        classes=class_names,
        hotels=hotel_names,
        booking=uniq_booking,
        update_client=None,
        update_booking=True,
        class_type=class_type
    )
