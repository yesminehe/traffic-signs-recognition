# Traffic Signs Recognition System

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
   git clone https://github.com/yourusername/traffic-signs-recognition.git
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
- `GET /video_feed` - Camera video stream
- `GET /collection` - User's sign collection
- `GET /get_collection` - Get collection data (JSON)
- `POST /predict` - Upload image for prediction
- `GET /get_prediction` - Get latest prediction results

## Database Schema

### Users Table

- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password

### Discovered Signs Table

- `sign_name`: Traffic sign name (primary key)
- `found`: Boolean indicating if sign was discovered

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Camera Issues

- Make sure your webcam is connected and not being used by another application
- Try different camera indices (0, 1, 2) in the `start_camera()` function
- Check if your browser allows camera access

### Model Issues

- Ensure the `best.pt` model file is in the root directory
- Verify the model is compatible with the current YOLOv8 version

### Database Issues

- The application automatically creates SQLite databases on first run
- If you encounter database errors, delete the `.db` files and restart

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) for the object detection framework
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [OpenCV](https://opencv.org/) for computer vision capabilities

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/traffic-signs-recognition](https://github.com/yourusername/traffic-signs-recognition)
