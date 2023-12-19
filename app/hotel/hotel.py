from flask import Blueprint, render_template
from app.database import db

from .models import Hotel

hotel_bp = Blueprint("hotel", __name__)


@hotel_bp.route("/", methods=["GET"])
def hotels():
    all_records_hotel = db.session.query(Hotel).all()
    return render_template("hotel/hotels.html", hotels=all_records_hotel)
