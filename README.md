# Face_Attendance

## Overview
This project is a Face Attendance System designed to automate the process of taking attendance using facial recognition technology. The system captures images from a webcam, detects faces, matches them with known faces, and retrieves student information from Firebase Realtime Database to update attendance records.

## Features
- **Facial Recognition**: Utilizes the face_recognition library to detect and recognize faces in captured frames.
- **Firebase Integration**: Retrieves student information such as name, branch, total attendance, standing, year, and starting year from Firebase Realtime Database.
- **Graphical User Interface (GUI)**: Displays student information overlaid on the captured frames for easy attendance tracking.
- **Multiple Modes**: Supports different modes (e.g., loading screen) with corresponding background images for a visually pleasing user experience.

## Installation
1. Clone the repository to your local machine:
git clone https://github.com/your-username/Face_Attendance.git
2. Install the required dependencies:
pip install -r requirements.txt

## Usage
1. Ensure that your system has a webcam connected and properly configured.
2. Run the `main.py` script:
python main.py

3. Follow the instructions provided by the GUI to perform various tasks such as adding users, taking attendance, etc.

## Dependencies
- Python 3.x
- OpenCV
- TensorFlow
- Numpy
- Pillow
- cvzone
- Firebase Admin

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
