from keras.preprocessing.image import img_to_array
# import imutils
from keras.models import load_model
import numpy as np
import cv2

# 모델 로드
detection_model_path = 'models/haarcascade_frontalface_default.xml'

emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'

face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry", "disgust", "scared",
            "happy", "sad", "surprised", "neutral"]


# 이미지 로드
img = cv2.imread('imgs/4.jpg')

# 이미지 전처리하기
h, w, c = img.shape  # h = 높이, w = 너비, c = 채널
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_detection.detectMultiScale(
    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)


# 표정 퍼센트 표시해 줄 캔버스 생성
canvas = np.zeros((250, 300, 3), dtype="uint8")

# 테스트
print(len(faces))

if len(faces) > 0:
    faces = sorted(faces, reverse=True,
                   key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
    # print(faces)

    (fX, fY, fW, fH) = faces
    # print(fX)  # x1
    # print(fY)  # y1
    # print(fW)  # x2-x1
    # print(fH)  # y2-y1

    # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
    # the ROI for classification via the CNN
    roi = gray[fY:fY + fH, fX:fX + fW]
    roi = cv2.resize(roi, (64, 64))
    roi = roi.astype("float") / 255.0
    roi = img_to_array(roi)
    roi = np.expand_dims(roi, axis=0)

    preds = emotion_classifier.predict(roi)[0]
    emotion_probability = np.max(preds)
    label = EMOTIONS[preds.argmax()]
else:
    print("인식된 얼굴이 없음.")

# 감정 정보를 담을 리스트 생성
text_list = []
emotion_list = []
prob_list = []
text_dic = {}

for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
    # construct the label text
    text = "{}: {:.2f}%".format(emotion, prob * 100)
    emotion_text = "{}".format(emotion)
    prob_text = "{:.2f}".format(prob * 100)
    text_dic["{}".format(emotion)] = "{:.2f}".format(prob * 100)

    # 감정 정보 리스트로 만들기
    text_list.append(text)
    emotion_list.append(emotion_text)
    prob_list.append(prob_text)

    # draw the label + probability bar on the canvas
    # emoji_face = feelings_faces[np.argmax(preds)]

    w = int(prob * 300)
    cv2.rectangle(canvas, (7, (i * 35) + 5),
                  (w, (i * 35) + 35), (0, 0, 255), -1)
    cv2.putText(canvas, text, (10, (i * 35) + 23),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                (255, 255, 255), 2)
    cv2.putText(img, label, (fX, fY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    cv2.rectangle(img, (fX, fY), (fX + fW, fY + fH),
                  (0, 0, 255), 2)

# 이미지, 감정 정보 출력
cv2.imshow('result', img)
# cv2.imshow("Probabilities", canvas)
cv2.waitKey(0)


# 감정 정보 출력
print("전체 리스트 : ", text_list)
print("감정 리스트 : ", emotion_list)
print("확률 리스트 : ", prob_list)
print("전체 사전 : ", text_dic)

# 이미지 저장
cv2.imwrite("imgs/4-1.jpg", img)

# 넘겨줄 값 : 감정정보=text_list ... / 이미지= 경로 or 파일
