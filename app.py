from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@db:5432/test_db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    
@app.before_first_request
def create_table():
    db.create_all()
    corn = Item(name='Corn', quantity=10)
    mango = Item(name='Mango', quantity=100)
    db.session.add_all([corn, mango])
    db.session.commit()

@app.route('/')
def index():
    return "Welcome to Flask API!"

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [{'name': item.name, 'quantity': item.quantity} for item in items]
    return jsonify({'items': items_list})

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = Item(name=data['name'], quantity=data['quantity'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item added successfully'})

@app.route('/items/<string:name>', methods=['DELETE'])
def delete_item(name):
    item = Item.query.filter_by(name=name).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    else:
        return jsonify({'message': 'Item not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

