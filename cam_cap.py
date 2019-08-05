import numpy as np
import cv2
import time
import os

cap = cv2.VideoCapture(0)
ret = cap.set(3,1920)
ret = cap.set(4,1080)

# scrn_path = ".\\output\\scrn\\"
scrn_path = "cam_cap"
if not os.path.exists(scrn_path):
    os.mkdir(scrn_path)


rate = 10
# cap.set(cv2.CV_CAP_PROP_FPS, 10)
frame_idx = 0
count = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_rs = cv2.resize(frame, (1056, 640))


    # print("frame.shape: ", frame.shape)
    if frame_idx == rate:
        print(frame_idx, count)
        suc = cv2.imwrite(os.path.join(scrn_path, (6-len(str(count)))*'0'+str(count)+".jpg"),frame)
        print("suc:", suc, scrn_path+(6-len(str(count)))*'0'+str(count)+".jpg")
        count += 1
        frame_idx = 0


    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame_rs, cv2.COLOR_BGR2GRAY)
    # time.sleep(0.1)

    # Display the resulting frame
    # cv2.imshow('frame',gray)
    cv2.imshow('frame',frame_rs)
    frame_idx += 1
    # print("frame_idx: ", frame_idx)
    # frame_idx %= rate
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()