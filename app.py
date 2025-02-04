from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# ✅ استخدم متغيرات البيئة لتخزين البيانات الحساسة
SMTP_SERVER = "smtp.zoho.com"
SMTP_PORT = 587
ZOHO_USER = os.getenv("ZOHO_EMAIL")  # ✅ يتم تخزينه في Render
ZOHO_PASSWORD = os.getenv("ZOHO_PASSWORD")  # ✅ يتم تخزينه في Render

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    to_email = data.get("to_email", "recipient@example.com")
    subject = data.get("subject", "اختبار Zoho")
    content = data.get("content", "هذا هو محتوى البريد الإلكتروني.")

    if not ZOHO_USER or not ZOHO_PASSWORD:
        return jsonify({"status": "error", "message": "⚠ بيانات SMTP غير متوفرة في البيئة!"}), 500

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
        return jsonify({"status": "success", "message": "✅ تم إرسال البريد بنجاح!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ استخدام منفذ Render
    app.run(host="0.0.0.0", port=port)
