from flask import Flask, render_template, request, jsonify, Response, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from ultralytics import YOLO
import os
from PIL import Image
import json
import cv2
import numpy as np
from threading import Thread
import sqlite3
from models import User, init_db

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Changez ceci par une clé secrète forte

# Initialisation de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Initialisation des bases de données
init_db()  # Initialise la base de données des utilisateurs

model = YOLO("best.pt")  # Ton modèle YOLOv8 classification
with open("class_descriptions.json", "r", encoding='utf-8') as f:
    class_info = json.load(f)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables for camera
camera = None
camera_thread = None
frame = None
stop_thread = False
last_prediction = None
last_confidence = None

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect('collection.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS discovered_signs
                 (sign_name TEXT PRIMARY KEY, found INTEGER)''')
    
    # Initialiser la table avec tous les panneaux
    for sign_name in class_info.keys():
        c.execute('INSERT OR IGNORE INTO discovered_signs (sign_name, found) VALUES (?, 0)',
                 (sign_name,))
    
    conn.commit()
    conn.close()

init_db()

def generate_frames():
    global camera, frame, stop_thread, last_prediction, last_confidence
    while not stop_thread:
        if camera is not None:
            try:
                success, frame = camera.read()
                if not success:
                    print("Erreur: Impossible de lire la caméra")
                    stop_camera()  # Arrêter la caméra en cas d'erreur
                    break
                else:
                    # Process frame with YOLO
                    try:
                        results = model(frame)
                        annotated_frame = results[0].plot()
                        
                        # Store prediction results
                        class_id = int(results[0].probs.top1)
                        last_prediction = results[0].names[class_id]
                        last_confidence = float(results[0].probs.top1conf)
                        
                        # Marquer le panneau comme trouvé
                        conn = sqlite3.connect('collection.db')
                        c = conn.cursor()
                        c.execute('UPDATE discovered_signs SET found = 1 WHERE sign_name = ?', (last_prediction,))
                        conn.commit()
                        conn.close()
                        
                        # Convert the frame to JPEG format
                        ret, buffer = cv2.imencode('.jpg', annotated_frame)
                        if not ret:
                            print("Erreur: Impossible d'encoder l'image")
                            continue
                        frame = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    except Exception as e:
                        print(f"Erreur lors du traitement de l'image: {str(e)}")
                        continue
            except Exception as e:
                print(f"Erreur générale de la caméra: {str(e)}")
                stop_camera()  # Arrêter la caméra en cas d'erreur
                break

def start_camera():
    global camera, stop_thread
    stop_thread = False
    try:
        # Vérifier d'abord si la caméra est déjà ouverte
        if camera is not None:
            print("La caméra est déjà ouverte")
            return True
            
        # Essayer d'ouvrir la caméra
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Ajout de CAP_DSHOW pour Windows
        if not camera.isOpened():
            print("Erreur: Impossible d'ouvrir la caméra")
            # Essayer avec un autre index de caméra
            camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
            if not camera.isOpened():
                print("Erreur: Impossible d'ouvrir la caméra avec aucun index")
                return False
        
        # Vérifier si la caméra peut lire des frames
        success, test_frame = camera.read()
        if not success:
            print("Erreur: La caméra ne peut pas lire de frames")
            camera.release()
            camera = None
            return False
            
        print("Caméra démarrée avec succès")
        return True
    except Exception as e:
        print(f"Erreur lors du démarrage de la caméra: {str(e)}")
        if camera is not None:
            camera.release()
            camera = None
        return False

def stop_camera():
    global camera, stop_thread
    stop_thread = True
    if camera is not None:
        try:
            camera.release()
            print("Caméra arrêtée avec succès")
        except Exception as e:
            print(f"Erreur lors de l'arrêt de la caméra: {str(e)}")
        camera = None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas')
            return redirect(url_for('signup'))
        
        try:
            user = User.create(username, password)
            login_user(user)
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Ce nom d\'utilisateur est déjà pris')
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera')
def start_camera_route():
    success = start_camera()
    if success:
        return jsonify({
            'status': 'success',
            'message': 'Caméra démarrée avec succès'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Impossible de démarrer la caméra. Vérifiez que votre caméra est connectée et non utilisée par une autre application.'
        }), 500

@app.route('/stop_camera')
def stop_camera_route():
    stop_camera()
    return jsonify({'status': 'Camera stopped'})

@app.route('/camera')
@login_required
def camera_page():
    return render_template('camera.html')

@app.route('/collection')
@login_required
def collection_page():
    return render_template('collection.html')

@app.route('/get_collection')
def get_collection():
    conn = sqlite3.connect('collection.db')
    c = conn.cursor()
    c.execute('SELECT sign_name, found FROM discovered_signs')
    signs = c.fetchall()
    conn.close()
    
    collection = []
    for sign_name, found in signs:
        collection.append({
            'name': sign_name,
            'description': class_info.get(sign_name, "Description non disponible."),
            'found': bool(found)
        })
    
    return jsonify({'signs': collection})

@app.route('/mark_sign_found', methods=['POST'])
def mark_sign_found():
    sign_name = request.json.get('sign_name')
    if sign_name:
        conn = sqlite3.connect('collection.db')
        c = conn.cursor()
        c.execute('UPDATE discovered_signs SET found = 1 WHERE sign_name = ?', (sign_name,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)

    results = model(img_path)
    class_id = int(results[0].probs.top1)
    class_name = results[0].names[class_id]
    confidence = float(results[0].probs.top1conf)

    # Marquer le panneau comme trouvé
    conn = sqlite3.connect('collection.db')
    c = conn.cursor()
    c.execute('UPDATE discovered_signs SET found = 1 WHERE sign_name = ?', (class_name,))
    conn.commit()
    conn.close()

    # Ajoutez ces lignes pour le débogage
    print("Class name from model:", class_name)
    print("Available keys in class_info:", class_info.keys())

    description = class_info.get(class_name, "Description not available.")

    response = jsonify({
        'prediction': class_name,
        'confidence': round(confidence * 100, 2),
        'description': description
    })
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/get_prediction')
def get_prediction():
    global last_prediction, last_confidence
    if last_prediction is None or last_confidence is None:
        return jsonify({
            'prediction': 'Aucune prédiction',
            'confidence': 0.0,
            'description': 'Aucune description disponible'
        })
    
    description = class_info.get(last_prediction, "Description non disponible.")
    
    return jsonify({
        'prediction': last_prediction,
        'confidence': last_confidence,
        'description': description
    })

if __name__ == '__main__':
    app.run(debug=True)
