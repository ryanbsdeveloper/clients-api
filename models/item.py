from .db import db


class ClientModel(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    passwordConfirmation = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    def __init__(self, name, email, password, passwordConfirmation, phone=None):
        self.name = name
        self.email = email
        self.password = password
        self.passwordConfirmation = passwordConfirmation
        self.phone = phone

    def json(self):
        return {'name': self.name, 'email': self.email, 'password': self.password, 'passwordConfirmation': self.passwordConfirmation, 'phone': self.phone}

    @classmethod
    def find_by_client(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
