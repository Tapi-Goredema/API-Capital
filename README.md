API‑Capital

This small Flask API returns the local time in a given world city. It requires a Bearer token for authentication.

1) Deployment details

Public IP & Port: 34.60.216.82:5001

Endpoint Path: /api/time

2) How to call your API
Curl: curl -H "Authorization: Bearer supersecrettoken123" \
     "http://34.60.216.82:5001/api/time?city=Paris"
Response: {
  "city": "Paris",
  "local_time": "2025-04-22T04:06:01.551455+02:00",
  "utc_offset": "+02:00"
}

Browsers by default will only use ports 80 or 443 if no port is specified. Since the Flask dev server runs on 5001, http://34.60.216.82 will refuse connection.

Even if you manually enter http://34.60.216.82:5001/api/time?city=Paris, browsers don’t let you add custom headers via the URL bar, so you’ll get:
{ "error": "Unauthorized" }

If you need to show results directly in a browser, you can temporarily disable the token check in app.py:
- token = request.headers.get("Authorization", "").split()[-1]
- if token != "supersecrettoken123":
-     return jsonify({"error": "Unauthorized"}), 401

Then restart the app and visit in your browser:
http://34.60.216.82:5001/api/time?city=Paris
