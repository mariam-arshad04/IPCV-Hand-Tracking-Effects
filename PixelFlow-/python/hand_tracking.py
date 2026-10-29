# import cv2
# import mediapipe as mp
# import math
# from pythonosc import udp_client


# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils

# hands = mp_hands.Hands(
#     static_image_mode=False,
#     max_num_hands=2,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
# )


# def count_fingers(hand_landmarks, hand_label):

#     fingers = 0

#     # Four fingers
#     finger_tips = [
#         mp_hands.HandLandmark.INDEX_FINGER_TIP,
#         mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
#         mp_hands.HandLandmark.RING_FINGER_TIP,
#         mp_hands.HandLandmark.PINKY_TIP
#     ]

#     finger_pips = [
#         mp_hands.HandLandmark.INDEX_FINGER_PIP,
#         mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
#         mp_hands.HandLandmark.RING_FINGER_PIP,
#         mp_hands.HandLandmark.PINKY_PIP
#     ]

#     for tip, pip in zip(finger_tips, finger_pips):

#         if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
#             fingers += 1

#     # Thumb
#     thumb_tip = hand_landmarks.landmark[
#         mp_hands.HandLandmark.THUMB_TIP
#     ]

#     thumb_ip = hand_landmarks.landmark[
#         mp_hands.HandLandmark.THUMB_IP
#     ]

#     if hand_label == "Right":

#         if thumb_tip.x < thumb_ip.x:
#             fingers += 1

#     else:

#         if thumb_tip.x > thumb_ip.x:
#             fingers += 1

#     return fingers



# def get_hand_control(hand_landmarks):

#     thumb = hand_landmarks.landmark[
#         mp_hands.HandLandmark.THUMB_TIP
#     ]

#     index = hand_landmarks.landmark[
#         mp_hands.HandLandmark.INDEX_FINGER_TIP
#     ]

#     # Distance between thumb and index
#     dx = index.x - thumb.x
#     dy = index.y - thumb.y

#     distance = math.sqrt(dx ** 2 + dy ** 2)

#     # Angle between thumb and index
#     angle = math.degrees(math.atan2(dy, dx))

#     return distance, angle



# def normalize(value, min_value, max_value):

#     value = max(min_value, min(value, max_value))

#     return (value - min_value) / (max_value - min_value)



# cap = cv2.VideoCapture(0)



# client = udp_client.SimpleUDPClient(
#     "127.0.0.1",
#     9000
# )



# previous_strength = 0.4
# alpha = 0.15

# previous_rotation = 0.0
# rotation_alpha = 0.15



# while True:

#     ret, frame = cap.read()

#     if not ret:
#         print("Could not read from camera.")
#         break

#     # Mirror camera
#     frame = cv2.flip(frame, 1)

#     # BGR → RGB
#     rgb_frame = cv2.cvtColor(
#         frame,
#         cv2.COLOR_BGR2RGB
#     )

#     # MediaPipe
#     results = hands.process(rgb_frame)


#     if results.multi_hand_landmarks:

#         for hand_landmarks, handedness in zip(
#             results.multi_hand_landmarks,
#             results.multi_handedness
#         ):

#             # Get Left / Right label
#             hand_label = handedness.classification[0].label


#             if hand_label == "Right":

#                 right_fingers = count_fingers(
#                 hand_landmarks,
#                 hand_label
#                 )
                
#                 # Get distance and angle
#                 distance, angle = get_hand_control(
#                     hand_landmarks
#                 )

               
#                 normalized_distance = normalize(
#                     distance,
#                     0.02,
#                     0.97
#                 )

#                 current_strength = (
#                     0.4
#                     + normalized_distance * 0.4
#                 )


#                 distortion_strength = (
#                     alpha * current_strength
#                     + (1 - alpha) * previous_strength
#                 )

#                 previous_strength = distortion_strength


#                 if right_fingers == 0:
#                   current_rotation = 0.0
#                 else:
#                   current_rotation = angle / 180.0

#                 # Smooth rotation
#                 rotation = (
#                     rotation_alpha * current_rotation
#                     + (1 - rotation_alpha) * previous_rotation
#                 )

#                 previous_rotation = rotation


#                 client.send_message(
#                     "/distortion",
#                     distortion_strength
#                 )

#                 client.send_message(
#                    "/rotation",
#                     rotation
#                 )

#                 cv2.putText(
#                     frame,
#                     f"Distance: {distance:.2f}",
#                     (30, 130),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.8,
#                     (0, 255, 0),
#                     2
#                 )

#                 cv2.putText(
#                     frame,
#                     f"Strength: {distortion_strength:.2f}",
#                     (30, 165),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.8,
#                     (0, 255, 0),
#                     2
#                 )

#                 cv2.putText(
#                     frame,
#                     f"Angle: {angle:.1f}",
#                     (30, 200),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.8,
#                     (0, 255, 0),
#                     2
#                 )

#                 cv2.putText(
#                     frame,
#                     f"Rotation: {rotation:.2f}",
#                     (30, 235),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.8,
#                     (0, 255, 0),
#                     2
#                 )


#             elif hand_label == "Left":

