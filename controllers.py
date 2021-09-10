from flask import render_template, make_response, jsonify, request
import xmltodict
from models import XRate


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
        print(xrates)
        xrates = self._filter(xrates)
        print('after--------------')

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
