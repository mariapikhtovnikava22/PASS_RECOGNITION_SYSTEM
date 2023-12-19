# Importing necessary module
import cv2
import os
import easyocr
import time
from base import data
from difflib import get_close_matches

# Loading training data
face_recognizer = cv2.face.LBPHFaceRecognizer.create()

face_recognizer.read('Training_data.yml')

# some initializations
x, y, w, h = 0, 0, 0, 0
l = ''


def recognise_text(image_path):
    result = ""
    reader = easyocr.Reader(['ru'], gpu=False)
    res = reader.readtext(image_path)
    # Извлечение чистого текста
    clean_text = [result[1] for result in res if result[1].strip() and result[1] != '"']

    return clean_text


# Function for detecting the faces and drawing rectangular frames around faces
def face_detector(img):
    global x, y, w, h
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # converting colored image to grayscale

    # Loading haar cascade classifier
    face_classifier = cv2.CascadeClassifier(
        'haarcascade_frontalface_default.xml')

    # getting coordinates of the detected faces
    faces = face_classifier.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=7)

    roi = None

    if len(faces) == ():
        return img, []

    # Drawing rectangular frames around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = img[y:y + h, x:x + w]  # cropping region of interest i.e. face area
        roi = cv2.resize(roi, (500, 500))  # Resizing the cropped region

    return img, roi


def text_check(text, label):
    userdata = data[label]
    facult = ["фксис", "ксис", "фкп", "иэф", "фсис", "фкснс"]
    is_facult = False
    date = ["30.06.2024", "30.06 2024", "30  2024", "2024"]
    is_date = False
    is_fio = False
    cheek = False

    for i in text:
        for j in facult:
            i.lower()
            print(i, j)
            if j in i.lower():
                is_facult = True
                break

    for i in text:
        print(i.lower())
        for j in date:
            if j in i.lower():
                is_date = True
                break

    print(is_facult, is_date)
    if is_facult and is_date:
        cheek = True
    else:
        cheek = False

    print(cheek)
    return cheek


# capturing video capture object
cap = cv2.VideoCapture(4)
recognise = False
check = -1
if_check = False

while True:
    ret, img_frame = cap.read()  # Reading images from web camer
    result = []
    image, req_face = face_detector(img_frame)  # calling face_detector() method

    try:
        req_face = cv2.cvtColor(req_face, cv2.COLOR_BGR2GRAY)
        label, confidence = face_recognizer.predict(req_face)  # predicting the label of given image
        print('Confidence :', confidence)
        print('Label :', label)

        l = label

        face_label = data[label]  # finding face labels to be displayed on rectangular frames
        # print(face_label)

        if (label == l) and (confidence < 50):
            if not recognise and if_check and check == label:
                cv2.putText(image, ' DOES NOT LIVE IN A HOSTEL', (50, 450),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255),
                            2)  # displaying 'Face not found' when no face is recognized
                cv2.imshow('Face Recognizer', image)
            elif recognise and check == label:
                cv2.putText(image, face_label['normname'].upper() + ' LIVES IN A HOSTEL', (50, 450),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0),
                            2)  # displaying 'Face not found' when no face is recognized
                cv2.imshow('Face Recognizer', image)
            else:
                cv2.putText(image, face_label['normname'], (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0),
                            2)  # displaying 'Name' of the recognized face
                cv2.imshow('Face Recognizer', image)
        else:
            print('Unknown Face !!!')
            cv2.putText(image, 'Unknown', (x, y), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255),
                        2)  # displaying 'Unknown' when unknown face is recognized
            cv2.putText(image, ' DOES NOT LIVE IN A HOSTEL', (50, 450),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255),
                        2)  # displaying 'Face not found' when no face is recognized
            cv2.imshow('Face Recognizer', image)

    except:
        if_check = False
        print('Face not found')
        cv2.putText(image, 'X X X ! Face Not Found ! X X X', (50, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255),
                    2)  # displaying 'Face not found' when no face is recognized
        cv2.imshow('Face Recognizer', image)

    if cv2.waitKey(1) == 13:  # Waits indefinitely until enter key is pressed

        try:
            data_path = 'test_trainner'
            label, confidence = face_recognizer.predict(req_face)
            for i in range(2):
                # Сохраняем кадр как изображение
                image_path = os.path.join(data_path, f'image_{i}.png')
                gray_img = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(image_path, gray_img)

                text = recognise_text(image_path)
                print(text)
                recognise = text_check(text, label)

            check = label

            if_check = True
            continue
        except:
            cv2.putText(image, 'X X X ! Face Not Found ! X X X', (50, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255),
                        2)  # displaying 'Face not found' when no face is recognized
            cv2.imshow('Face Recognizer', image)

cap.release()  # releasing the camera
cv2.destroyAllWindows()
