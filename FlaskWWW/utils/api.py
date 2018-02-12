from flask import redirect, url_for, session, flash
import requests
from config import USER_URL, ITEMS_URL
import json

from flask_api import status


def do_login(username, password, device):
    login_url = "{}/login".format(USER_URL)
    post_data = {"username": username, 'password': password, 'device': device}
    print(post_data)
    r = requests.post(login_url, data=post_data)
    print("r.text in do_login: ")
    print(r.text)
    login_dict = dict(json.loads(r.text))

    if login_dict["error"]:
        session.clear()
        flash(login_dict["message"])
        return redirect(url_for("home"))
    else:
        session["logged_in"] = True
        session["email"] = login_dict["email"]
        session["email_confirmed"] = login_dict["email_confirmed"]
        session["first_name"] = login_dict["first_name"]
        session["last_name"] = login_dict["last_name"]
        session["admin"] = login_dict["type"]
        session["user_id"] = login_dict["UserID"]
        session["session_key"] = login_dict["session_key"]
        session["language"] = login_dict["language"]
        flash(login_dict["message"])
        return redirect(url_for("home"))


def do_logout(username, key, device):
    logout_url = "{}/logout".format(USER_URL)
    post_data = {"username": username, 'session_key': key, 'device': device}

    r = requests.post(logout_url, data=post_data)
    logout_dict = dict(json.loads(r.text))
    session.clear()
    flash(logout_dict["message"])
    return redirect(url_for("home"))


def get_device_string(agent):
    browser = "unknown browser"
    os = "unknown system"
    if "Safari" in agent:
        browser = "Safari"
    if "Chrome" in agent:
        browser = "Chrome"

    if "Macintosh" in agent:
        os = "macOS"

    return "{} on {}".format(browser, os)


def get_events(key):
    print("in api.get_events()")
    events_url = "{}/api/v1/{}/events".format(ITEMS_URL, key)
    print(events_url)

    req_text = requests.get(events_url).text

    print("req_text: ")
    print(req_text)

    req_json = json.loads(req_text)

    print("req_json: ")
    print(req_json)

    req_dict = dict(req_json)

    print("req_dict: ")
    print(req_dict)
    print(req_dict.keys())

    if not req_dict["error"]:
        print("no errors")
        return req_dict["events"]


def delete_event(key, event_id):
    delete_url = "{}/api/v1/{}/delete/events/{}".format(ITEMS_URL, key, event_id)
    print(delete_url)

    delete_text = requests.post(delete_url).text

    print("delete_text: ")
    print(delete_text)

    delete_json = json.loads(delete_text)

    print("delete_json: ")
    print(delete_json)

    delete_dict = dict(delete_json)

    print("delete_dict: ")
    print(delete_dict)

    return delete_dict


def add_event(key, event_name, event_date):
    add_url = "{}/api/v1/{}/add/events".format(ITEMS_URL, key)
    post_data = {"event_name": event_name, 'session_key': key, 'event_date': event_date}
    print(add_url)
    print(event_name)
    print(event_date)
    print(post_data)
    add_text = requests.post(add_url, post_data).text

    print("add_text: ")
    print(add_text)

    add_json = json.loads(add_text)

    add_dict = dict(add_json)

    return add_dict


def get_items(key):
    print("in api.get_items()")
    events_url = "{}/api/v1/{}/items".format(ITEMS_URL, key)
    print(events_url)

    req_text = requests.get(events_url).text

    print("req_text: ")
    print(req_text)

    req_json = json.loads(req_text)

    print("req_json: ")
    print(req_json)

    req_dict = dict(req_json)

    print("req_dict: ")
    print(req_dict)
    print(req_dict.keys())

    if not req_dict["error"]:
        print("no errors")
        return req_dict["items"]


def add_item(key, item_name, item_description, item_price):
    add_url = "{}/api/v1/{}/items".format(ITEMS_URL, key)
    post_data = {"item_name": item_name,
                 'session_key': key,
                 'item_price': item_price,
                 'item_description': item_description}

    print(add_url)
    print(item_name)
    print(item_price)
    print(post_data)
    add_text = requests.post(add_url, post_data).text

    print("add_text: ")
    print(add_text)

    add_json = json.loads(add_text)

    add_dict = dict(add_json)

    return add_dict


def delete_item(key, item_id):
    delete_url = "{}/api/v1/{}/delete/items/{}".format(ITEMS_URL, key, item_id)
    print(delete_url)

    delete_text = requests.post(delete_url).text

    print("delete_text: ")
    print(delete_text)

    delete_json = json.loads(delete_text)

    print("delete_json: ")
    print(delete_json)

    delete_dict = dict(delete_json)

    print("delete_dict: ")
    print(delete_dict)

    return delete_dict


def get_event_items(key, event_id):
    print("in api.get_event_items()")
    items_url = "{}/api/v1/{}/event/{}/items".format(ITEMS_URL, key, event_id)
    print(items_url)
    rs = requests.get(items_url).text
    print(rs)
    items_json = json.loads(rs)
    print(items_json)
    return items_json["items"]


def delete_event_item(key, event_id, sale_id):
    print("in api.delete_event_item()")
    delete_url = "{}/api/v1/{}/event/{}/delete/items/{}".format(ITEMS_URL, key, event_id, sale_id)
    print(delete_url)
    return requests.post(delete_url)

