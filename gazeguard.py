import face_recognition
import cv2
import numpy as np
import os
import pandas as pd
from datetime import datetime
from openpyxl import Workbook, load_workbook

# Folder to store known face photos
photos_folder = "gazeguard_photos"
attendance_folder = "gazeguard_attendance"

# Check if the photos folder exists, if not, create it
if not os.path.exists(photos_folder):
    os.makedirs(photos_folder)
    print(f"'{photos_folder}' folder created. Please add photos of known faces to this folder and run the program again.")
    exit()

# Check if the attendance folder exists, if not, create it
if not os.path.exists(attendance_folder):
    os.makedirs(attendance_folder)

# Get current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Create the attendance file path
attendance_file = os.path.join(attendance_folder, f'{current_date}.xlsx')

# Load all images from the folder and encode them
known_face_encodings = []
known_face_names = []

for filename in os.listdir(photos_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(photos_folder, filename)
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])  # Use filename without extension as the name

# Create a DataFrame for attendance
attendance_df = pd.DataFrame({
    'Name': known_face_names,
    'Time of Arrival': [''] * len(known_face_names),
    'Status': ['Absent'] * len(known_face_names)
})

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
recorded_names = set()

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
    if not ret:
        print("Failed to capture video. Exiting...")
        break

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            
            # Record attendance if not already recorded
            if name != "Unknown" and name not in recorded_names:
                recorded_names.add(name)
                arrival_time = datetime.now().strftime('%H:%M:%S')
                attendance_df.loc[attendance_df['Name'] == name, 'Time of Arrival'] = arrival_time
                attendance_df.loc[attendance_df['Name'] == name, 'Status'] = 'Present'

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # End program if window is closed or 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

# Create summary
total_students = len(attendance_df)
present_students = attendance_df[attendance_df['Status'] == 'Present']['Name'].tolist()
absent_students = attendance_df[attendance_df['Status'] == 'Absent']['Name'].tolist()

summary_data = {
    'Total Students': [total_students],
    'Present Students': [len(present_students)],
    'Absent Students': [len(absent_students)],
    'Present Student Names': [', '.join(present_students)],
    'Absent Student Names': [', '.join(absent_students)]
}

summary_df = pd.DataFrame(summary_data)

# Save the attendance DataFrame and summary to Excel file
with pd.ExcelWriter(attendance_file, engine='openpyxl') as writer:
    attendance_df.to_excel(writer, sheet_name='Attendance', index=False)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)

print("Program has finished running. Please add more photos to the 'gazeguard_photos' folder if needed.")
