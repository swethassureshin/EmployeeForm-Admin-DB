from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from openpyxl import Workbook
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

FILE_NAME = "employees.json"
UPLOAD_FOLDER = "uploads"

# -------------------------------
# Create files/folders if not exists
# -------------------------------
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w") as f:
        json.dump([], f)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------
# Add Employee (WITH FILE UPLOAD)
# -------------------------------
@app.route("/add-employee", methods=["POST"])
def add_employee():
    try:
        data = request.form.to_dict()

        # Safe timestamp (NO zoneinfo)
        data["date_submitted"] = datetime.now().strftime("%d %b %Y, %I:%M %p")

        # File upload
        file = request.files.get("idProof")
        if file and file.filename != "":
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            data["file_name"] = file.filename
        else:
            data["file_name"] = None

        # Load existing data
        with open(FILE_NAME, "r") as f:
            employees = json.load(f)

        employees.append(data)

        # Save back
        with open(FILE_NAME, "w") as f:
            json.dump(employees, f, indent=4)

        return jsonify({"message": "Employee added successfully"}), 200

    except Exception as e:
        print("SERVER ERROR:", e)
        return jsonify({"error": str(e)}), 500


# -------------------------------
# Get All Employees
# -------------------------------
@app.route("/employees", methods=["GET"])
def get_employees():
    try:
        with open(FILE_NAME, "r") as f:
            employees = json.load(f)
        return jsonify(employees)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# Serve Uploaded Files
# -------------------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# -------------------------------
# Export Excel
# -------------------------------
@app.route("/export-excel", methods=["GET"])
def export_excel():
    try:
        with open(FILE_NAME, "r") as f:
            employees = json.load(f)

        wb = Workbook()
        ws = wb.active
        ws.title = "Employees"

        # ✅ FIXED header (comma was missing before)
        ws.append([
            "Full Name",
            "Email",
            "Phone",
            "Address",
            "Employee ID",
            "Department",
            "Date of Joining",
            "Date of Birth",
            "Gender",
            "File Name"
        ])

        for emp in employees:
            ws.append([
                emp.get("full_name", ""),
                emp.get("email", ""),
                emp.get("phone", ""),
                emp.get("address", ""),
                emp.get("employee_id", ""),
                emp.get("department", ""),
                emp.get("date_of_joining", ""),
                emp.get("dob", ""),
                emp.get("gender", ""),
                emp.get("file_name", "")
            ])

        file_name = "employees.xlsx"
        wb.save(file_name)

        return send_file(file_name, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
