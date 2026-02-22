from flask import Flask, render_template, request, redirect, jsonify, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies
)
import datetime
import cv2
from ultralytics import YOLO
from collections import Counter
import os
from werkzeug.utils import secure_filename
import json
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


app = Flask(__name__, static_url_path='/static')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
INSTANCE_FOLDER = os.path.join(BASE_DIR, 'instance')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(INSTANCE_FOLDER, exist_ok=True)
DB_PATH = os.path.join(INSTANCE_FOLDER, 'database.db')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SECRET_KEY'] = 'your_secret_key'
app.config["JWT_SECRET_KEY"] = "jwt_secret_key"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user')

    def __init__(self, name, email, password, role='user'):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def check_password(self, password):
        return self.password == password

with app.app_context():
    db.create_all()

import sqlite3

def ensure_role_column():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(user);")
    columns = [col[1] for col in cursor.fetchall()]
    if 'role' not in columns:
        print("[INFO] Adding missing 'role' column to 'user' table...")
        cursor.execute("ALTER TABLE user ADD COLUMN role TEXT DEFAULT 'user';")
        conn.commit()
        print("[INFO] Column 'role' added successfully ")
    conn.close()

ensure_role_column()


model = YOLO("yolov8n.pt")
camera = cv2.VideoCapture(0)
latest_counts = {}
detection_active = True

def annotate_image_from_results(img, results):
    if not (len(results) and hasattr(results[0].boxes, "xyxy")):
        return img
    for box, cls, conf in zip(results[0].boxes.xyxy, results[0].boxes.cls, results[0].boxes.conf):
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls)]
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 200, 0), 2)
        cv2.putText(img, label, (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 0), 2)
    return img

def detect_on_frame(frame):
    return model.predict(frame, verbose=False)

def gen_frames():
    global latest_counts, detection_active
    while True:
        success, frame = camera.read()
        if not success:
            break
        if detection_active:
            results = detect_on_frame(frame)
            if len(results) and hasattr(results[0].boxes, "cls"):
                labels = [model.names[int(cls)] for cls in results[0].boxes.cls.tolist()]
                latest_counts = Counter(labels)
            else:
                latest_counts = {}
            frame = annotate_image_from_results(frame, results)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/')
def home():
    return redirect('/login4')

@app.route('/register4', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'user')  
        if User.query.filter_by(email=email).first():
            return render_template('register4.html', error="Email already registered!")
        new_user = User(name, email, password, role)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login4')
    return render_template('register4.html')

@app.route('/login4', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(
                identity=user.email,
                additional_claims={'name': user.name, 'role': user.role},
                expires_delta=datetime.timedelta(hours=8)
            )
            response = redirect('/dashboard')
            set_access_cookies(response, access_token)
            return response
        else:
            return render_template('login4.html', error="Invalid email or password!")
    return render_template('login4.html')

@app.route('/logout')
def logout():
    response = redirect('/login4')
    unset_jwt_cookies(response)
    return response

@app.route('/dashboard')
@jwt_required()
def dashboard():
    current_user_email = get_jwt_identity()
    claims = get_jwt()
    user = {"name": claims.get("name"), "email": current_user_email, "role": claims.get("role")}
    return render_template('dashboard4.html', user=user)


@app.route('/admin')
@jwt_required()
def admin_panel():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return redirect('/dashboard')
    users = User.query.all()
    return render_template('admin.html', users=users, user=claims)

@app.route('/admin/promote', methods=['POST'])
@jwt_required()
def admin_promote():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({'status':'fail','message':'only admin'}), 403
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'status':'fail','message':'user not found'}), 404
    user.role = 'admin'
    db.session.commit()
    return jsonify({'status':'success'})

@app.route('/admin/demote', methods=['POST'])
@jwt_required()
def admin_demote():
    claims = get_jwt()
    if Mathjax.get("role") != "admin":
        return jsonify({'status':'fail','message':'only admin'}), 403
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'status':'fail','message':'user not found'}), 404
    user.role = 'user'
    db.session.commit()
    return jsonify({'status':'success'})

@app.route('/admin/delete', methods=['POST'])
@jwt_required()
def admin_delete():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({'status':'fail','message':'only admin'}), 403
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'status':'fail','message':'user not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status':'success'})


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_counts')
def get_counts():
    global latest_counts
    people_count = latest_counts.get('person', 0)
    return jsonify({
        'count': people_count,
        'details': dict(latest_counts)
    })

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global detection_active
    detection_active = True
    return jsonify({'status': 'success', 'message': 'Detection started'})

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    global detection_active
    detection_active = False
    return jsonify({'status': 'success', 'message': 'Detection stopped'})

