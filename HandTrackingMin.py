import cv2
import mediapipe as mp
import time

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("HandTrackingProject/Videos/9.mp4")
# fixed window size for visualization purposes
fixed_width = 450
fixed_height = 900

# Create a named window and set its size
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", fixed_width, fixed_height)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime=0
cTime = 0


while True:
    success, img = cap.read()
    img = cv2.resize(img, (fixed_width, fixed_height))
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    

    # connects the points on the fingers  
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                print(id,lm)
                # height width channels
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)

                # if id == 0:
                cv2.circle(img,(cx,cy), 7, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img,handLms, mpHands.HAND_CONNECTIONS)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)

