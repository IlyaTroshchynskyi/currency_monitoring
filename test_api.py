from datetime import datetime
from app import db
from models import XRate
from config import logging, LOGGER_CONFIG


log = logging.getLogger("TestApi")
fh = logging.FileHandler(LOGGER_CONFIG["file"])
fh.setLevel(LOGGER_CONFIG["level"])
fh.setFormatter(LOGGER_CONFIG["formatter"])
log.addHandler(fh)
log.setLevel(LOGGER_CONFIG["level"])


def update_xrates(from_currency, to_currency):
    log.info("Started update for: %s=>%s" % (from_currency, to_currency))
    xrate = XRate.query.filter_by(from_currency=from_currency,
                                  to_currency=to_currency).first()
    log.debug("rate before: %s", xrate)
    xrate.rate += 0.01
    xrate.updated = datetime.utcnow()
    db.session.commit()
    log.debug("rate after: %s", xrate)
    log.info("Finished update for: %s=>%s" % (from_currency, to_currency))