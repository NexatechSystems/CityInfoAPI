from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI:
# Example for MySQL, adjust as per your actual database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@ABRAR\\MSSQLSERVER01/CityInfoDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'



db = SQLAlchemy(app)

# Define your models here (we'll do this in the next step)
class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    country = db.Column(db.String(100))
    coordinates = db.Column(db.String(100))

    hotels = db.relationship('Hotel', backref='location', lazy=True)
    pois = db.relationship('POI', backref='location', lazy=True)
    restaurants = db.relationship('Restaurant', backref='location', lazy=True)


class Hotel(db.Model):
    __tablename__ = 'hotel'
    hotel_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    coordinates = db.Column(db.String(100))
    hotel_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    email = db.Column(db.String(100))
    website = db.Column(db.String(100))


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    restaurant_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    coordinates = db.Column(db.String(100))
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    email = db.Column(db.String(100))
    website = db.Column(db.String(100))


class POI(db.Model):
    __tablename__ = 'poi'
    poi_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), nullable=False)
    coordinates = db.Column(db.String(100))
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    email = db.Column(db.String(100))
    website = db.Column(db.String(100))
    tag = db.Column(db.String(50))
    type = db.Column(db.String(50))

@app.route('/location/<string:location_name>', methods=['GET'])
def get_location_details(location_name):
    location = Location.query.filter_by(name=location_name).first()

    if not location:
        return jsonify({"error": "Location not found"}), 404

    hotels = [{'hotel_name': hotel.hotel_name, 'address': hotel.address} for hotel in location.hotels]
    pois = [{'poi_name': poi.name, 'address': poi.address} for poi in location.pois]
    restaurants = [{'restaurant_name': restaurant.name, 'address': restaurant.address} for restaurant in location.restaurants]

    return jsonify({
        'location': location.name,
        'hotels': hotels,
        'pois': pois,
        'restaurants': restaurants
    })

if __name__ == "__main__":
    app.run(debug=False)

