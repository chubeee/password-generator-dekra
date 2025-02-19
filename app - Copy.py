from flask import Flask, render_template, request, send_file
import secrets
import string
import xml.etree.ElementTree as ET
import traceback
from io import BytesIO

app = Flask(__name__)

def generate_password(length=12, use_upper=True, use_numbers=True, use_special=True):
    characters = string.ascii_lowercase  # Default: only lowercase letters
    
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
        return render_template("index.html")
    except Exception as e:
        print("ERROR loading template:", e)
        print(traceback.format_exc())
        return "Internal Server Error - Template Not Found", 500

@app.route("/generate", methods=["POST"])
def generate():
    try:
        print("Incoming request:", request.form)  # Debugging input data

        num_passwords = request.form.get("num_passwords")
        if not num_passwords:
            print("MISSING num_passwords in request!")
            return "Bad Request: num_passwords is required", 400
        
        num_passwords = int(num_passwords)
        print(f"Generating {num_passwords} passwords...")

        root = ET.Element("Passwords")
        for _ in range(min(num_passwords, 10)):  # Max 10 passwords
            entry = ET.SubElement(root, "Entry")
            ET.SubElement(entry, "Password").text = generate_password()

        # Store XML in memory instead of writing to a file
        xml_io = BytesIO()
        tree = ET.ElementTree(root)

        print("Writing XML to memory...")
        tree.write(xml_io, encoding="utf-8", xml_declaration=True)
        xml_io.seek(0)  # Reset buffer position

        print("Sending XML file...")
        return send_file(xml_io, as_attachment=True, download_name="passwords.xml", mimetype="application/xml")

    except Exception as e:
        print("ERROR in /generate:", e)
        print(traceback.format_exc())
        return f"Internal Server Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
