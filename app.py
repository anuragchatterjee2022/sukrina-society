import os
import base64
import requests
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from receipt_gen import generate_receipt

app = Flask(__name__)
app.secret_key = "sukrina_secure_key"

# --- CONFIGURATION ---
# Replace with your actual GitHub token
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = "anuragchatterjee2022/sukrina-society"
# ---------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sukrina.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flat_no = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="Paid")

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    notices = Notice.query.all()
    # Automatically scans the folder to show all uploaded PDFs
    docs_path = 'static/docs'
    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
    all_files = os.listdir(docs_path)
    pdf_files = [f for f in all_files if f.endswith('.pdf')]
    return render_template('index.html', notices=notices, pdf_files=pdf_files)

@app.route('/upload-to-github', methods=['POST'])
def upload_to_github():
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        # 1. Save locally for instant visibility
        local_path = os.path.join('static/docs', file.filename)
        file.save(local_path)
        
        # 2. Push to GitHub for permanent storage
        file.seek(0)
        content = base64.b64encode(file.read()).decode()
        url = f"https://api.github.com/repos/{REPO_NAME}/contents/static/docs/{file.filename}"
        data = {"message": f"Upload: {file.filename}", "content": content, "branch": "main"}
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        requests.put(url, json=data, headers=headers)
        
    return redirect(url_for('home'))

@app.route('/add-notice', methods=['POST'])
def add_notice():
    content = request.form.get('notice')
    if content:
        db.session.add(Notice(content=content))
        db.session.commit()
    return redirect(url_for('home'))

# FIXED: Added the missing route to resolve BuildError
# Updated Deletion for Text Notices
@app.route('/delete-notice/<int:id>')
def delete_notice(id):
    notice = Notice.query.get(id)
    if notice:
        db.session.delete(notice)
        db.session.commit()
    # Stays on the Dashboard section
    return redirect(url_for('home', _anchor='home-view'))

# Updated Deletion for PDF Files
@app.route('/delete-pdf/<filename>')
def delete_pdf(filename):
    file_path = os.path.join('static/docs', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    # Stays on the Documents section
    return redirect(url_for('home', _anchor='docs-view'))
        
    return redirect(url_for('home'))

@app.route('/pay', methods=['POST'])
def pay():
    # Fetching data from the frontend form
    name = request.form.get('name')
    flat = request.form.get('flat')
    amount = request.form.get('amount')
    
    # Call the fixed generator
    # We pass "February 2026" as the default month for this deployment
    pdf_filename = generate_receipt(name, flat, amount, "February 2026")
    
    # Send file to user for download
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