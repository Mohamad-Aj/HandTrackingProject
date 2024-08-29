import cv2
import time
import numpy as np
from HandTrackingModule import HandDetector
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui
import speech_recognition as sr

wCam, hCam = 1280, 720
cap = cv2.VideoCapture(0)

cap.set(3, hCam)
cap.set(4, wCam)

pTime = 0
detector = HandDetector(detectionCon=0.7)

# Control Volume using pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]
vol = 0 
volume_control_enabled = True

def listen_for_activation():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Listening for the activation and deactivation commands...")

    with mic as source:
        while True:
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"Command heard: {command}")

                if "activate volume" in command:
                    print("Activation command detected!")
                    return "activate"
                elif "deactivate" in command:
                    print("Deactivation command detected!")
                    return "deactivate"
            except sr.UnknownValueError:
                print("Sorry, I did not catch that.")
            except sr.RequestError:
                print("Sorry, my speech service is down.")

volume_control_enabled_command = False

# Main loop
while True:
    if not volume_control_enabled_command:
        # Wait for activation command
        command = listen_for_activation()
        if command == "activate":
            pyautogui.press('volumedown')
            time.sleep(0.05)
            pyautogui.press('volumeup')
            volume_control_enabled_command = True
        elif command == "deactivate":
            break  # Exit the program when "deactivate volume" is detected

    success, img = cap.read()
    if not success or img is None:
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) and lmList[12][2] < lmList[10][2]:  # Middle finger is up
        volume_control_enabled = False
         # Listen for the deactivate command when the middle finger is up
        command = listen_for_activation()
        if command == "deactivate":
            break
    else:
        volume_control_enabled = True

    if volume_control_enabled and volume_control_enabled_command and len(lmList):
        pyautogui.press('volumedown')
        time.sleep(0.05)
        pyautogui.press('volumeup')

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

        vol = np.interp(length, [50, 200], [minVol, maxVol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    img = cv2.flip(img, 1)
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
