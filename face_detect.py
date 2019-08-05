import cv2
import os
import time
import sys

#
# xml_dir = r"C:\Users\zhengl11\venv\PyQt5\Lib\site-packages\cv2\data"
#
# face_cascade = cv2.CascadeClassifier(os.path.join(xml_dir, 'haarcascade_frontalface_default.xml'))
# eye_cascade = cv2.CascadeClassifier(os.path.join(xml_dir, 'haarcascade_eye.xml'))
#
#
#
# upperBody_cascade = cv2.CascadeClassifier(os.path.join(xml_dir, 'haarcascade_upperbody.xml'))
#
#
#
#
# img = cv2.imread('obama.jpg')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#
# # arrUpperBody = upperBody_cascade.detectMultiScale(gray)
# # if arrUpperBody != ():
# #         for (x,y,w,h) in arrUpperBody:
# #             cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
# #         print('body found')
# #
# # cv2.imshow('image',img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
#
#
# # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
# # for (x,y,w,h) in faces:
# #     img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
# #     roi_gray = gray[y:y+h, x:x+w]
# #     roi_color = img[y:y+h, x:x+w]
# #     eyes = eye_cascade.detectMultiScale(roi_gray)
# #     for (ex,ey,ew,eh) in eyes:
# #         cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
# #
# # cv2.imshow('img',img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
#
# class FaceDetect(object):
#     def __init__(self, xml_dir):
#         super(FaceDetect, self).__init__()
#         self._xml_dir = xml_dir
#         self.face_cascade = cv2.CascadeClassifier(os.path.join(xml_dir, 'haarcascade_frontalface_default.xml'))
#         self.eye_cascade = cv2.CascadeClassifier(os.path.join(xml_dir, 'haarcascade_eye.xml'))
#         self.upperBody_cascade = cv2.CascadeClassifier(os.path.join(xml_dir, 'haarcascade_upperbody.xml'))
#
#     def detect_face(self, img_bgr):
#         gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#         if len(faces) != 0:
#             for (x, y, w, h) in faces:
#                 img = cv2.rectangle(img_bgr, (x, y), (x + w, y + h), (255, 0, 0), 2)
#         else:
#             img = img_bgr
#         cv2.imshow('img', img)
#         cv2.waitKey(1000)
#         cv2.destroyAllWindows()
#         return img
#
#
# face_detector = FaceDetect(xml_dir)
#
# face_detector.detect_face(cv2.imread('obama.jpg'))
#
#
# cap_dir = "cam_cap"
# for i in os.listdir(cap_dir):
#     print(i)
#     img = cv2.imread(os.path.join(cap_dir, i))
#     det = face_detector.detect_face(img)
#     cv2.imwrite(os.path.join("out", i), det)



# import cv2
# import dlib
#
# cameraCapture = cv2.VideoCapture(0)
# success, frame = cameraCapture.read()
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(
#     "shape_predictor_68_face_landmarks.dat")
#
# while success and cv2.waitKey(1) == -1:
#     success, frame = cameraCapture.read()
#
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)              #生成灰度图
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)) #生成直方图
#     clahe_image = clahe.apply(gray)
#     detections = detector(clahe_image, 1)
#
#     for k, d in enumerate(detections):
#         shape = predictor(clahe_image, d)  # 获取坐标
#         for i in range(1, 68):  # 每张脸都有68个识别点
#             cv2.circle(frame, (shape.part(i).x, shape.part(i).y), 1, (0, 0, 255),
#                        thickness=2)
#
#     cv2.imshow("Camera", frame)
#
# cameraCapture.release()
# cv2.destroyAllWindows()



def detectFaceOpenCVDnn(net, frame):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes

if __name__ == "__main__" :

    # OpenCV DNN supports 2 networks.
    # 1. FP16 version of the original caffe implementation ( 5.4 MB )
    # 2. 8 bit Quantized version using Tensorflow ( 2.7 MB )
    DNN = "TF"
    if DNN == "CAFFE":
        modelFile = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
        configFile = "models/deploy.prototxt"
        net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    else:
        modelFile = "models/opencv_face_detector_uint8.pb"
        configFile = "models/opencv_face_detector.pbtxt"
        net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

    conf_threshold = 0.5

    source = 0
    if len(sys.argv) > 1:
        source = sys.argv[1]

    cap = cv2.VideoCapture(source)
    hasFrame, frame = cap.read()

    vid_writer = cv2.VideoWriter('output-dnn-{}.avi'.format(str(source).split(".")[0]),cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))

    frame_count = 0
    tt_opencvDnn = 0
    while(1):
        hasFrame, frame = cap.read()
        if not hasFrame:
            break
        frame_count += 1

        t = time.time()
        outOpencvDnn, bboxes = detectFaceOpenCVDnn(net,frame)
        tt_opencvDnn += time.time() - t
        fpsOpencvDnn = frame_count / tt_opencvDnn
        label = "OpenCV DNN ; FPS : {:.2f}".format(fpsOpencvDnn)
        cv2.putText(outOpencvDnn, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3, cv2.LINE_AA)

        cv2.imshow("Face Detection Comparison", outOpencvDnn)

        vid_writer.write(outOpencvDnn)
        if frame_count == 1:
            tt_opencvDnn = 0

        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()
    vid_writer.release()