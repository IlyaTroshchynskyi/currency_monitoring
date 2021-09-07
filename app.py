from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///golden-eye.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from models import XRate


@app.route('/')
def index():
    a = XRate.query.all()
    return "<h1>Hello</h1>", a


if __name__ == '__main__':
    app.run(debug=True)