
from app import db
from sqlalchemy.dialects.postgresql import JSON, JSONB

class survey(db.Model):
   id = db.Column('_id', db.Integer, primary_key = True) 
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
   id = db.Column('question_id', db.Integer, primary_key = True) 
   question = db.Column(JSON)
   prev_field_name = db.Column(db.String(100))
   next_field_name = db.Column(db.String(100))
   validation = db.Column(db.String(100))

class user_profile(db.Model):
   id = db.Column('_id', db.Integer, primary_key = True) 
   sender_id = db.Column(db.String(100))
   first_name = db.Column(db.String(100))
   last_name = db.Column(db.String(100))
   profile_pic = db.Column(db.String(5000))


#    def __repr__(self):
#         return '<User %r>' % (self.sender_id)


# def __init__(self, sender_id, Entry, Demog_Permission, Demog_Loc, Demog_Gender, Demog_Age, Demog_Resp_Edu, Demog_Resp_Occu, Demog_Resp_MaritalStatus, Demog_Resp_Member, SocEco_MHI):
#    self.sender_id = sender_id
#    self.Entry = Entry
#    self.Demog_Permission = Demog_Permission
#    self.Demog_Loc = Demog_Loc
#    self.Demog_Gender = Demog_Gender
#    self.Demog_Age = Demog_Age
#    self.Demog_Resp_Edu = Demog_Resp_Edu
#    self.Demog_Resp_Occu = Demog_Resp_Occu
#    self.Demog_Resp_MaritalStatus = Demog_Resp_MaritalStatus
#    self.Demog_Resp_Member = Demog_Resp_Member
#    self.SocEco_MHI = SocEco_MHI
   