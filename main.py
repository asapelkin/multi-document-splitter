import cv2
import os
import numpy as np

# Путь к исходному файлу сканирования визитных карточек
input_file = '/Volumes/sd_storage/yadisk/family_archive/holzman_business_cards/img20241109_20210851.png'
output_folder = 'out'

# Создаем папку для сохранения отдельных карточек, если ее нет
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Загружаем изображение
image = cv2.imread(input_file)

# Преобразуем изображение в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применяем размытие для уменьшения шума
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Применяем пороговое преобразование с инверсией, чтобы фон стал белым, а объекты — черными
_, threshold = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)

# Сохраняем промежуточное изображение для проверки
cv2.imwrite(os.path.join(output_folder, 'threshold_output.jpg'), threshold)

# Находим контуры после пороговой обработки
contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Копия изображения для отображения контуров
contour_image = image.copy()

# Проходим по каждому контуру, фильтруя их по форме и размеру
for i, contour in enumerate(contours):
    # Вычисляем прямоугольник, ограничивающий контур
    x, y, w, h = cv2.boundingRect(contour)

    # Фильтр по форме и размеру, чтобы выбрать только визитки
    aspect_ratio = w / float(h)
    if 1.5 < aspect_ratio < 3.5 and w > 200 and h > 100:  # Примерное соотношение сторон визитки

        # Добавляем небольшой отступ для рамки
        padding = 10  # Размер отступа для белой рамки
        x_start = max(x - padding, 0)
        y_start = max(y - padding, 0)
        x_end = min(x + w + padding, image.shape[1])
        y_end = min(y + h + padding, image.shape[0])

        # Вырезаем область визитки с отступом
        card = image[y_start:y_end, x_start:x_end]

        # Сохраняем каждый фрагмент как отдельный файл
        output_path = os.path.join(output_folder, f'card_{i+1}.jpg')
        cv2.imwrite(output_path, card)
        print(f'Сохранено: {output_path}')

        # Отображаем контуры для проверки
        cv2.rectangle(contour_image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

# Сохраняем изображение с отмеченными контурами для проверки
cv2.imwrite(os.path.join(output_folder, 'contours_output_with_padding.jpg'), contour_image)

print("Разделение завершено!")
