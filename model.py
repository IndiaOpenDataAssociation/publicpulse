from settings import db
from sqlalchemy.dialects.postgresql import JSON


class survey(db.Model):
    id = db.Column('_id', db.Integer, primary_key=True)
    sender_id = db.Column(db.String(100))
    entry = db.Column(db.String(500))
    demog_permission = db.Column(db.String(500))
    demog_loc = db.Column(db.String(500))
    demog_gender = db.Column(db.String(500))
    demog_age = db.Column(db.String(500))
    demog_resp_edu = db.Column(db.String(500))
    demog_resp_occu = db.Column(db.String(500))
    demog_resp_maritalstatus = db.Column(db.String(500))
    demog_resp_member = db.Column(db.String(500))
    soceco_mhi = db.Column(db.String(500))
    last_question_answered = db.Column(db.String(100))


class question_new(db.Model):
    id = db.Column('question_id', db.Integer, primary_key=True)
    question = db.Column(JSON)
    prev_field_name = db.Column(db.String(100))
    next_field_name = db.Column(db.String(100))
    validation = db.Column(db.String(100))


class user_profile(db.Model):
    id = db.Column('_id', db.Integer, primary_key=True)
    sender_id = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    profile_pic = db.Column(db.String(5000))
