from flask import Flask, request, jsonify, Response
import smtplib
from email.mime.text import MIMEText
import os
import json  # ✅ استيراد مكتبة JSON لتعديل طريقة الإخراج

app = Flask(__name__)

# ✅ استخدم متغيرات البيئة لحماية بيانات تسجيل الدخول
SMTP_SERVER = "smtp.zoho.com"
SMTP_PORT = 587
ZOHO_USER = os.getenv("brono0day@zohomail.com")  # يجب ضبطه في متغيرات البيئة
ZOHO_PASSWORD = os.getenv("ilyas.2020")  # يجب ضبطه في متغيرات البيئة

# ✅ دالة مخصصة لإرجاع JSON بدون تحويل Unicode
def custom_jsonify(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False),  # ✅ الحفاظ على اللغة العربية
        status=status,
        mimetype="application/json"
    )

@app.route("/", methods=["GET"])
def home():
    return custom_jsonify({"message": "✅ API تعمل بنجاح!"})

@app.route("/send-email", methods=["POST"])
def send_email():
    print("📩 Received request method:", request.method)  # ✅ طباعة نوع الطلب لفحصه

    # ✅ التحقق من أن الطلب بصيغة JSON
    if not request.is_json:
        return custom_jsonify({"status": "error", "message": "⚠ يجب إرسال الطلب بصيغة JSON!"}, 400)

    data = request.get_json()
    to_email = data.get("to_email")
    subject = data.get("subject", "اختبار Zoho")
    content = data.get("content", "هذا هو محتوى البريد الإلكتروني.")

    # ✅ التأكد من توفر بيانات تسجيل الدخول
    if not ZOHO_USER or not ZOHO_PASSWORD:
        return custom_jsonify({"status": "error", "message": "⚠ بيانات SMTP غير متوفرة!"}, 500)

    if not to_email:
        return custom_jsonify({"status": "error", "message": "⚠ البريد الإلكتروني للمستلم مطلوب!"}, 400)

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
        return custom_jsonify({"status": "success", "message": "✅ تم إرسال البريد بنجاح!"})
    except Exception as e:
        return custom_jsonify({"status": "error", "message": f"❌ خطأ في الإرسال: {str(e)}"}, 500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ استخدام منفذ بيئي إذا كان متاحًا
    app.run(host="0.0.0.0", port=port, debug=True)  # ✅ تشغيل Flask في وضع التصحيح
