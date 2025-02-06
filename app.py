from flask import Flask, request, jsonify, Response
import smtplib
from email.mime.text import MIMEText
import os
import json  # ✅ Import JSON library to modify output format

app = Flask(__name__)

# ✅ Use environment variables to protect login credentials
SMTP_SERVER = "smtp.zoho.com"
SMTP_PORT = 587
ZOHO_USER = os.getenv("ZOHO_USER")  # Must be set in environment variables
ZOHO_PASSWORD = os.getenv("ZOHO_PASSWORD")  # Must be set in environment variables

# ✅ Custom function to return JSON without Unicode conversion
def custom_jsonify(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False),  # ✅ Preserve Arabic language
        status=status,
        mimetype="application/json"
    )

@app.route("/", methods=["GET"])
def home():
    return custom_jsonify({"message": "✅ API is working successfully!"})

@app.route("/send-email", methods=["POST"])
def send_email():
    print("📩 Received request method:", request.method)  # ✅ Print request type for debugging

    # ✅ Ensure request is in JSON format
    if not request.is_json:
        return custom_jsonify({"status": "error", "message": "⚠ The request must be in JSON format!"}, 400)

    data = request.get_json()
    to_email = data.get("to_email")
    subject = data.get("subject", "Zoho Test")
    content = data.get("content", "This is the email content.")

    # ✅ Ensure login credentials are available
    if not ZOHO_USER or not ZOHO_PASSWORD:
        return custom_jsonify({"status": "error", "message": "⚠ SMTP credentials are not available!"}, 500)

    if not to_email:
        return custom_jsonify({"status": "error", "message": "⚠ Recipient email is required!"}, 400)

    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = ZOHO_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(ZOHO_USER, ZOHO_PASSWORD)
        server.sendmail(ZOHO_USER, to_email, msg.as_string())
        server.quit()
        return custom_jsonify({"status": "success", "message": "✅ Email sent successfully!"})
    except Exception as e:
        return custom_jsonify({"status": "error", "message": f"❌ Sending error: {str(e)}"}, 500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ Use an environment port if available
    app.run(host="0.0.0.0", port=port, debug=True)  # ✅ Run Flask in debug mode
