import os

import cv2
import numpy as np
from PIL import Image


# def colored_mask(img, threshold=-1):
#     # Convert Pillow Image to NumPy array
#     img_np = np.array(img)
#
#     # Размытие для удаления мелких шумов.
#     denoised = cv2.medianBlur(img_np, 3)
#     cv2.imwrite('denoised.bmp', denoised)
#
#     # Сохранение в ЧБ для получения маски.
#     gray = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)
#     cv2.imwrite('gray.bmp', gray)
#
#     # Получение цветной части изображения.
#     adaptiveThreshold = threshold if threshold >= 0 else cv2.mean(img_np)[0]
#     color = cv2.cvtColor(denoised, cv2.COLOR_BGR2HLS)
#
#     # Adjust the hue range for red-brown shades
#     hsv_min = np.array((53, 0, 0), np.uint8)
#     hsv_max = np.array((83, 255, 255), np.uint8)
#     mask = cv2.inRange(color, hsv_max, hsv_min)
#
#     # Создание маски цветной части изображения.
#     dst = cv2.bitwise_and(gray, gray, mask=mask)
#     cv2.imwrite('colors_mask.bmp', mask)
#
#     return dst
#
#
# def colored_mask1(img, threshold=-5):
#     img_np = np.array(img)
#     # Размытие для удаления мелких шумов
#     denoised = cv2.medianBlur(img_np, 3)
#     cv2.imwrite('denoised.bmp', denoised)
#
#     # Сохранение в ЧБ для получения маски.
#     gray = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)
#     cv2.imwrite('gray.bmp', gray)
#
#     # Получение цветной части изображения.
#     adaptiveThreshold = threshold if threshold >= 0 else cv2.mean(img_np)[0]
#     color = cv2.cvtColor(denoised, cv2.COLOR_BGR2HLS)
#     mask = cv2.inRange(color, (0, int(adaptiveThreshold / 6), 45), (270, adaptiveThreshold, 355))
#
#     # Создание маски цветной части изображения.
#     dst = cv2.bitwise_and(gray, gray, mask=mask)
#     cv2.imwrite('colors_mask.bmp', dst)
#     return dst
#
#
# image = Image.open('img_7.png')
# colored_mask1(image)


folder = r'/home/maria/Загрузки/PASS_RECOGNITION_SYSTEM_FOR_PASSING_CONTROL/for_pechat/DataSet/Bad'
count = 1

file_names = os.listdir(folder)
file_names.sort()

for file_name in os.listdir(folder):
    source = os.path.join(folder, file_name)
    destination = os.path.join(folder, str(count) + ".png")
    # print('Good\\' + str(count) + ".png" + ' 1 0 0 364 500')
    print('Bad\\' + str(count) + ".png")
    os.rename(source, destination)
    count += 1

# verify the result
res = os.listdir(folder)
print(res)


