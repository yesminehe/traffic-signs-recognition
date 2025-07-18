# Traffic Signs Recognition System

![YOLOv8](https://img.shields.io/badge/YOLOv8-Used-blue?logo=python)

A Flask web application that uses YOLOv8 to recognize and classify traffic signs in real-time using your computer's camera. The application includes user authentication, a collection system to track discovered signs, and a web interface for easy interaction.

## Features

- 🔐 **User Authentication**: Secure login and registration system
- 📷 **Real-time Camera Recognition**: Live traffic sign detection using your webcam
- 🎯 **YOLOv8 Integration**: Advanced object detection and classification
- 📊 **Collection System**: Track and display discovered traffic signs
- 🌐 **Web Interface**: User-friendly Flask web application
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Screenshots

_Add screenshots of your application here_

## Prerequisites

Before running this application, make sure you have:

- Python 3.7 or higher
- A webcam for real-time recognition
- Git (for cloning the repository)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yesminehe/traffic-signs-recognition.git
   cd traffic-signs-recognition
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**

   **Windows:**

   ```bash
   .venv\Scripts\activate
   ```

   **macOS/Linux:**

   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Download the YOLO model**

   You'll need to obtain the `best.pt` model file. This should be placed in the root directory of the project.

## Usage

1. **Start the application**

   ```bash
   python app.py
   ```

2. **Open your web browser**
   Navigate to `http://localhost:5000`

3. **Create an account or login**

   - Register a new account or use existing credentials
   - The system will redirect you to the main dashboard

4. **Use the camera recognition**

   - Click on the camera section to start real-time recognition
   - Point your camera at traffic signs to detect and classify them
   - Discovered signs are automatically added to your collection

5. **View your collection**
   - Check the collection page to see all discovered traffic signs
   - Track your progress in finding different types of signs

## Project Structure

```
traffic-signs-recognition/
├── app.py                 # Main Flask application
├── models.py              # User authentication models
├── requirements.txt       # Python dependencies
├── class_descriptions.json # Traffic sign class descriptions
├── best.pt               # YOLOv8 trained model (not included)
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── ...
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── uploads/
└── README.md
```

## Configuration

### Environment Variables

You can set the following environment variables:

- `SECRET_KEY`: Flask secret key for session management
- `DEBUG`: Set to `True` for development mode

### Model Configuration

The application uses a YOLOv8 model trained on traffic sign datasets. The model file (`best.pt`) should be placed in the root directory.

## API Endpoints

- `GET /` - Main dashboard (requires authentication)
- `GET /login` - Login page
- `POST /login` - Login form submission
- `GET /signup` - Registration page
- `POST /signup` - Registration form submission
- `GET /logout` - Logout user
- `GET /camera` - Camera recognition page
- `POST /start_camera` - Start camera stream
- `POST /stop_camera` - Stop camera stream
- `GET /video_feed`
