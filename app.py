# Standard Library
import json
import os
import sys
from datetime import datetime

# Third Party Stuff
import requests
from flask import render_template, request
import logging
from logging.handlers import RotatingFileHandler

# Public Pulse Stuff
import model
from settings import app


# Privacy Policy Route


@app.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy-policy.html')

# Term of Use Route


@app.route('/term-of-use', methods=['GET'])
def term_of_use():
    return render_template('term-of-use.html')

# Index Route


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ.get("verify_token"):
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return render_template('index.html'), 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    # the facebook ID of the person sending you the message
                    sender_id = messaging_event["sender"]["id"]
                    # the recipient's ID, which should be your page's facebook ID
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]  # the message's text
                    try:
                        row = model.survey.query.filter_by(sender_id=sender_id).first()
                        log(row)

                        if row is not None:
                            try:
                                question = model.question_new.query.filter_by(
                                    prev_field_name=row.last_question_answered).first()
                                field_name = question.prev_field_name

                                log(field_name)
                                row.last_question_answered = question.next_field_name

                                message_content_text = message_content(message_text)
                                setattr(row, field_name, message_content_text)
                                send_message(sender_id, json.dumps(question.question))
                                model.db.session.commit()

                            except Exception as error:
                                log(error)
                        else:
                            data = {
                                "text": "I am very basic program who can ask some simple questions in order and can "
                                        "store the answer I get from you as an answer. Let's talk about you and let "
                                        "me understand your profile a little more.",
                                "quick_replies": [{"content_type": "text", "title": "Yes", "payload": "yes", }]
                            }
                            msg = json.dumps(data)
                            # row_ques = (msg, 'Entry', 0)
                            post_profile(sender_id)
                            log(sender_id)
                            log(message_text["text"])
                            survey_var = model.survey(sender_id=sender_id,
                                                      entry=message_text["text"],
                                                      last_question_answered="demog_permission")
                            model.db.session.add(survey_var)
                            model.db.session.commit()

                            send_message(sender_id, msg)

                    except Exception as error:
                        log("error")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ.get("fb_access_token")
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": message_text
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def message_content(message_text):
    # log(message_text)
    if 'attachments' not in message_text:
        message_content_text = message_text["text"]
    else:
        lat = message_text["attachments"][0]["payload"]["coordinates"]["lat"]
        lon = message_text["attachments"][0]["payload"]["coordinates"]["long"]
        message_content_text = str(lat) + " , " + str(lon)

    return message_content_text


def post_profile(sender_id):
    access_token = os.environ.get("fb_access_token")
    r = requests.get("https://graph.facebook.com/v2.6/" + sender_id +
                     "?fields=first_name,last_name,profile_pic&access_token=" + access_token).json()
    user_data = model.user_profile(sender_id=r["id"], first_name=r["first_name"],
                                   last_name=r["last_name"], profile_pic=r["profile_pic"])
    model.db.session.add(user_data)
    model.db.session.commit()


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = str(msg).format(*args, **kwargs)
        app.logger.info(msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    model.db.create_all()
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
