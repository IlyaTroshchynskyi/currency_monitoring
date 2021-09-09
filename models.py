from datetime import datetime
from app import db, app


class XRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_currency = db.Column(db.Integer, index=True)
    to_currency = db.Column(db.Integer, index=True)
    rate = db.Column(db.Float)
    updated = db.Column(db.DateTime, default=datetime.utcnow())
    module = db.Column(db.String(100))

    def __repr__(self):
        return "XRate(%s=>%s): %s" % (self.from_currency, self.to_currency, self.rate)


class ApiLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    request_url = db.Column(db.String(255))
    request_data = db.Column(db.Text, nullable=True)
    request_method = db.Column(db.String(100))
    request_headers = db.Column(db.Text, nullable=True)
    response_text = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    finished = db.Column(db.DateTime)
    error = db.Column(db.Text, nullable=True)


class ErrorLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    request_data = db.Column(db.Text, nullable=True)
    request_url = db.Column(db.Text)
    request_method = db.Column(db.String(255))
    error = db.Column(db.Text)
    traceback = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)


def init_db():
    # XRate.__table__.drop(app.config['SQLALCHEMY_DATABASE_URI'])
    # XRate.__table__.create(app.config['SQLALCHEMY_DATABASE_URI'])
    # db.drop_all()
    # db.create_all()
    XRate.query.delete()
    cur = XRate(from_currency=840, to_currency=980, rate=1, module="privat_api")
    cur2 = XRate(from_currency=840, to_currency=643, rate=1, module="cbr_api")
    cur3 = XRate(from_currency=1000, to_currency=840, rate=1, module="privat_api")
    cur4 = XRate(from_currency=1000, to_currency=980, rate=1, module="cryptonator_api")
    cur5 = XRate(from_currency=1000, to_currency=643, rate=1, module="cryptonator_api")

    for item in [cur, cur2, cur3, cur4, cur5]:
        db.session.add(item)

    db.session.commit()

    for m in (ApiLog, ErrorLog):
        # m.__table__.drop(app.config['SQLALCHEMY_DATABASE_URI'])
        # m.__table__.create(app.config['SQLALCHEMY_DATABASE_URI'])
        m.query.delete()
    db.session.commit()
    print("db created!")