#                 finger_count = count_fingers(
#                     hand_landmarks,
#                     hand_label
#                 )
#                 client.send_message(
#                  "/finger_count",
#                   finger_count
#                 )
#                 if finger_count == 0:

#                     mode = "GRAYSCALE"

#                 elif finger_count == 1:

#                     mode = "RED"

#                 elif finger_count == 2:

#                     mode = "GREEN"

#                 elif finger_count == 3:

#                     mode = "BLUE"

#                 elif finger_count == 5:

#                     mode = "RGB"

#                 else:

#                     mode = "UNKNOWN"


#                 cv2.putText(
#                     frame,
#                     f"Fingers: {finger_count}",
#                     (30, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1,
#                     (0, 255, 0),
#                     2
#                 )


#                 cv2.putText(
#                     frame,
#                     f"Mode: {mode}",
#                     (30, 90),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1,
#                     (0, 255, 0),
#                     2
#                 )

#             mp_drawing.draw_landmarks(
#                 frame,
#                 hand_landmarks,
#                 mp_hands.HAND_CONNECTIONS
#             )


#             h, w, _ = frame.shape

#             wrist = hand_landmarks.landmark[
#                 mp_hands.HandLandmark.WRIST
#             ]

#             x = int(wrist.x * w)
#             y = int(wrist.y * h)


#             cv2.putText(
#                 frame,
#                 hand_label,
#                 (x, y - 20),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1,
#                 (0, 255, 0),
#                 2
#             )

#     cv2.imshow(
#         "PixelFlow - Hand Tracking",
#         frame
#     )

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break


# cap.release()
# hands.close()
# cv2.destroyAllWindows()


import cv2
import mediapipe as mp
import numpy as np
import math
from collections import deque


# -----------------------------
# MediaPipe setup
# -----------------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)


# -----------------------------
# Count fingers
# -----------------------------
def count_fingers(hand_landmarks, hand_label):
    fingers = 0

    finger_tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]

    finger_pips = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP
    ]

    for tip, pip in zip(finger_tips, finger_pips):
        if (
            hand_landmarks.landmark[tip].y
            < hand_landmarks.landmark[pip].y
        ):
            fingers += 1

    thumb_tip = hand_landmarks.landmark[
        mp_hands.HandLandmark.THUMB_TIP
    ]
    thumb_ip = hand_landmarks.landmark[
        mp_hands.HandLandmark.THUMB_IP
    ]

    if hand_label == "Right":
        if thumb_tip.x < thumb_ip.x:
            fingers += 1
    else:
        if thumb_tip.x > thumb_ip.x:
            fingers += 1

    return fingers


# -----------------------------
# Thumb-index distance and angle
# -----------------------------
def get_hand_control(hand_landmarks):
    thumb = hand_landmarks.landmark[
        mp_hands.HandLandmark.THUMB_TIP
    ]
    index = hand_landmarks.landmark[
        mp_hands.HandLandmark.INDEX_FINGER_TIP
    ]

    dx = index.x - thumb.x
    dy = index.y - thumb.y

    distance = math.sqrt(dx ** 2 + dy ** 2)
    angle = math.degrees(math.atan2(dy, dx))

    return distance, angle


def normalize(value, min_value, max_value):
    value = max(min_value, min(value, max_value))
    return (value - min_value) / (max_value - min_value)


# -----------------------------
# Color effects
# -----------------------------
def apply_color_mode(frame, mode):
    if mode == "GRAYSCALE":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    elif mode == "RED":
        result = np.zeros_like(frame)
        result[:, :, 2] = frame[:, :, 2]
        return result

    elif mode == "GREEN":
        result = np.zeros_like(frame)
        result[:, :, 1] = frame[:, :, 1]
        return result

    elif mode == "BLUE":
        result = np.zeros_like(frame)
        result[:, :, 0] = frame[:, :, 0]
        return result

    elif mode == "RGB":
        # Keep the original full-color image.
        # This avoids channel shifting that can look like
        # duplicated or reversed images.
        return frame.copy()

    return frame.copy()


# -----------------------------
# Swirl distortion
# -----------------------------
def apply_swirl(frame, strength, direction):
    if strength <= 0.01:
        return frame

    height, width = frame.shape[:2]
    center_x = width / 2
    center_y = height / 2

    y, x = np.indices((height, width), dtype=np.float32)

    dx = x - center_x
    dy = y - center_y

    radius = np.sqrt(dx * dx + dy * dy)
    max_radius = math.sqrt(center_x ** 2 + center_y ** 2)

    normalized_radius = radius / max_radius

    twist = (
        strength
        * 3.0
        * (1 - normalized_radius)
        * direction
    )

    cos_twist = np.cos(twist)
    sin_twist = np.sin(twist)

    map_x = center_x + dx * cos_twist - dy * sin_twist
    map_y = center_y + dx * sin_twist + dy * cos_twist

    return cv2.remap(
        frame,
        map_x,
        map_y,
        cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )


# -----------------------------
# Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam.")
    hands.close()
    raise SystemExit


# Start in full-color mode
mode = "RGB"

# Require the same left-hand mode across several frames
mode_history = deque(maxlen=8)

