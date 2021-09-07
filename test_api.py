from datetime import datetime
from app import db
from models import XRate


def update_xrates(from_currency, to_currency):

    xrate = XRate.query.filter_by(from_currency=from_currency,
                                  to_currency=to_currency).first()
    xrate.rate += 0.01
    xrate.updated = datetime.utcnow()
    db.session.commit()