@app.route('/capture', methods=['POST'])
def capture():
    success, frame = camera.read()
    if not success:
        return jsonify({'status': 'fail', 'message': 'Camera not accessible'})
    results = detect_on_frame(frame)
    frame = annotate_image_from_results(frame, results)
    filename = f"capture_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    cv2.imwrite(filepath, frame)
    counts = Counter([model.names[int(cls)] for cls in results[0].boxes.cls.tolist()]) if len(results) else {}
    return jsonify({'status': 'success', 'image_url': f"/static/uploads/{filename}", 'counts': dict(counts)})


@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
              
        return jsonify({'status': 'fail', 'message': 'No image uploaded'})
    file = request.files['image']
    if file.filename == '':
        return jsonify({'status': 'fail', 'message': 'No selected file'})
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    img = cv2.imread(filepath)
    results = detect_on_frame(img)
    img = annotate_image_from_results(img, results)
    out_path = os.path.join(app.config['UPLOAD_FOLDER'], 'det_' + filename)
    cv2.imwrite(out_path, img)
    counts = Counter([model.names[int(cls)] for cls in results[0].boxes.cls.tolist()]) if len(results) else {}


    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'last_image_counts.json')
    with open(save_path, 'w') as f:
         json.dump(counts, f)

    return jsonify({
    'status': 'success',
    'image_url': f"/static/uploads/det_{filename}",
    'counts': dict(counts)
})


@app.route('/api/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'status': 'fail', 'message': 'No video uploaded'})
    file = request.files['video']
    if file.filename == '':
        return jsonify({'status': 'fail', 'message': 'No selected file'})
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        return jsonify({'status': 'fail', 'message': 'Unable to open uploaded video'})
    fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'det_' + os.path.splitext(filename)[0] + ".mp4")
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_path = output_path.replace(".mp4", ".avi")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    counts = Counter()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = detect_on_frame(frame)
        frame = annotate_image_from_results(frame, results)
        out.write(frame)
        if len(results) and hasattr(results[0].boxes, "cls"):
            labels = [model.names[int(cls)] for cls in results[0].boxes.cls.tolist()]
            counts.update(labels)
    cap.release()
    out.release()
    cv2.destroyAllWindows()


    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'last_video_counts.json')
    with open(save_path, 'w') as f:
        json.dump(counts, f)

    return jsonify({
    'status': 'success',
    'video_url': f"/static/uploads/{os.path.basename(output_path)}",
    'counts': dict(counts)
})



@app.route('/api/users')
@jwt_required()
def api_users():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify([])  
    users = User.query.all()
    out = [{'id': u.id, 'name': u.name, 'email': u.email, 'role': u.role} for u in users]
    return jsonify(out)

@app.route('/api/user_status')
@jwt_required()
def api_user_status():
    
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error':'not found'}), 404

    return jsonify({
        'email': user.email,
        'name': user.name,
        'last_seen': datetime.datetime.utcnow().isoformat(),
        'last_count': latest_counts.get('person', 0),
        'details': dict(latest_counts)
    })

@app.route('/api/safe_zones', methods=['POST'])
@jwt_required()
def api_safe_zones():
    
    payload = request.get_json() or {}
    zones = payload.get('zones', [])
    zones_file = os.path.join(INSTANCE_FOLDER, 'safe_zones.json')
    with open(zones_file, 'w') as f:
        json.dump(zones, f)
    return jsonify({'status':'saved'})

@app.route('/api/get_safe_zones')
@jwt_required()
def api_get_safe_zones():
    zones_file = os.path.join(INSTANCE_FOLDER, 'safe_zones.json')
    if os.path.exists(zones_file):
        with open(zones_file, 'r') as f:
            zones = json.load(f)
    else:
        zones = []
    return jsonify({'zones': zones})
@app.route('/download_report')
@jwt_required()
def download_report():
    claims = get_jwt()
    role = claims.get("role")

    
    if role != "admin":
        return "Access denied: Only admin can download reports!", 403

    mode = request.args.get('mode', 'live')

    if mode == 'live':
        counts = latest_counts
    elif mode == 'image':
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'last_image_counts.json')
        counts = json.load(open(path)) if os.path.exists(path) else {}
    elif mode == 'video':
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'last_video_counts.json')
        counts = json.load(open(path)) if os.path.exists(path) else {}
    else:
        counts = {}

    people_count = counts.get('person', 0)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, height - 60, f"{mode.capitalize()} Crowd Report")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100,
                 f"Generated On: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(50, height - 130, f"Total People Count: {people_count}")

    y = height - 160
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Detected Objects:")
    p.setFont("Helvetica", 12)

    for k, v in counts.items():
        y -= 20
        p.drawString(70, y, f"- {k}: {v}")

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{mode}_crowd_report.pdf",
        mimetype='application/pdf'
    )




if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        if camera.isOpened():
            camera.release()
        cv2.destroyAllWindows()
