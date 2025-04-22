from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

# Your token
API_TOKEN = "supersecrettoken123"

# Sample database of capitals and timezones
CITY_TIMEZONES = {
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "Washington": "America/New_York",
    "London": "Europe/London",
    "Delhi": "Asia/Kolkata"
}

# Token validator
def token_required(f):
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if auth.startswith("Bearer ") and auth.split(" ")[1] == API_TOKEN:
            return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/api/time", methods=["GET"])
@token_required
def get_time():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Missing 'city' parameter"}), 400

    timezone_name = CITY_TIMEZONES.get(city)
    if not timezone_name:
        return jsonify({"error": f"City '{city}' not found in the database."}), 404

    tz = pytz.timezone(timezone_name)
    now = datetime.now(tz)
    return jsonify({
        "city": city,
        "local_time": now.isoformat(),
        "utc_offset": now.strftime('%z')[:3] + ":" + now.strftime('%z')[3:]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
