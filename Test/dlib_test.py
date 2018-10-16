import dlib
from cv2.cv2 import *

img_path = '1.jpg'
img = imread(img_path)
img_rgb = cvtColor(img, COLOR_BGR2RGB)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
rects, scores, idx = detector.run(img_rgb, 2, 0)
faces = dlib.full_object_detections()
for rect in rects:
    faces.append(predictor(img_rgb, rect))
for landmark in faces:
    for idx, point in enumerate(landmark.parts()):
        putText(img, str(idx), (point.x, point.y), FONT_HERSHEY_DUPLEX, 0.3, (0,0,255), 1, LINE_AA)