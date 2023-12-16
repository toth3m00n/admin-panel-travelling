from flask import Blueprint, render_template, request, redirect

from app.database import db

client_bp = Blueprint('client', __name__)


@client_bp.route('/', methods=['GET'])
def clients():
    db.reflect()
    table_client = db.metadata.tables['client']
    all_records_client = db.session.query(table_client)
    return render_template('client/clients.html', clients=all_records_client)


@client_bp.route('/create', methods=['GET', 'POST'])
def create_client():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        sex = 'male' if request.form['gender'] == 'male' else 'female'
        age = request.form['age']
        telephone = request.form['telephone']
        job = request.form['job']

        hotel = request.form['hotel']
        class_name = request.form['class_name']
        room = request.form['room']

        checkin_day = request.form['checkin_day']
        checkin_month = request.form['checkin_month']
        checkin_year = request.form['checkin_year']

        checkout_day = request.form['checkout_day']
        checkout_month = request.form['checkout_month']
        checkout_year = request.form['checkout_year']
        
        return redirect("/client")

    return render_template('client/client_form.html')

