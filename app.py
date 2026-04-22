from flask import Flask, render_template, request, send_from_directory
import os, uuid, json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DB_FILE = 'database.json'

if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        file = request.files.get('file')
        pin = request.form.get('pin')
        if file and pin:
            db = load_db()
            file_id = str(uuid.uuid4())[:8]
            filename = file_id + "_" + file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            db[file_id] = {"pin": pin, "file": filename}
            save_db(db)
            return f"<h1>Muvaffaqiyatli!</h1><p>Link: <a href='/view/{file_id}'>http://127.0.0{file_id}</a></p><p>PIN: {pin}</p><a href='/admin'>Orqaga</a>"
    return '<h2>Admin: PDF Yuklash</h2><form method="post" enctype="multipart/form-data">Fayl: <input type="file" name="file"><br>PIN: <input type="text" name="pin" maxlength="4"><br><input type="submit" value="Yuklash"></form>'

@app.route('/view/<file_id>', methods=['GET', 'POST'])
def view(file_id):
    db = load_db()
    if file_id not in db: return "Fayl topilmadi!"
    if request.method == 'POST':
        p = request.form.get('p1','') + request.form.get('p2','') + request.form.get('p3','') + request.form.get('p4','')
        if p == db[file_id]['pin']:
            return send_from_directory(UPLOAD_FOLDER, db[file_id]['file'])
        return "<h1>PIN xato!</h1><a href='javascript:history.back()'>Orqaga</a>"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
