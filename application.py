from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager

from models.db import db
from resources.item import Item, ItemList

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# app.config["JWT_SECRET_KEY"] = "Dese.Decent.Pups.BOOYO0OST"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)

api = Api(app)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()

api.add_resource(Item, '/client')
api.add_resource(ItemList, '/clients')

if __name__ == '__main__':
    app.run(debug=True, port=8000)