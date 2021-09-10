import unittest
from unittest.mock import patch
import json
import xmltodict
import xml.etree.ElementTree as ET
import requests
import models
import api


def get_privat_response(*args, **kwds):
    print("get_privat_response")

    class Response:
        def __init__(self, response):
            self.text = json.dumps(response)

        def json(self):
            return json.loads(self.text)

    return Response([{"ccy": "USD", "base_ccy": "UAH", "sale": "30.0"}])


class Test(unittest.TestCase):
    def setUp(self):
        models.init_db()

    @unittest.skip("skip")
    def test_privat_usd(self):
        xrate = models.XRate.query.filter_by(id=1).first()
        updated_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)

        api.update_rate(840, 980)

        xrate = models.XRate.query.filter_by(id=1).first()
        updated_after = xrate.updated

        self.assertGreater(xrate.rate, 25)
        self.assertGreater(updated_after, updated_before)
        api_log = models.ApiLog.query.order_by(models.ApiLog.created.desc()).first()
        self.assertEqual(api_log.request_url,
                         "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        self.assertIsNotNone(api_log.response_text)

        self.assertIn('{"ccy":"USD","base_ccy":"UAH",', api_log.response_text)

    @unittest.skip('skip')
    def test_privat_btc(self):
        xrate = models.XRate.query.filter_by(from_currency=1000,
                                             to_currency=840).first()
        updated_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)

        api.update_rate(1000, 840)

        xrate = models.XRate.query.filter_by(from_currency=1000,
                                             to_currency=840).first()
        updated_after = xrate.updated

        self.assertGreater(xrate.rate, 5000)
        self.assertGreater(updated_after, updated_before)
        api_log = models.ApiLog.query.order_by(models.ApiLog.created.desc()).first()
        self.assertEqual(api_log.request_url,
                         "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")


        self.assertIn('{"ccy":"USD","base_ccy":"UAH",', api_log.response_text)

    @unittest.skip('skip')
    def test_cbr(self):
        xrate = models.XRate.query.filter_by(from_currency=840, to_currency=643).first()
        updated_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        api.update_rate(840, 643)
        xrate = models.XRate.query.filter_by(from_currency=840, to_currency=643).first()
        updated_after = xrate.updated

        self.assertGreater(xrate.rate, 10)
        self.assertGreater(updated_after, updated_before)
        api_log = models.ApiLog.query.order_by(models.ApiLog.created.desc()).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, "http://www.cbr.ru/scripts/XML_daily.asp")
        self.assertIsNotNone(api_log.response_text)
        self.assertIn("<NumCode>840</NumCode>", api_log.response_text)

    @unittest.skip('skip')
    @patch('api._Api._send', new=get_privat_response)
    def test_privat_mock(self):

        xrate = models.XRate.query.filter_by(id=1).first()
        updated_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)

        api.update_rate(840, 980)

        xrate = models.XRate.query.filter_by(id=1).first()
        updated_after = xrate.updated

        self.assertEqual(xrate.rate, 30)
        self.assertGreater(updated_after, updated_before)

        api_log = models.ApiLog.query.order_by(models.ApiLog.created.desc()).first()

        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url,
                         "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        self.assertIsNotNone(api_log.response_text)

        self.assertEqual('[{"ccy": "USD", "base_ccy": "UAH", "sale": "30.0"}]',
                         api_log.response_text)

    @unittest.skip('skip')
    def test_api_error(self):
        api.HTTP_TIMEOUT = 0.001
        xrate = models.XRate.query.filter_by(id=1).first()
        updated_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)

        self.assertRaises(requests.exceptions.RequestException,
                          api.update_rate, 840, 980)

        xrate = models.XRate.query.filter_by(id=1).first()
        updated_after = xrate.updated

        self.assertEqual(xrate.rate, 1.0)
        self.assertEqual(updated_after, updated_before)

        api_log = models.ApiLog.query.order_by(models.ApiLog.created.desc()).first()

        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url,
                         "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        self.assertIsNone(api_log.response_text)
        self.assertIsNotNone(api_log.error)

        error_log = models.ErrorLog.query.order_by(models.ErrorLog.created.desc()).first()
        self.assertIsNotNone(error_log)
        self.assertEqual(error_log.request_url,
                         "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        self.assertIsNotNone(error_log.traceback)
        self.assertEqual(api_log.error, error_log.error)
        self.assertIn("Connection to api.privatbank.ua timed out", error_log.error)

        api.HTTP_TIMEOUT = 15

    @unittest.skip("error 520")
    def test_cryptonator_uah(self):
        from_currency = 1000
        to_currency = 980
        xrate = models.XRate.query.filter_by(from_currency=from_currency,
                                             to_currency=to_currency).first()
        updated_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)

        api.update_rate(from_currency, to_currency)

        xrate = models.XRate.query.filter_by(from_currency=from_currency,
                                             to_currency=to_currency).first()
        updated_after = xrate.updated

        self.assertGreater(xrate.rate, 150000)
        self.assertGreater(updated_after, updated_before)

        api_log = models.ApiLog.query.order_by(models.ApiLog.created.desc()).first()

        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, "https://api.cryptonator.com/api/ticker/btc-uah")
        self.assertIsNotNone(api_log.response_text)

        self.assertIn('{"base":"BTC","target":"UAH","price":', api_log.response_text)

    def test_xml_api(self):
        r = requests.get("http://localhost:5000/api/xrates/xml")
        self.assertIn("<xrates>", r.text)
        xml_rates = xmltodict.parse(r.text)
        print(xml_rates)
        self.assertIn("xrates", xml_rates)
        self.assertIsInstance(xml_rates["xrates"]["xrate"], list)
        self.assertEqual(len(xml_rates["xrates"]["xrate"]), 5)

    def test_json_api(self):
        r = requests.get("http://localhost:5000/api/xrates/json")
        json_rates = r.json()
        print(json_rates)
        self.assertIsInstance(json_rates, list)
        self.assertEqual(len(json_rates), 5)
        for rate in json_rates:
            self.assertIn('from', rate)
            self.assertIn('to', rate)
            self.assertIn('rate', rate)

    def test_json_api_uah(self):
        r = requests.get("http://localhost:5000/api/xrates/json?to_currency=980")
        json_rates = r.json()
        print(json_rates)
        self.assertIsInstance(json_rates, list)
        self.assertEqual(len(json_rates), 2)

    def test_html_xrates(self):
        r = requests.get("http://localhost:5000/xrates")
        print(r)
        self.assertTrue(r.ok)
        self.assertIn('<table border="1">', r.text)
        root = ET.fromstring(r.text)
        body = root.find("body")
        self.assertIsNotNone(body)
        table = body.find("table")
        self.assertIsNotNone(table)
        rows = table.findall("tr")
        self.assertEqual(len(rows), 5)


if __name__ == '__main__':
    unittest.main()