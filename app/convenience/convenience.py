from flask import Blueprint, render_template, request, redirect
from sqlalchemy import distinct, and_

from app import Class, Hotel, ClassConvenience
from app.database import db
from .models import Convenience

convenience_bp = Blueprint("convenience", __name__)


def error_handler(class_names, hotel_names, form_values, errors):
    return render_template(
        "convenience/convenience_form.html",
        classes=class_names,
        hotels=hotel_names,
        convenience=Convenience(name=form_values["convenience_name"], size=form_values["size"]),
        errors=errors,
    )


@convenience_bp.route("/", methods=["GET"])
def conveniences():
    all_records_conveniences = db.session.query(Convenience).all()
    return render_template(
        "convenience/conveniences.html", conveniences=all_records_conveniences
    )

@convenience_bp.route("/create", methods=["GET", "POST"])
def create_convenience():
    errors = []
    class_names = db.session.query(distinct(Class.name)).all()
    hotel_names = db.session.query(Hotel).all()

    if request.method == "POST":

        form_values = {}
        # считывает все формы в словарь, а потом его распаковыввает
        for convenience_info in request.form:
            if request.form[convenience_info] != "":
                form_values[convenience_info] = request.form[convenience_info]

        try:
            db.session.add(
                Convenience(
                    name=form_values["convenience_name"], size=form_values["size"]
                )
            )
        except Exception as err:
            db.session.rollback()
            errors.append(str(err))

        if errors:
            error_handler(class_names, hotel_names, form_values, errors)

        db.session.commit()

        try:
            for convenience_info in form_values:

                if (
                    convenience_info != "size"
                    and convenience_info != "convenience_name"
                ):
                    hotel_name, class_name = convenience_info.split("_")
                    class_id = (
                        db.session.query(Class.id)
                        .filter(
                            and_(
                                Class.name == class_name, Class.hotel_name == hotel_name
                            )
                        )
                        .scalar()
                    )

                    data_for_class_convenience = {
                        "convenience_name": form_values["convenience_name"],
                        "class_id": class_id,
                        "amount": int(form_values[convenience_info]),
                    }

                    db.session.add(ClassConvenience(**data_for_class_convenience))

        except Exception as err:
            db.session.rollback()
            errors.append(str(err))

        if errors:
            error_handler(class_names, hotel_names, form_values, errors)

        db.session.commit()

        return redirect("/convenience")

    return render_template(
        "convenience/convenience_form.html",
        classes=class_names,
        hotels=hotel_names,
        convenience=None,
        amounts=None
    )


@convenience_bp.route("/<slug:convenience_name>", methods=["GET", "POST", "DELETE"])
def get_convenience(convenience_name: str):

    origin_convenience_name = convenience_name.replace("_", " ")
    uniq_convenience = db.session.query(Convenience).filter(Convenience.name == origin_convenience_name).first()

    class_names = db.session.query(distinct(Class.name)).all()
    hotel_names = db.session.query(Hotel).all()

    amounts = {}
    for class_obj in class_names:
        for hotel_obj in hotel_names:
            class_id = (
                db.session.query(Class.id)
                .filter(
                    and_(
                        Class.name == class_obj[0], Class.hotel_name == hotel_obj.name
                    )
                )
                .scalar()
            )

            amount = db.session.query(ClassConvenience.amount).filter(and_(ClassConvenience.class_id == class_id,
                                                                    ClassConvenience.convenience_name == origin_convenience_name)).scalar()
            amounts[f'{hotel_obj.name}_{class_obj[0]}'] = amount

    if request.method == "POST":
        errors = []
        form_values = {}

        # считывает все формы в словарь, а потом его распаковыввает
        for convenience_info in request.form:
            if convenience_info not in ('convenience_name', 'size'):
                if int(amounts[convenience_info]) == int(request.form[convenience_info]):
                    continue
            form_values[convenience_info] = request.form[convenience_info]

        insert_data_convenience = {
            "name": form_values["convenience_name"],
            "size": int(form_values["size"]),
        }

        if form_values["convenience_name"] != origin_convenience_name:
            try:
                # обновляю всё в классах
                db.session.query(ClassConvenience).filter_by(convenience_name=origin_convenience_name).update(
                    {"convenience_name": None}
                )
            except Exception as err:
                errors.append(str(err))
                db.session.rollback()

            if errors:
                error_handler(class_names, hotel_names, form_values, errors)

            db.session.commit()

        # Это выполняю в любом случае - тк не обязательно менять имя удобства
        try:
            db.session.query(Convenience).filter_by(name=origin_convenience_name).update(
                insert_data_convenience
            )
        except Exception as err:
            errors.append(str(err))
            db.session.rollback()

        if errors:
            error_handler(class_names, hotel_names, form_values, errors)

        db.session.commit()

        if form_values["convenience_name"] != origin_convenience_name:
            try:
                db.session.query(ClassConvenience).filter_by(convenience_name=None).update(
                    {"convenience_name": form_values["convenience_name"]}
                )
            except Exception as err:
                errors.append(str(err))
                db.session.rollback()

            if errors:
                error_handler(class_names, hotel_names, form_values, errors)

            db.session.commit()

        try:
            for hotel_class in form_values:
                if hotel_class not in ('convenience_name', 'size'):
                    hotel_name, class_name = hotel_class.split('_')
                    class_id = db.session.query(Class.id).filter(and_(Class.name == class_name,
                                                                      Class.hotel_name == hotel_name)).scalar()

                    db.session.query(ClassConvenience).filter(and_(ClassConvenience.convenience_name == origin_convenience_name,
                                                                   ClassConvenience.class_id == class_id)).update(
                        {"amount": form_values[hotel_class]}
                    )

        except Exception as err:
            errors.append(str(err))
            db.session.rollback()

        if errors:
            error_handler(class_names, hotel_names, form_values, errors)

        db.session.commit()

        return redirect('/convenience')

    return render_template(
        "convenience/convenience_form.html",
        classes=class_names,
        hotels=hotel_names,
        convenience=uniq_convenience,
        amounts=amounts
    )


@convenience_bp.route("<slug:convenience_name>/delete", methods=["POST"])
def delete_client(convenience_name: str):
    """ delete convenience and convenience_name row """
    origin_convenience_name = convenience_name.replace("_", " ")
    print(origin_convenience_name)
    errors = []
    try:
        db.session.query(Convenience).filter_by(name=origin_convenience_name).delete()
    except Exception as err:
        uniq_convenience = db.session.query(Convenience).filter_by(name=origin_convenience_name).first()
        errors.append(str(err))
        db.session.rollback()
        print(errors)
        return render_template("convenience/convenience_form.html",
                               convenience=uniq_convenience, errors=errors)
    db.session.commit()
    return redirect("/convenience")

