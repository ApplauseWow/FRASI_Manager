# -*-coding:utf-8-*-
import face_recognition
import cv2
import numpy
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.externals import joblib

# 进一步需要解决注册时添加标签（字典）
# 不应该有unknown?这里unknown 有两个人的特征   导致guogoayu识别不出来？
def person_id(n):
    n = bytes.decode(n)
    id = {"guogaoyu": 201610414206, "trump": 201610414225}
    return id[n]


# for i in range(1, 4):
#     # ret, frame = cv2.VideoCapture(0).read()
#     frame = cv2.imread("./g"+str(i)+".jpg")
#     face = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#     location = face_recognition.face_locations(face, model="cnn")
#     encoding = face_recognition.face_encodings(face, location)
#     numpy.savetxt(i.__str__()+'.txt', encoding, delimiter=",")
#     with open(i.__str__()+'.txt', "r") as f:
#         lines = f.readlines()
#         for line in lines:
#             line = line.strip("\n") + ",guogaoyu\n"
#             with open("data.dat", "a") as e:
#                 e.write(line)


path = u"./data.dat"
data = numpy.loadtxt(path, delimiter=",", converters={128: person_id}, dtype=float)
x, y = numpy.split(data, (128, ), axis=1)
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42, train_size=0.6)
classifier = svm.SVC(C = 0.8, gamma=20, kernel='rbf', probability=True, decision_function_shape='ovr')
classifier.fit(x_train, y_train)
joblib.dump(classifier, "classifier.dat")
print(classifier.score(x_train, y_train))

#
# # ufunc 返回的是object类型 但是ufunc是在哪一步计算的？ debug中所有数据都是float64
# # 之前print("predict:\n" + classifier.predict(x_test))
# # 当成连接字符串结果把"字符串"当做矩阵做add...导致ufunc add 类型不对 此错误完全和ufunc无关 是操作失误
# print("predict:\n", classifier.predict(x_test))
# print("score:\n", classifier.predict_proba(x))
#
# print("--------------predict the current frame:----------------\n")
#
# clf = joblib.load("./classifier.dat")
#
# while True:
#     ret, frame = cv2.VideoCapture(0).read()
#     frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#     location = face_recognition.face_locations(frame)
#     encoding = face_recognition.face_encodings(frame, location)
#     encoding = numpy.asarray(encoding, float)
#     print(clf.predict(encoding))
#
#
# '''
# face = cv2.imread("../face/1.jpg")
# face = cv2.resize(face, (0, 0), fx=0.25, fy=0.25)
# location = face_recognition.face_locations(face)
# encoding = face_recognition.face_encodings(face, location)
# print(clf.predict(encoding))
# '''
#
# '''
# for i in range(1, 4):
#     index = i.__str__()+".jpg"
#     path = "../face/10518/201610414206/"+index
#     img = cv2.imread(path)
#     img2 = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
#     loc = face_recognition.face_locations(img2)
#     enc = face_recognition.face_encodings(img2, loc)
#     numpy.savetxt(i.__str__()+".txt", enc, delimiter=",")
#     with open(i.__str__()+".txt", "r") as f:
#         ls= f.readlines()
#         for l in ls:
#             l = l.strip("\n")+",yanglei\n"
#             with open("./data.dat", "a") as e:
#                 e.write(l)
#
# '''

# 了解二分查找