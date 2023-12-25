from flask import Blueprint, render_template, request, redirect
from sqlalchemy import distinct

from app.class_type.models import Class
from app.database import db

from .models import Hotel

hotel_bp = Blueprint("hotel", __name__)


@hotel_bp.route("/", methods=["GET"])
def hotels():
    all_records_hotel = db.session.query(Hotel).all()
    return render_template("hotel/hotels.html", hotels=all_records_hotel)


def validate_hotel(name: str, count_stars: int, class_names, errors):

    if not name.isdigit():
        errors.append("Hotel name must consist only latinic letter!")
    for class_name in class_names:
        if name == class_name[0]:
            errors.append(
                "Hotel with this name already exist. Please enter unique name"
            )
            break
    if count_stars > 5 or count_stars < 1:
        errors.append("Amount of stars must be beetwen 1.0 and 5.0")


@hotel_bp.route("/create", methods=["GET", "POST"])
def create_hotel():
    class_names = db.session.query(distinct(Class.name)).all()
    if request.method == "POST":

        errors = []

        # for hotel
        form_values = {}

        # считывает все формы в словарь, а потом его распаковыввает
        for class_name in request.form:
            form_values[class_name] = request.form[class_name]

        validate_hotel(
            form_values["hotel_name"],
            int(form_values["count_stars"]),
            class_names,
            errors,
        )

        insert_data_hotel = {
            "hotel_name": form_values["hotel_name"],
            "count_stars": form_values["count_stars"],
        }

        print(form_values)

        try:
            db.session.add(Hotel(**insert_data_hotel))
            for class_type in class_names:
                class_name = class_type[0]
                db.session.query.add(Class(
                    hotel_name=form_values["hotel_name"],
                    name=class_name,
                    price_per_nigth=form_values[class_name],
                ))
        except Exception as e:
            errors.append(str(e))

        if errors:
            return render_template(
                "hotel/hotel_form.html", errors=errors, classes=class_names
            )

        # db.session.commit()

        return redirect("/hotel")

    return render_template("hotel/hotel_form.html", classes=class_names)
