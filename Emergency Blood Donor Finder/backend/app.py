import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

sample_donors = [
    {"id": 1, "name": "Asha", "blood_group": "O+", "city": "Salem", "available": True},
    {"id": 2, "name": "Karthik", "blood_group": "A+", "city": "Chennai", "available": True},
    {"id": 3, "name": "Priya", "blood_group": "AB-", "city": "Coimbatore", "available": False},
]


@app.get("/")
def health_check():
    return jsonify({
        "status": "ok",
        "service": "blood-donor-backend",
        "message": "Backend is running"
    })


@app.get("/api/donors")
def get_donors():
    blood_group = request.args.get("blood_group", "").strip()
    city = request.args.get("city", "").strip()

    donors = sample_donors
    if blood_group:
        donors = [d for d in donors if d["blood_group"] == blood_group]
    if city:
        donors = [d for d in donors if city.lower() in d["city"].lower()]

    return jsonify({"donors": donors})


@app.post("/api/register")
def register_user():
    payload = request.get_json(force=True, silent=True) or {}
    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "data": payload,
    })


@app.post("/api/login")
def login_user():
    payload = request.get_json(force=True, silent=True) or {}
    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "email": payload.get("email"),
            "role": "donor"
        }
    })


@app.get("/api/admin")
def admin_info():
    return jsonify({
        "success": True,
        "message": "Admin API available",
        "username": os.getenv("ADMIN_USERNAME", "admin")
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
