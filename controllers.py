from datetime import datetime
from flask import render_template, make_response, jsonify, request, \
    redirect, url_for
import xmltodict
from models import XRate, ApiLog, ErrorLog
import api
from app import app, db


class BaseController:
    def __init__(self):
        self.request = request

    def call(self, *args, **kwargs):
        try:
            return self._call(*args, **kwargs)
        except Exception as ex:
            return make_response(str(ex), 500)

    def _call(self, *args, **kwargs):
        raise NotImplemented('call')


class ViewAllRates(BaseController):
    def _call(self):
        xrates = XRate.query.all()
        return render_template("xrates.html", xrates=xrates)


class GetApiRates(BaseController):
    def _call(self, fmt):
        xrates = XRate.query.all()
        xrates = self._filter(xrates)

        if fmt == "json":
            return self._get_json(xrates)
        elif fmt == 'xml':
            return self._get_xml(xrates)
        raise ValueError(f'Unknown fmt: {fmt}')

    def _filter(self, xrates):
        args = self.request.args
        print(args)
        if "from_currency" in args:
            xrates = [rate for rate in
                      xrates if rate.from_currency == int(args["from_currency"])]
            print(xrates, 'filter')

        if "to_currency" in args:
            xrates = [rate for rate in
                      xrates if rate.to_currency == int(args["to_currency"])]
        return xrates

    def _get_xml(self, xrates):
        d = {"xrates": {"xrate": [
            {"from": rate.from_currency, "to": rate.to_currency, "rate": rate.rate}
            for rate in xrates]}}
        return make_response(xmltodict.unparse(d), {'Content-Type': 'text/xml'})

    def _get_json(self, xrates):
        return jsonify([{"from": rate.from_currency, "to": rate.to_currency,
                         "rate": rate.rate} for rate in xrates])


class UpdateRates(BaseController):
    def _call(self, from_currency, to_currency):
        if not from_currency and not to_currency:
            self._update_all()

        elif from_currency and to_currency:
            self._update_rate(from_currency, to_currency)

        else:
            ValueError("from_currency and to_currency")
        return redirect(url_for("view_rates"))

    def _update_rate(self, from_currency, to_currency):
        api.update_rate(from_currency, to_currency)

    def _update_all(self):
        xrates = XRate.query.all()
        for rate in xrates:
            try:
                self._update_rate(rate.from_currency, rate.to_currency)
            except Exception as ex:
                print(ex)


class ViewLogs(BaseController):
    def _call(self, log_type):
        app.logger.debug("log_type: %s" % log_type)
        page = int(self.request.args.get("page", 1))
        logs_map = {"api": ApiLog, "error": ErrorLog}
        if log_type not in logs_map:
            raise ValueError("Unknown log_type %s" % log_type)
        log_model = logs_map[log_type]
        logs = log_model.query.order_by(ApiLog.id.desc()).paginate(page, 2)
        return render_template("logs.html", logs=logs)


class EditRate(BaseController):
    def _call(self, from_currency, to_currency):
        if self.request.method == "GET":
            return render_template("rate_edit.html",
                                   from_currency=from_currency,
                                   to_currency=to_currency)

        if "new_rate" not in request.form:
            raise Exception("new_rate parametr is required")

        if not request.form["new_rate"]:
            raise Exception("new_rate must be not empty")

        x_rate = XRate.query.filter_by(from_currency=from_currency,
                                 to_currency=to_currency).first()
        x_rate.rate = float(request.form['new_rate'])
        x_rate.updated = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('view_rates'))
