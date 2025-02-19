from flask import Flask, render_template, request, send_file
import secrets
import string
import xml.etree.ElementTree as ET
import traceback
from io import BytesIO

app = Flask(__name__)

def generate_password(length=12, use_upper=True, use_numbers=True, use_special=True):
    characters = string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.route("/")
def home():
    try:
        print("✅ / route accessed")  # Debugging
        return render_template("index.html")
    except Exception as e:
        print("❌ ERROR loading template:", e)
        print(traceback.format_exc())
        return "Internal Server Error - Template Not Found", 500

@app.route("/generate", methods=["POST"])
def generate():
    try:
        print("✅ /generate route accessed")
        num_passwords = int(request.form.get("num_passwords", 1))
        password_length = int(request.form.get("password_length", 12))
        use_upper = "use_uppercase" in request.form
        use_numbers = "use_numbers" in request.form
        use_special = "use_special" in request.form

        root = ET.Element("Passwords")
        for _ in range(min(num_passwords, 50)):  
            entry = ET.SubElement(root, "Entry")
            ET.SubElement(entry, "Password").text = generate_password(
                length=password_length, 
                use_upper=use_upper, 
                use_numbers=use_numbers, 
                use_special=use_special
            )

        xml_io = BytesIO()
        tree = ET.ElementTree(root)
        tree.write(xml_io, encoding="utf-8", xml_declaration=True)
        xml_io.seek(0)

        return send_file(xml_io, as_attachment=True, download_name="passwords.xml", mimetype="application/xml")

    except Exception as e:
        print("❌ ERROR in /generate:", e)
        print(traceback.format_exc())
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
