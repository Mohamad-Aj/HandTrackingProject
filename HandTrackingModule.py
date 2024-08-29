import cv2
import mediapipe as mp
import time


class HandDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon,
        )
        self.mpDraw = mp.solutions.drawing_utils




    def findHands(self,img,draw = True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        # connects the points on the fingers  
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img, handNo=0, draw=True):

        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                # print(id,lm)
                # height width channels
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id,cx,cy])
                # if id == 0:
                if draw:
                    cv2.circle(img,(cx,cy), 3, (255,0,255), cv2.FILLED)

        return lmList

    

# this dummy code is used to run the module in different files (use the model)
def main():
    pTime=0
    cTime = 0
    cap = cv2.VideoCapture(0)
    
    detector =  HandDetector()
    while True:
        success, img = cap.read()
        # if draw=false here it will not draw anything at all
        img = detector.findHands(img)
        # if draw=false here it will not draw the custome drawing
        lmList = detector.findPosition(img)

        if len(lmList):
            print(lmList[4])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
       
        img = cv2.flip(img, 1)
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow("Image",img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()