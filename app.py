from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
model = SentenceTransformer("all-MiniLM-L6-v2")
products = [
    {"id": 1, "name": "Running Shoes", "price": 80, "category": "Sports", "description": "Lightweight shoes for running", "rating": 4.5},
    {"id": 2, "name": "Basketball", "price": 30, "category": "Sports", "description": "Official size basketball", "rating": 4.2},
    {"id": 3, "name": "Laptop Backpack", "price": 45, "category": "Accessories", "description": "Waterproof backpack for laptops", "rating": 4.8},
    {"id": 4, "name": "Wireless Mouse", "price": 25, "category": "Electronics", "description": "Ergonomic wireless mouse", "rating": 4.0},
    {"id": 5, "name": "Bluetooth Headphones", "price": 65, "category": "Electronics", "description": "Noise-cancelling headphones", "rating": 4.7},
    {"id": 6, "name": "Smart Watch", "price": 150, "category": "Electronics", "description": "Fitness tracker and smart notifications", "rating": 4.4},
    {"id": 7, "name": "Yoga Mat", "price": 20, "category": "Fitness", "description": "Non-slip yoga mat", "rating": 4.3},
    {"id": 8, "name": "Gaming Keyboard", "price": 60, "category": "Electronics", "description": "Mechanical keyboard with RGB lights", "rating": 4.6}
]
product_texts = [f"{p['name']} {p['description']} category: {p['category']} price: {p['price']} rating: {p['rating']}" for p in products]
product_embeddings = model.encode(product_texts, convert_to_tensor=True)
def apply_dynamic_pricing():
    updated = []
    for p in products:
        price = p["price"]
        if p["rating"] >= 4.5:
            price *= 1.10  
        elif p["rating"] < 4.0:
            price *= 0.90  
        updated.append({**p, "price": round(price, 2)})
    return updated

@app.route("/")
def home():
    updated_products = apply_dynamic_pricing()
    return render_template("index.html", products=updated_products)

@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("query", "")
    if not query.strip():
        return jsonify(apply_dynamic_pricing())

    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, product_embeddings)[0]
    top_indices = scores.argsort(descending=True)
    
    matched = []
    for idx in top_indices:
        matched.append(products[int(idx)])
    return jsonify(matched)

@app.route("/recommend", methods=["POST"])
def recommend():
    selected_id = request.json.get("id")
    selected_product = next((p for p in products if p["id"] == selected_id), None)
    if not selected_product:
        return jsonify([])

    recs = [p for p in products if p["category"] == selected_product["category"] and p["id"] != selected_id]
    return jsonify(recs[:3])

if __name__ == "__main__":
    app.run(debug=True)
