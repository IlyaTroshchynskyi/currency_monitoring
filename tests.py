import unittest
import models
from api import cbr_api, privat_api, test_api


class Test(unittest.TestCase):
    def setUp(self):
        models.init_db()

    def test_main(self):
        xrate = models.XRate.query.filter_by(id=1).first()
        print(xrate.rate)
        self.assertEqual(xrate.rate, 1.0)
        test_api.update_xrates(840, 980)
        xrate = models.XRate.query.filter_by(id=1).first()

        self.assertEqual(xrate.rate, 1.01)

    def test_privat(self):
        xrate = models.XRate.query.filter_by(id=1).first()
        updated_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        privat_api.update_xrates(840, 980)
        xrate = models.XRate.query.filter_by(id=1).first()
        updated_after = xrate.updated

        self.assertGreater(xrate.rate, 25)
        self.assertGreater(updated_after, updated_before)

    def test_cbr(self):
        xrate = models.XRate.query.filter_by(id=1).first()
        updated_before = xrate.updated
        self.assertEqual(xrate.rate, 1.0)
        cbr_api.Api().update_rate(840, 980)
        xrate = models.XRate.query.filter_by(id=1).first()
        updated_after = xrate.updated

        self.assertGreater(xrate.rate, 60)
        self.assertGreater(updated_after, updated_before)


if __name__ == '__main__':
    unittest.main()