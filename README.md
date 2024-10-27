# Python Face Recognition Attendance System

This repository contains a Python-based facial recognition attendance system. Using face recognition technology, this project captures and records attendance details into Excel files for each session. Developed with innovative machine learning techniques, this system offers accurate, real-time attendance tracking.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Example Code](#example-code)
- [Patent Information](#patent-information)
- [Contact](#contact)
- [Demonstration](#demonstration)

---

## Project Overview

The Python Face Recognition Attendance System is designed to:
1. Recognize faces in real time using the device's camera.
2. Record attendance and arrival times in an Excel sheet.
3. Generate daily attendance summaries for review.

This project features a smart and efficient face matching algorithm, optimizing attendance recording while securely storing data in Excel files.

---

## Technologies Used

- **Python Libraries**: `face_recognition`, `cv2` (OpenCV), `numpy`, `os`, `pandas`, `datetime`, and `openpyxl`
- **File Storage**: `gazeguard_photos` for known faces and `gazeguard_attendance` for daily Excel attendance records.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/face-recognition-attendance.git
    cd face-recognition-attendance
    ```
2. Install the required libraries:
    ```bash
    pip install face_recognition opencv-python numpy pandas openpyxl
    ```
3. Add images of known faces in the `gazeguard_photos` folder (create it if it doesn’t exist).

---

## Usage

1. Run the program:
    ```bash
    python main.py
    ```
2. The system will:
   - Capture live video.
   - Recognize faces and mark attendance in an Excel file under `gazeguard_attendance`.
3. End the program by closing the video window or pressing 'q'.

---

## Example Code
```python
import face_recognition
import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime
from openpyxl import Workbook, load_workbook

# Full code is available in the main.py file.
```
## Patent Information
Title: Facial Guard Smart Glasses for Secure Attendance Capture<br>
Patent Number: 202421016351 A<br>
Filed in: India<br>
Abstract: A smart glasses system for automated, secure attendance tracking in educational settings.<br> Integrates face recognition, machine learning, and AI for high accuracy, secure data handling, and real-time attendance insights.

## Contact
For more information, visit the inventor's LinkedIn profile: <a href="https://www.linkedin.com/posts/ashish-mali-312901254_startup-entrepreneurship-innovation-activity-7207603926068637696-CIs0?utm_source=share&utm_medium=member_desktop">Ashish Mali</a>  on LinkedIn.

## Demonstration
<img src="https://github.com/lmno3418/GazeGuard/blob/main/Demonstration/1.jpeg" alt="1">

<img src="https://github.com/lmno3418/GazeGuard/blob/main/Demonstration/2.jpeg" alt="2">

<img src="https://github.com/lmno3418/GazeGuard/blob/main/Demonstration/3.jpeg" alt="3">

<img src="https://github.com/lmno3418/GazeGuard/blob/main/Demonstration/4.jpeg" alt="4">
