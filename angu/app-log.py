from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"⚠️ Error loading model.pkl: {e}")
    model = None

users = {
  "alice": {"password": "wonderland"},
  "bob":   {"password": "builder"},
  "dirar":   {"password": "dirar"},
  "oussema":   {"password": "oussema"},
}

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({ 'error': 'Model not loaded' }), 500

    data = request.get_json() or {}
    days = data.get('resolution_days', None)
    if days is None:
        return jsonify({ 'error': 'Missing resolution_days' }), 400
    if not isinstance(days, (int, float)):
        return jsonify({ 'error': 'resolution_days must be numeric' }), 400

    try:
        # model expects a 2D array
        pred = model.predict([[days]])[0]
        return jsonify({ 'prediction': pred })
    except Exception as e:
        return jsonify({ 'error': f'Prediction error: {e}' }), 500
    
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    u = data.get("username","")
    p = data.get("password","")
    user = users.get(u)
    if user and user["password"] == p:
        return jsonify({ "success": True, "username": u }), 200
    return jsonify({ "success": False, "message": "Invalid credentials" }), 401


if __name__=="__main__":
    app.run(port=5000, debug=True)