previous_strength = 0.0
previous_rotation = 0.0

alpha = 0.15
rotation_alpha = 0.12

# Track rotation across the -180 / +180 degree boundary
previous_raw_angle = None
unwrapped_angle = 0.0


# -----------------------------
# Main loop
# -----------------------------
try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Could not read from camera.")
            break

        # Mirror the webcam consistently.
        # This line never switches on or off.
        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        current_strength = previous_strength
        current_rotation = previous_rotation

        left_finger_count = None
        right_distance = None
        right_angle = None

        right_hand_detected = False

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):
                hand_label = handedness.classification[0].label

                # -------------------------
                # RIGHT HAND: effects only
                # -------------------------
                if hand_label == "Right":
                    right_hand_detected = True

                    right_fingers = count_fingers(
                        hand_landmarks, hand_label
                    )

                    distance, angle = get_hand_control(
                        hand_landmarks
                    )

                    right_distance = distance
                    right_angle = angle

                    if right_fingers == 0:
                        # Fist resets effects, not color mode.
                        target_strength = 0.0
                        target_rotation = 0.0
                        previous_raw_angle = None
                    else:
                        normalized_distance = normalize(
                            distance, 0.02, 0.50
                        )

                        target_strength = (
                            normalized_distance * 0.8
                        )

                        # Unwrap the angle so crossing from
                        # +180 to -180 does not cause a jump.
                        if previous_raw_angle is None:
                            unwrapped_angle = angle
                        else:
                            angle_change = (
                                (angle - previous_raw_angle + 180)
                                % 360
                            ) - 180

                            unwrapped_angle += angle_change

                        previous_raw_angle = angle

                        # Map angle to a limited rotation range.
                        target_rotation = (
                            (unwrapped_angle % 360) / 360 * 40 - 20
                        )

                    # Smooth distortion strength
                    current_strength = (
                        alpha * target_strength
                        + (1 - alpha) * previous_strength
                    )

                    # Smooth rotation using the shortest angular path
                    rotation_difference = (
                        target_rotation - previous_rotation
                    )

                    rotation_difference = (
                        (rotation_difference + 20) % 40
                    ) - 20

                    current_rotation = (
                        previous_rotation
                        + rotation_alpha * rotation_difference
                    )

                    current_rotation = max(
                        -20, min(20, current_rotation)
                    )

                # -------------------------
                # LEFT HAND: color only
                # -------------------------
                elif hand_label == "Left":
                    left_finger_count = count_fingers(
                        hand_landmarks, hand_label
                    )

                    if left_finger_count == 0:
                        detected_mode = "GRAYSCALE"
                    elif left_finger_count == 1:
                        detected_mode = "RED"
                    elif left_finger_count == 2:
                        detected_mode = "GREEN"
                    elif left_finger_count == 3:
                        detected_mode = "BLUE"
                    elif left_finger_count == 5:
                        detected_mode = "RGB"
                    else:
                        detected_mode = None

                    if detected_mode is not None:
                        mode_history.append(detected_mode)

                        # Change mode only when the last 8
                        # detected frames agree.
                        if (
                            len(mode_history) == mode_history.maxlen
                            and all(
                                item == mode_history[0]
                                for item in mode_history
                            )
                        ):
                            mode = mode_history[0]

        # Smoothly return to normal if the right hand disappears
        if not right_hand_detected:
            current_strength = (
                (1 - alpha) * previous_strength
            )
            current_rotation = (
                (1 - rotation_alpha) * previous_rotation
            )
            previous_raw_angle = None

        previous_strength = current_strength
        previous_rotation = current_rotation

        # Apply color effect first
        output = apply_color_mode(frame, mode)

        # Apply swirl only when the right hand is controlling it
        direction = 1 if current_rotation >= 0 else -1

        output = apply_swirl(
            output,
            current_strength,
            direction
        )

        # Rotate without flipping the image
        height, width = output.shape[:2]

        rotation_matrix = cv2.getRotationMatrix2D(
            (width // 2, height // 2),
            current_rotation,
            1.0
        )

        output = cv2.warpAffine(
            output,
            rotation_matrix,
            (width, height),
            borderMode=cv2.BORDER_REFLECT
        )

        # Draw hand landmarks on the displayed image
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):
                mp_drawing.draw_landmarks(
                    output,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

        # Display status
        cv2.putText(
            output, f"Mode: {mode}", (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
        )

        if left_finger_count is not None:
            cv2.putText(
                output,
                f"Left fingers: {left_finger_count}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 255, 0), 2
            )

        if right_distance is not None:
            cv2.putText(
                output,
                f"Distance: {right_distance:.2f}",
                (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 255, 0), 2
            )

            cv2.putText(
                output,
                f"Distortion: {current_strength:.2f}",
                (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 255, 0), 2
            )

            cv2.putText(
                output,
                f"Rotation: {current_rotation:.1f} degrees",
                (20, 175),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (0, 255, 0), 2
            )

        cv2.imshow("PixelFlow - Hand Tracking", output)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == 27:
            break

finally:
    cap.release()
    hands.close()
    cv2.destroyAllWindows()
