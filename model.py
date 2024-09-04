from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'

    code = db.Column(db.String(10), primary_key=True)
    unit_price = db.Column(db.Integer, nullable=False)
    special_price = db.Column(db.String(50), nullable=True)

    def __init__(self, code, unit_price, special_price=None):
        self.code = code
        self.unit_price = unit_price
        self.special_price = special_price

    def to_dict(self):
        return {
            'code': self.code,
            'unit_price': self.unit_price,
            'special_price': self.special_price
        }
