import cv2
import numpy as np
import os

# Загрузите каскадный классификатор для обнаружения лиц
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Укажите путь к папке, где хранятся изображения
data_path = 'DataSet'

# Создайте два списка для хранения данных для обучения и связанных с ними меток
training_data, labels = [], []

# Перебирайте файлы в папке и находите изображения лиц с соответствующими метками
for filename in os.listdir(data_path):
    if filename.startswith('.'):
        print('Пропуск системного файла')  # Пропустить системные файлы
        continue

    file_parts = filename.split('.')  # Разделите имя файла на части
    if len(file_parts) != 4 or file_parts[0] != 'User':
        continue  # Ожидается имя файла в формате "User.ID.NUM.jpg"

    f_id = file_parts[1]  # Извлекаем метку пользователя из имени файла
    img_path = os.path.join(data_path, filename)  # Создаем путь к изображению
    print('img_path:', img_path)
    print('f_id:', f_id)

    test_img = cv2.imread(img_path)  # Загрузка/чтение каждого изображения

    # Проверьте, загрузилось ли изображение правильно
    if test_img is None:
        print('Изображение не загрузено должным образом!!!')
        continue

    test_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    print('test_gray:', test_gray)

    # Обнаруживаем лицо на изображении
    faces = face_classifier.detectMultiScale(test_gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) != 1:
        continue  # Поскольку предполагается, что на входной модуль будет передано только одно лицо

    for (x, y, w, h) in faces:
        roi_gray = test_gray[y:y + h, x:x + w]  # Вырезаем область интереса - лицо

    roi_gray = cv2.resize(roi_gray, (500, 500))  # Изменяем размер вырезанной области

    # Подготовка данных для обучения
    training_data.append(roi_gray)  # Добавляем область лица в обучающие данные
    labels.append(int(f_id))  # Добавляем связанные с обнаруженными лицами метки

# Создаем модель для распознавания лиц с использованием LBPH

model = cv2.face.LBPHFaceRecognizer.create()

# Обучаем модель на данных
model.train(training_data, np.array(labels))

# Сохраняем обученную модель
model.save('Training_data.yml')

print('Обучение модели завершено!!!')
