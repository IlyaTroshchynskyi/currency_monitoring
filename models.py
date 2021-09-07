from datetime import datetime
from app import db


class XRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_currency = db.Column(db.Integer, index=True)
    to_currency = db.Column(db.Integer, index=True)
    rate = db.Column(db.Float)
    updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return "XRate(%s=>%s): %s" % (self.from_currency, self.to_currency, self.rate)


def init_db():
    db.drop_all()
    db.create_all()
    cur = XRate(from_currency=840, to_currency=980, rate=1)
    db.session.add(cur)
    db.session.commit()
    print("db created!")