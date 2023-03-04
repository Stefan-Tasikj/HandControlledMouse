import mediapipe as mp
import cv2
from mediapipe.tasks import python
import pyautogui
import motion as move

pyautogui.FAILSAFE = False
# BaseOptions = mp.tasks.BaseOptions
# GestureRecognizer = mp.tasks.vision.GestureRecognizer
# GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
# VisionRunningMode = mp.tasks.vision.RunningMode
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.3)
mpDraw = mp.solutions.drawing_utils


def checkdistance(x1, x2, y1, y2):
    # checks if distance between thumb and index base is very small, consistent with a thumb in palm gesture
    dist = abs(((x1 + x2) ** 2 - (y1 + y2) ** 2) ** 0.5)
    print(f'distance: {dist}')
    if dist <= 300:
        return True
    else:
        return False


while cap.isOpened():
    ret, frame = cap.read()
    x, y, c = frame.shape
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)
    className = ''
    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            relindx = int(handslms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].x * 1980 * 1.8 - 300)
            relindy = int(handslms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP].y * 1080 * 1.8 - 300)
            tmbx = int(handslms.landmark[mpHands.HandLandmark.THUMB_TIP].x * 1980)
            tmby = int(handslms.landmark[mpHands.HandLandmark.THUMB_TIP].y * 1080)
            basex = int(handslms.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP].x * 1980)
            basey = int(handslms.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP].y * 1080)
            print("thumb coords")
            print(tmbx, tmby)
            print("base coords")
            print("______")
            print(basex, basey)
            move.movement(relindx, relindy)
            if checkdistance(tmbx, tmby, basex, basey):
                pyautogui.click()
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * 1920)
                lmy = int(lm.y * 1080)
                landmarks.append([lmx, lmy])
                mpDraw.draw_landmarks(frame, handslms,
                                      mpHands.HAND_CONNECTIONS)
    cv2.imshow('Landmarks', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
