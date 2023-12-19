import os
import cv2
import time
import easyocr


def recognise_text(image_path):
    result = ""
    reader = easyocr.Reader(['ru'], gpu=False)
    res = reader.readtext(image_path)
    # Извлечение чистого текста
    clean_text = [result[1] for result in res if result[1].strip() and result[1] != '"']

    # Вывод результатов
    for text in clean_text:
        result += text + " "

    return result


def videoText():
    cap = cv2.VideoCapture(4)

    while True:
        result = []
        # Считываем кадр из видеопотока
        ret, frame = cap.read()

        # Отображаем текущий кадр
        cv2.imshow('Video Stream', frame)

        # Если клавиша 'q' нажата, выходим из цикла
        if cv2.waitKey(1) == 13:
            data_path = 'test_trainner'

            for i in range(3):
                # Сохраняем кадр как изображение
                image_path = os.path.join(data_path, f'image_{i}.png')
                gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(image_path, gray_img)

                # Задержка для создания "датасета"
                time.sleep(1)
                result.append(recognise_text(image_path))

                # Распознаем текст
            print(result)
            print('Next Session')
            continue

    # Освобождаем ресурсы камеры
    cap.release()
    cv2.destroyAllWindows()





def check(test_list):
    facult = ["фксис", "ксис", "фкп", "иэф"]



# Запускаем видеопоток
videoText()

# recognise_text('img_4.png')
