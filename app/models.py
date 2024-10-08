import uuid

import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class SKUModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String)
    product_title = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

    # JSON serializer
    def to_json(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "product_title": self.product_title,
            "quantity": self.quantity,
            "price": self.price,
        }


class DeviceModel(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(80))
    device_key = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel", back_populates="devices")

    def __init__(self, device_name, user_id, device_key=None):
        self.device_name = device_name
        self.user_id = user_id
        self.device_key = device_key or uuid.uuid4().hex

    def json(self):
        return {
            "device_name": self.device_name,
            "device_key": self.device_key,
            "user_id": self.user_id,
        }

    @classmethod
    def find_by_name(cls, device_name):
        return cls.query.filter_by(device_name=device_name).first()

    @classmethod
    def find_by_device_key(cls, device_key):
        return cls.query.filter_by(device_key=device_key).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    devices = db.relationship("DeviceModel", back_populates="user")
