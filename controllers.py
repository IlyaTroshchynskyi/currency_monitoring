from flask import render_template, make_response

from models import XRate


def get_all_rates():
    try:
        xrates = XRate.query.all()
        return render_template("xrates.html", xrates=xrates)
    except Exception as ex:
        return make_response(str(ex), 500)