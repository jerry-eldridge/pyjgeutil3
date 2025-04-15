# Requirements:
# pip install opencv-python mediapipe numpy

import cv2
import mediapipe as mp # Python 312, not yet in 313.
import numpy as np
import math

root = f"./imgs/"

##########################################
# [1] Google Gemini 2.5 Pro, a large language model
#

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5)

# --- Configuration ---
# You might need to change the camera index
#if 0 is not your default webcam
CAMERA_INDEX = 0

# Choose landmarks for waist width estimation
# (Hips are often used)
# Options: LEFT_HIP, RIGHT_HIP, LEFT_SHOULDER,
# RIGHT_SHOULDER
# Using hips provides a reference width in the
#lower torso area.
LEFT_LANDMARK = mp_pose.PoseLandmark.LEFT_HIP
RIGHT_LANDMARK = mp_pose.PoseLandmark.RIGHT_HIP
# --- End Configuration ---

#Gets pixel coordinates for a specific landmark.
def get_landmark_coords(landmarks, landmark_enum,
                        image_shape):
    if landmarks:
        try:
            landmark = landmarks.landmark[landmark_enum]
            # Check visibility - landmarks might
            #be detected but estimated as not visible
            if landmark.visibility < 0.5:
                # Adjust threshold if needed
                 return None
            # Convert normalized coordinates
            #(0.0 - 1.0) to pixel coordinates
            img_h, img_w = image_shape[:2]
            x = int(landmark.x * img_w)
            y = int(landmark.y * img_h)
            return (x, y)
        except IndexError:
            return None
    return None

# Start video capture
cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print(f"Error: Could not open video source "+\
          f"{CAMERA_INDEX}.")
    exit()

print("Starting video stream. Press 'q' to quit.")

n = 0
flag = False
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later
    # selfie-view display
    # Also convert the BGR image to RGB before
    # processing
    image = cv2.cvtColor(cv2.flip(image, 1),
                         cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    # Performance optimization

    # Process the image and find pose landmarks
    results = pose.process(image)

    # Prepare image for drawing (convert back to
    # BGR and allow writing)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    pixel_width_text = f"Pixel Width: N/A - {flag}"
    pixel_width = None

    # Extract landmarks if detected
    if results.pose_landmarks:
        img_h, img_w = image.shape[:2]

        # Get coordinates for the chosen landmarks
        left_coord = get_landmark_coords(\
            results.pose_landmarks, LEFT_LANDMARK,\
            image.shape)
        right_coord = get_landmark_coords(\
            results.pose_landmarks, RIGHT_LANDMARK,\
            image.shape)

        # Draw the pose annotation on the image.
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=\
                mp_drawing.DrawingSpec(\
                    color=(245,117,66), \
                    thickness=2, circle_radius=2),
            connection_drawing_spec=\
                mp_drawing.DrawingSpec(\
                    color=(245,66,230), \
                    thickness=2, circle_radius=2))

        # Calculate and display pixel distance if both landmarks are visible
        if left_coord and right_coord:
            # Calculate Euclidean distance
            pixel_width = math.sqrt(\
                (left_coord[0] - right_coord[0])**2 + \
                (left_coord[1] - right_coord[1])**2)
            pixel_width_text = \
                f"Pixel Width: {pixel_width:.2f} px"

            # Draw line between landmarks for visualization
            cv2.line(image, left_coord, right_coord, (0, 255, 0), 2)
            # Put landmark coordinates text
            cv2.putText(image,
                f'L({left_coord[0]},{left_coord[1]})',
                (left_coord[0]-80, left_coord[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(image,
                f'R({right_coord[0]},{right_coord[1]})',
                (right_coord[0]+10, right_coord[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                0, 0, 255), 1, cv2.LINE_AA)


    # Display the pixel width calculation
    cv2.putText(image, pixel_width_text, (10, 30), \
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), \
        2, cv2.LINE_AA)
    cv2.putText(image,
        "NOTE: This is PIXEL width, NOT real-world "+\
        "size or circumference.", (10, 60), \
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), \
        1, cv2.LINE_AA)


    # Display the resulting frame
    cv2.imshow(f"MediaPipe Pose - Waist Width"+\
        " Estimation (Pixels)", image)
    if n % 5 == 0 and flag:
        fn_save = root + f"20250406-JGE-pose-{n:06d}.jpg"
        cv2.imwrite(fn_save, image)
    n = n + 1
    c = cv2.waitKey(5)

    # Exit loop if 'q' is pressed
    if c & 0xFF == ord('q'):
        break
    if c & 0xFF == ord('s'):
        flag = not flag

# Release resources
pose.close()
cap.release()
cv2.destroyAllWindows()

####################################################
