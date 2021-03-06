import requests
from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://main:traincascade@db:5432/main'
# app.config.from_object("main.config.Config")
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    __tablename__ = 'product_user'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='user_product_unique'),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
@cross_origin()
def like(id):
    req = requests.get('http://172.168.0.20:8020/api/user', timeout=5)
    json = req.json()

    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
    except:
        abort(400, 'You already liked this product')
    return jsonify({
        'message': 'success'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
