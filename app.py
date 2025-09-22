from flask import Flask, render_template, request, session, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = "secret123"   # for session

# MongoDB Atlas connection
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://<user-name>:<password>@cluster0.acfjro2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
client = MongoClient(MONGO_URI)
db = client["giftshop"]
orders_collection = db["orders"]
# MongoDB Atlas connection
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://<user-name>:<password>@cluster0.acfjro2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
client = MongoClient(MONGO_URI)
db = client["giftshop"]
orders_collection = db["orders"]

# 10 Gifts (Static)
gifts = [
    {"id": 1, "name": "Teddy Bear", "price": 500, "image": "images/teddy.png"},
    {"id": 2, "name": "Flower Bouquet", "price": 300, "image": "images/Flower Bouquet.png"},
    {"id": 3, "name": "Chocolate Box", "price": 450, "image": "images/Chocolate Box.png"},
    {"id": 4, "name": "Coffee Mug", "price": 250, "image": "images/licensed-image.jpg"},
    {"id": 5, "name": "Photo Frame", "price": 350, "image": "images/Photo Frame.jpg"},
    {"id": 6, "name": "Perfume", "price": 700, "image": "images/Perfume.jpg"},
    {"id": 7, "name": "Keychain", "price": 150, "image": "images/Keychain.jpg"},
    {"id": 8, "name": "Watch", "price": 1200, "image": "images/Watch.jpg"},
    {"id": 9, "name": "Greeting Card", "price": 100, "image": "images/Greeting Card.jpg"},
    {"id": 10, "name": "Soft Toy Dog", "price": 600, "image": "images/Soft Toy Dog.jpg"}
]

@app.route("/")
def index():
    return render_template("index.html", gifts=gifts)

@app.route("/add_to_cart/<int:gift_id>", methods=["POST"])
def add_to_cart(gift_id):
    gift = next((item for item in gifts if item["id"] == gift_id), None)
    if gift:
        cart = session.get("cart", [])
        cart.append(gift)
        session["cart"] = cart
    return jsonify({"message": "Item added to cart", "cart": session["cart"]})

@app.route("/get_cart")
def get_cart():
    return jsonify(session.get("cart", []))

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    location = data.get("location")
    cart = session.get("cart", [])

    if not cart:
        return jsonify({"message": "Cart is empty!"}), 400

    # Save to MongoDB
    order = {
        "customer_name": name,
        "customer_email": email,
        "customer_location": location,
        "items": cart
    }
    orders_collection.insert_one(order)

    session["cart"] = []  # clear cart
    return jsonify({"message": "Thank you for shopping with Nikhil Gift Shopy 🎁! Your order is placed."})

if __name__ == "__main__":
    app.run(debug=True)

