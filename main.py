import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# # For static images:
# IMAGE_FILES = []
# with mp_hands.Hands(
#     static_image_mode=True,
#     max_num_hands=2,
#     min_detection_confidence=0.5) as hands:
#   for idx, file in enumerate(IMAGE_FILES):
#     # Read an image, flip it around y-axis for correct handedness output (see
#     # above).
#     image = cv2.flip(cv2.imread(file), 1)
#     # Convert the BGR image to RGB before processing.
#     results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#
#     # Print handedness and draw hand landmarks on the image.
#     print('Handedness:', results.multi_handedness)
#     if not results.multi_hand_landmarks:
#       continue
#     image_height, image_width, _ = image.shape
#     annotated_image = image.copy()
#     for hand_landmarks in results.multi_hand_landmarks:
#       print('hand_landmarks:', hand_landmarks)
#       print(
#           f'Index finger tip coordinates: (',
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
#       )
#       mp_drawing.draw_landmarks(
#           annotated_image,
#           hand_landmarks,
#           mp_hands.HAND_CONNECTIONS,
#           mp_drawing_styles.get_default_hand_landmarks_style(),
#           mp_drawing_styles.get_default_hand_connections_style())
#     cv2.imwrite(
#         '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
#     # Draw hand world landmarks.
#     if not results.multi_hand_world_landmarks:
#       continue
#     for hand_world_landmarks in results.multi_hand_world_landmarks:
#       mp_drawing.plot_landmarks(
#         hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)

# For webcam input:
cap = cv2.VideoCapture(2)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    w, h, _ = image.shape

    results = hands.process(image)
    # print(results.multi_hand_landmarks)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())

    # Flip the image horizontally for a selfie-view display. 640 x 480
    # cv2.line(image, (0, 340), (640, 340), (0, 0, 255), 2)
    # cv2.line(image, (0, 240), (640, 240), (0, 255, 0), 2)
    # cv2.line(image, (0, 140), (640, 140), (255, 0, 0), 2)
    cv2.rectangle(image, (0, 100), (640, 200), (255, 0, 0), 2)

    try:
      for i in range(0, 2):
        try:
          hand_lr = results.multi_handedness[i].classification[0].label
          print(hand_lr)
          p1 = results.multi_hand_landmarks[i].landmark[4]
          p2 = results.multi_hand_landmarks[i].landmark[8]
          p3 = results.multi_hand_landmarks[i].landmark[12]
          p4 = results.multi_hand_landmarks[i].landmark[16]
          p5 = results.multi_hand_landmarks[i].landmark[20]
          if hand_lr == 'Left':
            cv2.line(image, (int(p1.x * h), int(p1.y * w)), (int(p2.x * h), int(p2.y * w)), (0, 0, 255), 2)
            cv2.line(image, (int(p2.x * h), int(p2.y * w)), (int(p3.x * h), int(p3.y * w)), (0, 255, 255), 2)
            cv2.line(image, (int(p3.x * h), int(p3.y * w)), (int(p4.x * h), int(p4.y * w)), (255, 0, 255), 2)
            cv2.line(image, (int(p4.x * h), int(p4.y * w)), (int(p5.x * h), int(p5.y * w)), (0, 255, 0), 2)
          elif hand_lr == 'Right':
            cv2.line(image, (int(p1.x * h), int(p1.y * w)), (int(p2.x * h), int(p2.y * w)), (0, 0, 255), 2)
            cv2.line(image, (int(p2.x * h), int(p2.y * w)), (int(p3.x * h), int(p3.y * w)), (0, 255, 255), 2)
            cv2.line(image, (int(p3.x * h), int(p3.y * w)), (int(p4.x * h), int(p4.y * w)), (255, 0, 255), 2)
            cv2.line(image, (int(p4.x * h), int(p4.y * w)), (int(p5.x * h), int(p5.y * w)), (0, 255, 0), 2)
        except:
          continue

    except Exception as ex:
      # pass
      print(ex)
      # continue

    cv2.imshow('MediaPipe Hands', cv2.flip(image, 2))
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
