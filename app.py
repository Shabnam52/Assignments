from flask import Flask, jsonify, request
import mysql.connector
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Add the db_config, conn, and cursor here
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Shab@0052',
    'database': 'resume'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

# API Endpoint to fetch employee details by employee_id
@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    query = 'SELECT * FROM Employees WHERE id = %s'
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()
    if employee:
        return jsonify(employee)
    return jsonify(error='Employee not found'), 404

# API Endpoint to fetch project details by project_id
@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    query = 'SELECT * FROM Projects WHERE project_id = %s'
    cursor.execute(query, (project_id,))
    project = cursor.fetchone()
    if project:
        return jsonify(project)
    return jsonify(error='Project not found'), 404

# Function to generate resume content
def generate_resume(employee):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(50, 750, f"Resume for {employee['name']}")
    c.drawString(50, 720, f"Designation: {employee['designation']}")
    c.drawString(50, 690, "Professional Summary:")
    c.drawString(50, 670, employee['summary'])
    c.drawString(50, 640, "Technical Skills:")
    c.drawString(50, 620, employee['technical_skills'])
    c.save()
    buffer.seek(0)
    return buffer

# API Endpoint to generate and download resume as PDF
@app.route('/api/resume/<int:employee_id>', methods=['GET'])
def download_resume(employee_id):
    query = 'SELECT * FROM Employees WHERE id = %s'
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()
    if employee:
        pdf_buffer = generate_resume(employee)
        return pdf_buffer.getvalue(), 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'attachment; filename={employee["name"]}_resume.pdf'
        }
    return jsonify(error='Employee not found'), 404

if __name__ == '__main__':
    app.run()
