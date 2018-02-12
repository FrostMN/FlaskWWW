from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from FlaskWWW.models.event import Event
from FlaskWWW.models.item import Item
import FlaskWWW.utils.api as api
import json

from config import ITEMS_URL

import datetime

app = Flask(__name__)
app.config.from_object("config")

section = "home"


# user Routes


@app.route('/')
def index():
    global section
    concerts = []
    key = str

    if "session_key" in session.keys():
        key = session["session_key"]
        db_concerts = api.get_events(key)

        if len(db_concerts) > 0:
            for e in db_concerts:
                print(e)
                event_items = []

                db_items = api.get_event_items(key, e["id"])

                for item in db_items:
                    print(item)
                    event_items.append(Item(db=item))

                    print(event_items)

                concerts.append(Event(db=e, items=event_items))
    else:
        key = ""
    return render_template("index.html",
                           title=app.config["TITLE"],
                           section=section,
                           events=concerts,
                           items_url=ITEMS_URL,
                           session_key=key)


@app.route('/home')
def home():
    global section
    section = "home"
    return redirect(url_for("index"))


# admin Routes


@app.route('/admin/events')
def events():
    global section
    section = "events"
    return redirect(url_for("admin"))


@app.route('/admin/add/<key>/events', methods=["GET", "POST"])
def new_event(key):
    request_data = request.get_data().decode("utf-8")
    req_dict = unpack_request(request_data)
    print("key: ")
    print(key)
    print("new event: ")
    print(req_dict)

    day = int(req_dict["day"])
    month = int(req_dict["month"])
    year = int(req_dict["year"])

    print("from drop down: ")
    print(day)
    print(month)
    print(year)

    event_date = datetime.date(month=month, day=day, year=year)

    add_json = api.add_event(key, req_dict["name"], event_date)

    print(add_json)
    flash(add_json["message"])

    return redirect(url_for("events"))


@app.route('/admin/delete/<key>/events/<event_id>', methods=["GET", "POST"])
def delete_event(key, event_id):
    """ Api Route to delete an event from the DB """
    if request.method == "POST":
        delete_json = api.delete_event(key, event_id)
        flash(delete_json["message"])
        return redirect(url_for("events"))
    else:
        return redirect(url_for("events"))


@app.route('/admin/items')
def items():
    """ Sets the section variable so the admin route displays 'Items' section """
    global section
    section = "items"
    return redirect(url_for("admin"))


@app.route('/admin/add/<key>/items', methods=["GET", "POST"])
def new_item(key):
    """ API route for adding an Item"""
    request_data = request.get_data().decode("utf-8")
    req_dict = unpack_request(request_data)

    add_json = api.add_item(key, req_dict["name"], req_dict["description"], float(req_dict["price"]))

    flash(add_json["message"])

    return redirect(url_for("items"))


@app.route('/admin/<key>/delete/items/<item_id>', methods=["GET", "POST"])
def delete_item(key, item_id):
    if request.method == "POST":
        print("in delete_event()")
        print(key)
        print(item_id)
        delete_json = api.delete_item(key, item_id)
        print(delete_json)
        flash(delete_json["message"])

        return redirect(url_for("items"))
    else:
        return redirect(url_for("items"))


@app.route('/admin/users')
def users():
    global section
    section = "users"
    return redirect(url_for("admin"))


@app.route('/admin')
def admin():
    concerts = []
    merchandise = []
    year = datetime.datetime.now().year

    if "session_key" in session.keys():
        key = session["session_key"]
        db_concerts = api.get_events(key)
        db_items = api.get_items(key)

        if len(db_concerts) > 0:
            for event in db_concerts:
                concerts.append(Event(db=event))

        if len(db_items) > 0:
            for item in db_items:
                merchandise.append(Item(db=item))

    return render_template("admin.html", title=app.config["TITLE"], section=section, events=concerts, items=merchandise,
                           this_year=year)


@app.route('/login', methods=["GET", "POST"])
def login():
    if (request.method == 'POST') and ('user' not in session):
        request_data = request.form
        device = api.get_device_string(request.headers.get('User-Agent'))
        return api.do_login(request_data["email"], request_data["password"], device)
    else:
        return redirect(url_for("index"))


@app.route('/logout', methods=["GET", "POST"])
def logout():
    if "logged_in" in session.keys() and session["logged_in"]:
        device = api.get_device_string(request.headers.get('User-Agent'))
        api.do_logout(session["email"], session["session_key"], device)
        return redirect(url_for("index"))
    else:
        session.clear()
        flash("logged out")
        return redirect(url_for("index"))


@app.template_filter('format_date')
def format_date_filter(date):
    template = '%b, %d %Y'
    if isinstance(date, str):
        date = date.split(" ")[0]
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        day = int(date.split("-")[2])
        return datetime.datetime(day=day, month=month, year=year).strftime(template)
    return date.strftime(template)


def unpack_request(data):
    try:
        req_json = json.loads(data)
        req_dict = dict(req_json)
        print(req_dict)
    except ValueError:
        req_dict = request.form
        print(req_dict)
    return req_dict


if __name__ == '__main__':
    app.run(port=8080)
