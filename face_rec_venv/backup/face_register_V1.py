import face_recognition
import cv2
from datetime import datetime, timedelta
import pickle
import numpy as np

# Global variables for known face data
known_face_encodings = []
known_face_metadata = []

def load_known_faces():
    global known_face_encodings, known_face_metadata

    try:
        with open("known_faces.dat", "rb") as face_data_file:
            known_face_encodings, known_face_metadata = pickle.load(face_data_file)
            print("Known faces loaded from disk.")
    except FileNotFoundError:
        print("No previous face data found - starting with a blank known face list.")
        pass

def lookup_known_face(face_encoding):
    '''Check if the given face matches any known faces.'''

    metadata = None
    if len(known_face_encodings) == 0:
        return metadata

    # Compare the face with known encodings
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)

    if face_distances[best_match_index] < 0.65:
        metadata = known_face_metadata[best_match_index]

        # Update metadata
        metadata["last_seen"] = datetime.now()
        metadata["seen_frames"] += 1
        if datetime.now() - metadata["first_seen_this_interaction"] > timedelta(minutes=5):
            metadata["first_seen_this_interaction"] = datetime.now()
            metadata["seen_count"] += 1

    return metadata

def draw_visitor_sidebar(frame, metadata):
    '''Draw the sidebar showing visitors at the top-left corner.'''
    sidebar_x = 10
    sidebar_y = 10
    sidebar_width = 300
    sidebar_height = 150  # Adjust this based on content
    sidebar_color = (200, 200, 200)
    
    # Draw sidebar background
    cv2.rectangle(frame, (sidebar_x, sidebar_y), (sidebar_x + sidebar_width, sidebar_y + sidebar_height), sidebar_color, -1)

    # Draw header text
    cv2.putText(frame, "Visitors at Door", (sidebar_x + 10, sidebar_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    if metadata:
        face_image = metadata["face_image"]
        face_name = metadata["face_name"]
        seen_count = metadata["seen_count"]

        # Insert the visitor's cropped face image
        face_image_resized = cv2.resize(face_image, (100, 100))
        frame[sidebar_y + 30:sidebar_y + 130, sidebar_x + 10:sidebar_x + 110] = face_image_resized

        # Display the visitor's name and visit count
        cv2.putText(frame, f"{face_name} - {seen_count} visits", (sidebar_x + 120, sidebar_y + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

def main_loop():
    '''Main loop to capture video and recognize faces in real-time.'''

    # Initialize the webcam or video source
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to grab frame.")
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Find all faces in the current frame
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        visitor_metadata = None  # Initialize for sidebar

        # Iterate over each detected face
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Check if the face is known
            metadata = lookup_known_face(face_encoding)

            top, right, bottom, left = [v * 4 for v in face_location]  # Scale face box back to original size

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 255), 2)

            if metadata:
                visitor_metadata = metadata  # Set for sidebar
                elapsed_time = int((datetime.now() - metadata["last_seen"]).total_seconds())
                cv2.putText(frame, f"At door {elapsed_time}s", (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

        # Draw the visitor sidebar
        draw_visitor_sidebar(frame, visitor_metadata)

        # Display the resulting imagef
        cv2.imshow("Video", frame)

        # Press 'q' to quit the video loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    load_known_faces()  # Load faces from the previous session
    main_loop()  # Start the main video loop