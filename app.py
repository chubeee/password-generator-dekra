from flask import Flask, render_template, request, send_file
import secrets
import string
import xml.etree.ElementTree as ET
from io import BytesIO

app = Flask(__name__)

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        num_passwords = int(request.form.get("num_passwords", 1))
        root = ET.Element("Passwords")

        for _ in range(min(num_passwords, 10)):  # Max 10 passwords
            entry = ET.SubElement(root, "Entry")
            ET.SubElement(entry, "Password").text = generate_password()

        xml_io = BytesIO()
        tree = ET.ElementTree(root)
        tree.write(xml_io, encoding="utf-8", xml_declaration=True)
        xml_io.seek(0)

        return send_file(xml_io, as_attachment=True, download_name="passwords.xml", mimetype="application/xml")

    except Exception as e:
        print("Error:", e)
        print(traceback.format_exc())
        return "Internal Server Error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
