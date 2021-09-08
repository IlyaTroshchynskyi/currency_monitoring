from datetime import datetime
import requests
from models import XRate, db
from config import logging, LOGGER_CONFIG


fh = logging.FileHandler(LOGGER_CONFIG["file"])
fh.setLevel(LOGGER_CONFIG["level"])
fh.setFormatter(LOGGER_CONFIG["formatter"])


class _Api:
    def __init__(self, logger_name):
        self.log = logging.getLogger(logger_name)
        self.log.addHandler(fh)
        self.log.setLevel(LOGGER_CONFIG["level"])

    def update_rate(self, from_currency, to_currency):
        self.log.info("Started update for: %s=>%s" % (from_currency, to_currency))
        xrate = XRate.query.filter_by(from_currency=from_currency,
                                      to_currency=to_currency).first()
        self.log.debug("rate before: %s", xrate)
        xrate.rate = self._update_rate(xrate)
        xrate.updated = datetime.utcnow()
        db.session.commit()
        self.log.debug("rate after: %s", xrate)
        self.log.info("Finished update for: %s=>%s" % (from_currency, to_currency))

    def _update_rate(self, xrate):
        raise NotImplementedError("_update_rate")