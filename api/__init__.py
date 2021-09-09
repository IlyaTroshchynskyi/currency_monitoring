from datetime import datetime
import traceback
import requests
from models import XRate, db, ApiLog, ErrorLog
from config import logging, LOGGER_CONFIG, HTTP_TIMEOUT


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

    def _send_request(self, url, method, data=None, headers=None):
        log = ApiLog(request_url=url, request_data=data, request_method=method,
                     request_headers=headers)
        try:
            response = self._send(method=method, url=url, headers=headers, data=data)
            log.response_text = response.text
            return response
        except Exception as ex:
            self.log.exception("Error during request sending")
            log.error = str(ex)
            err_log = ErrorLog(request_data=data, request_url=url, request_method=method,
                            error=str(ex), traceback=traceback.format_exc(chain=False))
            db.session.add(err_log)
            raise
        finally:
            log.finished = datetime.utcnow()
            db.session.add(log)
            db.session.commit()

    def _send(self, url, method, data=None, headers=None):
        return requests.request(method=method, url=url, headers=headers,
                                data=data, timeout=HTTP_TIMEOUT)