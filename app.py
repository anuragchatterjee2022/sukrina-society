from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from receipt_gen import generate_receipt
import os

app = Flask(__name__)
app.secret_key = "sukrina_secure_key"

# Database configuration
# Ensure it is 'URI' at the end, not 'PATH' or 'URL'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sukrina.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Table for Members
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flat_no = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Paid")

# Initialize database with a sample member
with app.app_context():
    db.create_all()
    if not Member.query.first():
        db.session.add(Member(flat_no="A-101", name="Anurag Chatterjee", status="Paid"))
        db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pay', methods=['POST'])
def pay():
    name = request.form.get('name')
    flat = request.form.get('flat')
    amount = request.form.get('amount')
    month = "February 2026"
    
    # Logic to generate PDF receipt
    pdf_filename = generate_receipt(name, flat, amount, month)
    return send_file(pdf_filename, as_attachment=True)

@app.route('/directory')
def directory():
    search = request.args.get('q', '')
    if search:
        members = Member.query.filter(Member.name.contains(search) | Member.flat_no.contains(search)).all()
    else:
        members = Member.query.all()
    return render_template('members.html', members=members)

if __name__ == '__main__':
    app.run(debug=True)