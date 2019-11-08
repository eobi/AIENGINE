from apipackage.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    userid = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    othernames = db.Column(db.String(80))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(50),unique=True,index=True)
    orgnaisionationame = db.Column(db.String(80))
    country = db.Column(db.String(80))
    isAdmin = db.Column(db.Integer)
    datetime = db.Column(db.String(80))

    def __init__(self, email, password, lastname, firstname, othernames, phone, country, orgnaisionationame, datetime, isAdmin):
        self.password = password
        self.lastname = lastname
        self.firstname = firstname
        self.othernames = othernames
        self.phone = phone
        self.email = email
        self.orgnaisionationame = orgnaisionationame
        self.country = country
        self.datetime = datetime
        self.isAdmin = isAdmin

    def json(self):
        return {
            'id': self.userid,
            "lastname": self.lastname,
            "firstname": self.firstname,
            "othernames": self.othernames,
            "phone": self.phone,
            "email": self.email,
            "orgnaisionationame": self.orgnaisionationame,
            "country": self.country,
            "datetime": self.datetime
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(userid=_id).first()

    @classmethod
    def set_as_admin(cls, _id):
        user = UserModel.find_by_id(_id)
        if user:
            db.session.update({user.isAdmin: 1}, synchronize_session=False)
            db.session.commit()
            return True

        return False

    @classmethod
    def check_if_admin(cls, _id):
        user = UserModel.find_by_id(_id)
        if user.isAdmin == 1:
            return True
        return False

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
