from flask import Blueprint, render_template, request, redirect
from sqlalchemy import distinct, and_

from app.class_type.models import Class
from app.database import db

from .models import Hotel

hotel_bp = Blueprint("hotel", __name__)


@hotel_bp.route("/", methods=["GET"])
def hotels():
    all_records_hotel = db.session.query(Hotel).all()
    return render_template("hotel/hotels.html", hotels=all_records_hotel)


def validate_hotel(name: str, count_stars: int, hotel_names: list) -> list:
    """ validate hotel info: name, check uniq hotel name and count stars """

    errors = []
    if name.isdigit():
        errors.append("Hotel name must consist only latin letter!")
    for hotel_name in hotel_names:
        if name == hotel_name[0]:
            errors.append(
                "Hotel with this name already exist. Please enter unique name"
            )
            break
    if count_stars > 5 or count_stars < 1:
        errors.append("Amount of stars must be between 1.0 and 5.0")

    return errors


def validate_update_hotel(name: str, count_stars: float) -> list:
    """ validate hotel data in update """
    errors = []
    if name.isdigit():
        errors.append("Hotel name must consist only latin letter!")
    if count_stars > 5 or count_stars < 1:
        errors.append("Amount of stars must be between 1.0 and 5.0")

    return errors


@hotel_bp.route("/create", methods=["GET", "POST"])
def create_hotel():
    """ creation new hotel """

    hotel_names = db.session.query(distinct(Class.hotel_name)).all()
    class_names = db.session.query(distinct(Class.name)).all()
    if request.method == "POST":

        # for hotel
        form_values = {}

        # считывает все формы в словарь, а потом его распаковыввает
        for hotel_info in request.form:
            form_values[hotel_info] = request.form[hotel_info]

        print(form_values)
        errors = validate_hotel(
            form_values["hotel_name"], int(form_values["count_stars"]), hotel_names,
        )

        insert_data_hotel = {
            "name": form_values["hotel_name"],
            "count_stars": form_values["count_stars"],
        }

        try:
            db.session.add(Hotel(**insert_data_hotel))
            for class_type in class_names:
                class_name = class_type[0]
                db.session.add(
                    Class(
                        hotel_name=form_values["hotel_name"],
                        name=class_name,
                        price_per_night=form_values[class_name],
                    )
                )
        except Exception as e:
            errors.append(str(e))
            db.session.rollback()

        if errors:
            return render_template(
                "hotel/hotel_form.html",
                errors=errors,
                classes=class_names,
                hotel=Hotel(**insert_data_hotel),
                price=form_values,
            )

        db.session.commit()

        return redirect("/hotel")

    return render_template(
        "hotel/hotel_form.html", classes=class_names, hotel=None, price=None
    )


@hotel_bp.route("/<slug:hotel_name>", methods=["GET", "POST"])
def get_hotel(hotel_name: str):

    origin_hotel_name = hotel_name.replace("_", " ")
    uniq_hotel = db.session.query(Hotel).filter_by(name=origin_hotel_name).first()
    prices = db.session.query(Class).filter(Class.hotel_name == origin_hotel_name).all()
    class_names = db.session.query(distinct(Class.name)).all()

    all_price_data = {}

    for price in prices:
        all_price_data[price.name] = int(price.price_per_night)

    if request.method == "POST":

        form_values = {}
        for hotel_info in request.form:
            form_values[hotel_info] = request.form[hotel_info]

        errors = validate_update_hotel(
            form_values["hotel_name"], float(form_values["count_stars"]),
        )

        insert_data_hotel = {
            "name": form_values["hotel_name"],
            "count_stars": float(form_values["count_stars"]),
        }

        if form_values["hotel_name"] != origin_hotel_name:

            try:
                # обновляю всё в классах
                db.session.query(Class).filter_by(hotel_name=origin_hotel_name).update(
                    {"hotel_name": None}
                )
            except Exception as err:
                errors.append(str(err))
                db.session.rollback()
            db.session.commit()

        # Это выполняю в любом случае - тк не обязательно менять имя отеля
        try:
            db.session.query(Hotel).filter_by(name=origin_hotel_name).update(
                insert_data_hotel
            )
        except Exception as err:
            errors.append(str(err))
            db.session.rollback()
        db.session.commit()

        if form_values["hotel_name"] != origin_hotel_name:
            try:
                db.session.query(Class).filter_by(hotel_name=None).update(
                    {"hotel_name": form_values["hotel_name"]}
                )
            except Exception as err:
                errors.append(str(err))
                db.session.rollback()
            db.session.commit()

        try:
            for class_name in class_names:
                name = class_name[0]
                print(name, form_values[name])
                db.session.query(Class).filter(and_(
                    Class.hotel_name == form_values["hotel_name"], Class.name == name
                )).update({"price_per_night": form_values[name]})
        except Exception as err:
            errors.append(str(err))
            db.session.rollback()

        if errors:
            return render_template(
                "hotel/hotel_form.html",
                errors=errors,
                hotel=Hotel(**insert_data_hotel),
                price=all_price_data,
                classes=class_names,
            )

        db.session.commit()

        return redirect("/hotel")

    return render_template(
        "/hotel/hotel_form.html",
        hotel=uniq_hotel,
        price=all_price_data,
        classes=class_names,
    )
